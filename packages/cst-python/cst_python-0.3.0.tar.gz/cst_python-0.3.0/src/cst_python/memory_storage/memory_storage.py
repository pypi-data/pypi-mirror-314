import json
import weakref
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import logging
import functools
from typing import Optional, cast

import redis

from cst_python.core.entities import Codelet, Mind, Memory, MemoryObject
from .memory_encoder import MemoryEncoder
from .logical_time import LogicalTime, LamportTime

logger = logging.getLogger("MemoryStorageCodelet")
logger.setLevel(logging.DEBUG)

class MemoryStorageCodelet(Codelet):
    '''
    Synchonizes local memories with a Redis database. 

    When using MemoryStorage, each local CST instance is called a node.
    Memories with the same name in participating nodes are synchronized.
    
    The collection of synchonized nodes is a mind.
    A single Redis instance can support multiple minds with unique names
    '''

    def __init__(self, mind:Mind, 
                 node_name:Optional[str]=None, mind_name:Optional[str]=None, 
                 request_timeout:float=500e-3, **redis_args) -> None:
        '''
        MemoryStorageCodelet initializer.

        Args:
            mind (Mind): agent mind, used to monitor memories.
            node_name (Optional[str], optional): name of the local node in the network.
                If None, creates a unique name with 'node{int}'. Defaults to None.
            mind_name (Optional[str], optional): name of the network mind. 
                If None, uses 'default_mind'. Defaults to None.
            request_timeout (float, optional): time before timeout when
                requesting a memory synchonization. Defaults to 500e-3.
        '''
        super().__init__()
        
        self._mind = mind
        self._request_timeout = request_timeout
        
        if mind_name is None:
            mind_name = "default_mind"
        self._mind_name = cast(str, mind_name)
        
        self._memories : weakref.WeakValueDictionary[str, Memory] = weakref.WeakValueDictionary()

        if "decode_responses" in redis_args:
            del redis_args["decode_responses"]
        
        self._client = redis.Redis(decode_responses=True, **redis_args)
        self._pubsub = self._client.pubsub()
        self._pubsub_thread : redis.client.PubSubWorkerThread = self._pubsub.run_in_thread(daemon=True)

        # Creates node name
        if node_name is None:
            node_name = "node"
        base_name = node_name
        
        if self._client.sismember(f"{mind_name}:nodes", node_name):
            node_number = self._client.scard(f"{mind_name}:nodes")
            node_name = base_name+str(node_number)
            while self._client.sismember(f"{mind_name}:nodes", node_name):
                node_number += 1
                node_name = base_name+str(node_number)
            

        self._node_name = cast(str, node_name)

        self._client.sadd(f"{mind_name}:nodes", node_name)

        # Creates transfer channels subscription
        transfer_service_addr = f"{self._mind_name}:nodes:{node_name}:transfer_memory"
        self._pubsub.subscribe(**{transfer_service_addr:self._handler_transfer_memory})

        transfer_done_addr = f"{self._mind_name}:nodes:{node_name}:transfer_done"
        self._pubsub.subscribe(**{transfer_done_addr:self._handler_notify_transfer})

        # Initalize variables

        self._last_update : dict[str, int] = {}
        self._memory_logical_time : dict[str, LogicalTime] = {}
        self._waiting_retrieve : set[str] = set()
        
        self._retrieve_executor = ThreadPoolExecutor(3)

        self._waiting_request_events : dict[str, threading.Event] = {}

        self._request = None

        self._current_time = LamportTime()

    def calculate_activation(self) -> None: #NOSONAR
        pass

    def access_memory_objects(self) -> None: #NOSONAR
        pass

    def proc(self) -> None:
        
        #Check new memories

        mind_memories : dict[str, Memory] = {}
        for memory in self._mind.raw_memory.all_memories:
            if memory.get_name() == "": #No name -> No MS
                continue

            mind_memories[memory.get_name()] = memory

        mind_memories_names = set(mind_memories.keys())
        memories_names = set(self._memories.keys())

        #Check only not here (memories_names not in mind should be garbage collected)
        difference = mind_memories_names - memories_names
        for memory_name in difference:
            memory = mind_memories[memory_name]
            self._memories[memory_name] = memory
            self._memory_logical_time[memory_name] = self._current_time

            if self._client.exists(f"{self._mind_name}:memories:{memory_name}"):
                self._retrieve_executor.submit(self._retrieve_memory, memory)
                
            else: #Send impostor with owner
                memory_impostor : dict[str|bytes, str|float|int] = {"name":memory.get_name(),
                                   "evaluation" : 0.0,
                                   "I": "",
                                   "id" : 0,
                                   "owner": self._node_name,
                                   "logical_time":str(self._current_time)}
                
                self._client.hset(f"{self._mind_name}:memories:{memory_name}", mapping=memory_impostor)
                self._current_time = self._current_time.increment()

            subscribe_func = lambda _, name : self.update_memory(name)
            subscribe_func = functools.partial(subscribe_func, name=memory_name)
            self._pubsub.subscribe(**{f"{self._mind_name}:memories:{memory_name}:update":subscribe_func})

        #Update memories
        to_update = self._last_update.keys()
        for memory_name in to_update:
            if memory_name not in self._memories:
                del self._last_update[memory_name]
                del self._memory_logical_time[memory_name]
                continue

            memory = self._memories[memory_name]
            if memory.get_timestamp() > self._last_update[memory_name]:
                self._memory_logical_time[memory_name] = self._current_time
                self.update_memory(memory_name)

    def update_memory(self, memory_name:str) -> None:
        '''
        Updates a memory, sending or retrieving the memory data
        to/from the database.

        Performs a time comparison with the local data and storage
        data to decide whether to send or retrieve the data.

        Args:
            memory_name (str): name of the memory to synchonize.
        '''
        logger.info(f"Updating memory [{memory_name}@{self._node_name}]")

        if memory_name not in self._memories:
            self._pubsub.unsubscribe(f"{self._mind_name}:memories:{memory_name}:update")
            return

        message_time_str = self._client.hget(f"{self._mind_name}:memories:{memory_name}", "logical_time")
        assert message_time_str is not None
        message_time = LamportTime.from_str(message_time_str)
        memory_time = self._memory_logical_time[memory_name]

        memory = self._memories[memory_name]
        
        if memory_time < message_time:
            self._retrieve_executor.submit(self._retrieve_memory, memory)

        elif memory_time > message_time:
            self._send_memory(memory)

        self._last_update[memory_name] = memory.get_timestamp()


    def _send_memory(self, memory:Memory) -> None:
        '''
        Sends a memory data to the storage.

        Args:
            memory (Memory): memory to send.
        '''
        memory_name = memory.get_name()
        logger.info(f"Sending memory [{memory_name}@{self._node_name}]")

        memory_dict = cast(dict[str|bytes, int|float|str], MemoryEncoder.to_dict(memory, jsonify_info=True))
        memory_dict["owner"] = ""
        memory_dict["logical_time"] = str(self._memory_logical_time[memory_name])


        self._client.hset(f"{self._mind_name}:memories:{memory_name}", mapping=memory_dict)
        self._client.publish(f"{self._mind_name}:memories:{memory_name}:update", "")
        
        self._current_time = self._current_time.increment()
        

    def _retrieve_memory(self, memory:Memory) -> None:
        '''
        Retrieves a memory data from the storage.

        Blocks the application, it is advisable to use a separate thread to call the method.

        Args:
            memory (Memory): memory to retrieve data.
        '''
        memory_name = memory.get_name()
        logger.info(f"Retrieving memory [{memory_name}@{self._node_name}]")

        if memory_name in self._waiting_retrieve:
            return
        self._waiting_retrieve.add(memory_name)

        memory_dict = self._client.hgetall(f"{self._mind_name}:memories:{memory_name}")

        if memory_dict["owner"] != "":
            event = threading.Event()
            self._waiting_request_events[memory_name] = event
            self._request_memory(memory_name, memory_dict["owner"])

            if not event.wait(timeout=self._request_timeout):
                logger.warning(f"Request failed [{memory_name}@{memory_dict['owner']} to {self._node_name}]")
                #Request failed
                self._send_memory(memory)
                return 
            
            memory_dict = self._client.hgetall(f"{self._mind_name}:memories:{memory_name}")

        MemoryEncoder.load_memory(memory, memory_dict)
        message_time = LamportTime.from_str(memory_dict["logical_time"])
        self._current_time = LamportTime.synchronize(self._current_time, message_time)

        self._last_update[memory_name] = memory.get_timestamp()
        self._memory_logical_time[memory_name] = message_time

        self._waiting_retrieve.remove(memory_name)

    def _request_memory(self, memory_name:str, owner_name:str) -> None:
        '''
        Requests another node to send its local memory to storage.

        Args:
            memory_name (str): name of the memory to request.
            owner_name (str): node owning the memory.
        '''
        logger.info(f"Requesting memory [{memory_name}@{owner_name} to {self._node_name}]")

        request_addr = f"{self._mind_name}:nodes:{owner_name}:transfer_memory"
        
        request_dict = {"memory_name":memory_name, "node":self._node_name}
        full_request_dict = {"request":request_dict, "logical_time":str(self._current_time)}
        request = json.dumps(full_request_dict)
        self._client.publish(request_addr, request)

    def _handler_notify_transfer(self, message:dict[str,str]) -> None:
        '''
        Handles a message in the notify transfer channel.

        Args:
            message (dict[str,str]): message received in the channel.
        '''
        data = data = json.loads(message["data"])
        if "logical_time" in data:
            message_time = LamportTime.from_str(data["logical_time"])
            self._current_time = LamportTime.synchronize(message_time, self._current_time)

        memory_name = data["memory_name"]
        if memory_name in self._waiting_request_events:
            event = self._waiting_request_events[memory_name]
            event.set()
            del self._waiting_request_events[memory_name]

        
    def _handler_transfer_memory(self, message:dict[str,str]) -> None:
        '''
        Handles a message in the transfer memory channel.

        Args:
            message (dict[str,str]): message received in the channel.
        '''
        data = json.loads(message["data"])
        if "logical_time" in data:
            message_time = LamportTime.from_str(data["logical_time"])
            self._current_time = LamportTime.synchronize(message_time, self._current_time)

        request = data["request"]
        
        memory_name = request["memory_name"]
        requesting_node = request["node"]

        logger.info(f"Transfering memory to server [{memory_name}@{self._node_name}]")

        if memory_name in self._memories:
            memory = self._memories[memory_name]
        else:
            memory = MemoryObject()
            memory.set_name(memory_name)

        self._memory_logical_time[memory_name] = self._current_time
        
        self._send_memory(memory)

        response = {"memory_name":memory_name, "logical_time":str(self._current_time)}
        response_str = json.dumps(response)

        response_addr = f"{self._mind_name}:nodes:{requesting_node}:transfer_done"
        self._client.publish(response_addr, response_str)

    def stop(self):
        self._pubsub_thread.stop()
        self._retrieve_executor.shutdown(cancel_futures=True)
        self._client.close()
        super().stop()

    def __del__(self) -> None:
        self._pubsub_thread.stop()
        self._retrieve_executor.shutdown(cancel_futures=True)
        self._client.close()