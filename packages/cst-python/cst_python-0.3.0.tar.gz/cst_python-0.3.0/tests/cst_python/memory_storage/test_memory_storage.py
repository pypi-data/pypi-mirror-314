import functools
import json
import threading
import threading
import time
import types
import unittest
from typing import Any

import redis
from numpy.testing import assert_array_almost_equal

from cst_python import MemoryObject, Mind
from cst_python.memory_storage import MemoryStorageCodelet

sleep_time = 0.75


def set_info(self:MemoryObject, value:Any, start_time:float) -> int:
    self._info = value

    time_time = start_time + time.monotonic()

    self._timestamp = int(time_time*1000)
    self._notify_memory_observers()

    return -1

def patch_memory_object(memory:MemoryObject, start_time:float) -> None:
    set_info_fixedtime = functools.partial(set_info, start_time=start_time)
    memory.set_info = types.MethodType(set_info_fixedtime, memory)

client = redis.Redis(decode_responses=True)
try:
    client.ping()
    redis_reachable = True
except Exception:
    redis_reachable = False

@unittest.skipIf(not redis_reachable, "Redis server not running")
class TestMemoryStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = redis.Redis(decode_responses=True)


    def setUp(self) -> None:
        self.client.flushall()

        self.start_times = [0, 1e3]

        self.mind = Mind()
        self.mind2 = Mind()

    def tearDown(self):
        self.mind.shutdown()
        self.mind2.shutdown()
        
        self.client.flushall()

    def test_patch_memory_object(self) -> None:

        memory1 = MemoryObject()
        memory2 = MemoryObject()

        patch_memory_object(memory1, 0)
        patch_memory_object(memory2, 1e3)

        memory1.set_info(0)
        memory2.set_info(1)
        
        assert memory1.get_info() == 0
        assert memory2.get_info() == 1

        assert (memory2.get_timestamp() - memory1.get_timestamp()) >= 1e6

    def test_node_enter(self) -> None:
        ms_codelet = MemoryStorageCodelet(self.mind)
        ms_codelet.time_step = 50
        self.mind.insert_codelet(ms_codelet)
        self.mind.start()

        time.sleep(sleep_time)

        assert ms_codelet._node_name == "node"
        members = client.smembers("default_mind:nodes")
        assert len(members) == 1
        assert "node" in members

        self.mind2 = Mind()
        ms_codelet2 = MemoryStorageCodelet(self.mind2)
        ms_codelet2.time_step = 50
        self.mind2.insert_codelet(ms_codelet2)
        self.mind2.start()

        time.sleep(sleep_time)

        assert ms_codelet2._node_name == "node1"
        members = client.smembers("default_mind:nodes")
        assert len(members) == 2
        assert "node" in members
        assert "node1" in members

    def test_redis_args(self) -> None:
        redis_args = {"host":"localhost", "port":6379}
        ms_codelet = MemoryStorageCodelet(self.mind, **redis_args)
        ms_codelet.time_step = 50
        self.mind.insert_codelet(ms_codelet)
        self.mind.start()

        time.sleep(sleep_time)

        members = client.smembers("default_mind:nodes")
        assert len(members) == 1
        assert "node" in members

    def test_memory_transfer(self) -> None:
        
        memory1 = self.mind.create_memory_object("Memory1", "INFO")
        patch_memory_object(memory1, self.start_times[0])

        ms_codelet = MemoryStorageCodelet(self.mind)
        ms_codelet.time_step = 50
        self.mind.insert_codelet(ms_codelet)
        
        self.mind.start()

        time.sleep(sleep_time)

        assert self.client.exists("default_mind:memories:Memory1") >= 1

        result = client.hgetall("default_mind:memories:Memory1")
        expected_result = {"name":"Memory1", "evaluation":"0.0", "I":"", "id":"0", "owner":"node", "logical_time":"0"}
        assert result == expected_result

        request = {"request":{"memory_name":"Memory1", "node":"node1"}, "logical_time":"0"}
        request = json.dumps(request)

        self.client.publish("default_mind:nodes:node:transfer_memory", request)

        time.sleep(sleep_time)

        result = client.hgetall("default_mind:memories:Memory1")
        expected_result = {"name":"Memory1", "evaluation":"0.0", "I":'"INFO"', "id":"0", "owner":""}
        del result["logical_time"]
        del result["timestamp"]
        assert result == expected_result


    def test_ms(self) -> None:
        memory1 = self.mind.create_memory_object("Memory1", "")
        patch_memory_object(memory1, self.start_times[0])

        ms_codelet = MemoryStorageCodelet(self.mind)
        ms_codelet.time_step = 50

        self.mind.insert_codelet(ms_codelet)
        self.mind.start()

        assert memory1.get_info() == ""

        memory1.set_info([1,1,1])

        time.sleep(sleep_time)

        self.mind2_memory1 = self.mind2.create_memory_object("Memory1", "")
        patch_memory_object(self.mind2_memory1, self.start_times[1])
        self.mind2_ms_codelet = MemoryStorageCodelet(self.mind2)
        self.mind2_ms_codelet.time_step = 50
        self.mind2.insert_codelet(self.mind2_ms_codelet)
        self.mind2.start()

        assert self.mind2_memory1.get_info() == ""

        time.sleep(sleep_time)

        assert_array_almost_equal(memory1.get_info(), [1,1,1])
        assert_array_almost_equal(self.mind2_memory1.get_info(), [1,1,1])

        result = client.hgetall("default_mind:memories:Memory1")
        expected_result = {"name":"Memory1", "evaluation":"0.0", "I":"[1, 1, 1]", "id":"0", "owner":""}

        assert "logical_time" in result
        assert "timestamp" in result
        del result["logical_time"]
        del result["timestamp"]
        assert result == expected_result

        memory1.set_info("INFO")
        time.sleep(sleep_time)

        assert memory1.get_info() == "INFO"
        assert self.mind2_memory1.get_info() == "INFO"


        self.mind2_memory1.set_info("INFO2")
        time.sleep(sleep_time)

        assert memory1.get_info() == "INFO2"
        assert self.mind2_memory1.get_info() == "INFO2"

        memory1.set_info(1)
        time.sleep(sleep_time)

        assert memory1.get_info() == 1
        assert self.mind2_memory1.get_info() == 1

        memory1.set_info("1")
        time.sleep(sleep_time)


        assert memory1.get_info() == "1"
        assert self.mind2_memory1.get_info() == "1"

        memory1.set_info(True)
        time.sleep(sleep_time)

        assert memory1.get_info() == True
        assert self.mind2_memory1.get_info() == True


        self.mind2_memory1.set_info([1,2,3])
        time.sleep(sleep_time)

        assert_array_almost_equal(memory1.get_info(), [1,2,3])
        assert_array_almost_equal(self.mind2_memory1.get_info(), [1,2,3])

        self.mind.shutdown()
        self.mind2.shutdown()

        assert (self.mind2_memory1.get_timestamp() - memory1.get_timestamp()) >= 9e5

        time.sleep(sleep_time)
        assert threading.active_count() == 1
    