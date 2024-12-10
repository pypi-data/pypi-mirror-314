from __future__ import annotations

import abc
import traceback
import threading
import time
from typing import List, Optional

from cst_python.python import alias
from .memory import Memory
from .memory_buffer import MemoryBuffer
from .memory_observer import MemoryObserver

#TODO: Profile, Broadcast, impending access, correct exception types

#@alias.aliased
class Codelet(MemoryObserver): #(abc.ABC) is not necessary
    '''
    The **Codelet** class, together with the **MemoryObject**
    class and the **Mind** class is one of the most important classes
    in the CST toolkit. According to the Baars-Franklin architecture,
    consciousness is the emergence of a serial stream on top of a parallel set of
    interacting devices. In the Baars-Franklin architectures, such devices are
    called "codelets", which are small pieces of code specialized in performing
    simple tasks. In a CST-built cognitive architecture, everything is either a
    **Codelet** or a **MemoryObject**. Codelets are used to
    implement every kind of processing in the architecture.
    
    Codelets have two kinds of inputs: standard inputs and broadcast inputs.
    Standard inputs are used to convey access to MemoryObjects. Broadcast inputs
    come from consciousness, and can also be used. Nevertheless, Standard inputs
    are usually fixed (but can be changed through learning mechanisms), and
    Broadcast inputs change all the time, due to the consciousness mechanism.
    Codelets also have outputs. Outputs are used for the Codelets to write or
    generate new MemoryObjects. Codelets also have an Activation level, which can
    be used in some situations.
    '''
    _last_id = 0

    def __init__(self) -> None:
        '''
        Codelet's init.
        '''
        self._threshold = 0.0
        self._inputs : List[Memory] = []
        self._outputs : List[Memory] = []
        self._broadcast : List[Memory] = []
        self._loop = True
        self._is_memory_observer = False
        self._time_step = 300
        self._enabled = True
        self._enable_count = 0
        self._name = threading.current_thread().name+"|"+type(self).__name__+str(Codelet._last_id)
        self._last_start_time = 0.0
        self._lock = threading.RLock()
        self._activation = 0.0
        #self._timer = 
        self._is_profiling = False
        self._thread : threading.Thread = threading.Thread(target=self.run, daemon=True)
        self._codelet_profiler = None
        self._additional_wait = 0.0

        Codelet._last_id += 1


    
    #@alias.alias("should_loop", "shouldLoop", "is_loop", "isLoop")
    @property
    def loop(self) -> bool:
        '''
        Defines if proc() should be automatically called in a loop
        '''

        return self._loop

    #@alias.alias("set_loop", "setLoop")
    @loop.setter
    def loop(self, value:bool) -> None:
        self._loop = value

    #@alias.alias("get_enabled", "getEnabled")
    @property
    def enabled(self) -> bool:
        '''
        A codelet is a priori enabled to run its proc(). However, if it tries to
        read from a given output and fails, it becomes not able to do so.
        '''

        return self._enabled
    
    #@alias.alias("set_enabled", "setEnabled")
    @enabled.setter
    def enabled(self, value:bool) -> None:
        self._enabled = value

        if self._enabled:
            self._enable_count = 0

    #@alias.alias("get_name", "getName")
    @property
    def name(self) -> str:
        '''
        Gives this codelet a name, mainly for debugging purposes
        '''

        return self._name

    #@alias.alias("set_name", "setName")
    @name.setter
    def name(self, value:str) -> None:
        self._name = value

    #@alias.alias("get_activation", "getActivation")
    @property
    def activation(self) -> float:
        '''
        Activation level of the Codelet. Ranges from 0.0 to 1.0.
        '''

        return self._activation
    
    #@alias.alias("set_activation", "setActivation")
    @activation.setter
    def activation(self, value:float):
        if value > 1.0 or value < 0.0:
            if value > 1.0:
                self._activation = 1.0
            else:
                self._activation = 0.0

            raise ValueError(f"Codelet activation must be in (0.0 , 1.0) \
(value {value} is not allowed).")
        
        self._activation = value

    #@alias.alias("get_inputs", "getInputs")
    @property
    def inputs(self) -> List[Memory]:
        '''
        Input memories, the ones that are read.
        '''

        return self._inputs
    
    #@alias.alias("set_inputs", "setInputs")
    @inputs.setter
    def inputs(self, value:List[Memory]):
        self._inputs = value

    #@alias.alias("get_outputs", "getOutputs")
    @property
    def outputs(self) -> List[Memory]:
        '''
        Output memories, the ones that are written.
        '''
        
        return self._outputs

    #@alias.alias("set_outputs", "setOutputs")
    @outputs.setter
    def outputs(self, value:List[Memory]):
        self._outputs = value

    #@alias.alias("get_threshold", "getThreshold")
    @property
    def threshold(self) -> float:
        '''
        Threshold of the codelet, which is used to decide if it runs or not. If
	    activation is equal or greater than activation, codelet runs
	    proc(). Ranges from 0.0 to 1.0.
        '''
        
        return self._threshold

    #@alias.alias("set_threshold", "setThreshold")
    @threshold.setter
    def threshold(self, value:float):
        if value > 1.0 or value < 0.0:
            if value > 1.0:
                self._threshold = 1.0
            else:
                self._threshold = 0.0

            raise ValueError(f"Codelet threshold must be in (0.0 , 1.0) \
(value {value} is not allowed).")
        
        self._threshold = value

    #@alias.alias("get_time_step", "getTime_step")
    @property
    def time_step(self) -> int:
        '''
        If the proc() method is set to be called automatically in a loop, this
	    variable stores the time step for such a loop. A timeStep of value 0
	    means that the proc() method should be called continuously, without
	    interval.
        '''

        return self._time_step

    #@alias.alias("set_time_step", "setTime_step")
    @time_step.setter
    def time_step(self, value:int):
        
        self._time_step = value

    #@alias.alias("get_broadcast", "getBroadcast")
    #Problem: get_broadcast method overload
    @property
    def broadcast(self) -> List[Memory]:
        '''
        Input memories, the ones that were broadcasted.
        '''
        
        return self._broadcast

    #@alias.alias("set_broadcast", "setBroadcast")
    @broadcast.setter
    def broadcast(self, value:List[Memory]) -> None:
        self._broadcast = value

    #@alias.alias("IsProfiling")
    @property
    def profiling(self) -> bool:
        '''
        Option for profiling execution times.
        '''
        
        return self._is_profiling

    #@alias.alias("set_profiling", "setProfiling")
    @profiling.setter
    def profiling(self, value:bool):
        if value is True:
            raise NotImplementedError("Profiling is not implemented")

        self._is_profiling = value

    @property
    def is_memory_observer(self) -> bool:
        '''
        Defines if codelet is a memory observer (runs when memory input changes).
        '''
        
        return self._is_memory_observer
    
    @is_memory_observer.setter
    def is_memory_observer(self, value) -> None:
        self._is_memory_observer = value

    ##########################################################################


    #@alias.alias("accessMemoryObjects")
    @abc.abstractmethod
    def access_memory_objects(self) -> None:
        '''
        This method is used in every Codelet to capture input, broadcast and
	    output MemoryObjects which shall be used in the proc() method. This
	    abstract method must be implemented by the user. Here, the user must get
	    the inputs and outputs it needs to perform proc.
        '''
        ...
    
    #@alias.alias("calculateActivation")
    @abc.abstractmethod
    def calculate_activation(self) -> None:
        '''
        This abstract method must be implemented by the user. Here, the user must
        calculate the activation of the codelet before it does what it is
        supposed to do in proc().
        '''
        ...

    @abc.abstractmethod
    def proc(self) -> None:
        '''
        Main Codelet function, to be implemented in each subclass.
        '''
        ...

    def run(self) -> None:
        '''
        When first activated, the thread containing this codelet runs the proc()
        method.
        '''

        try:
            self._scheduled_run()
        except Exception as e:
            traceback.print_exception(e)

    def start(self) -> None:
        '''
        Starts this codelet execution.
        '''
        self._thread.start()
        #thread.join(0.0)

        

    def stop(self):
        '''
        Tells this codelet to stop looping (stops running).
        '''
        self.loop = False

        if self._thread.is_alive():
            self._thread.join(0.0)

    #@alias.alias("impendingAccess")
    def impending_acess(self, accessing:Codelet) -> bool:
        '''
        Safe access to other Codelets through reentrant locks.

        Args:
            accessing (Codelet): the Codelet accessing.

        Raises:
            NotImplementedError: this method is not implemented yet.

        Returns:
            bool: True if is impeding access.
        '''
        raise NotImplementedError()

    #@alias.alias("impendingAccessBuffer")
    def impending_access_buffer(self, accessing:MemoryBuffer) -> bool:
        '''
        Safe access to MemoryBuffers through reentrant locks.

        Args:
            accessing (MemoryBuffer): the Memory Buffer accessing.

        Raises:
            NotImplementedError: this method is not implemented yet.

        Returns:
            bool: True if is impending access.
        '''
        raise NotImplementedError()
    
    #@alias.alias("addInput")
    def add_input(self, memory:Memory) -> None:
        '''
        Add one memory to the input list.

        Args:
            memory (Memory): one input to set.
        '''
        if self._is_memory_observer:
            memory.add_memory_observer(self)
        
        self._inputs.append(memory)

    #@alias.alias("addInputs")
    def add_inputs(self, memories:List[Memory]) -> None:
        '''
        Add a list of memories to the input list.

        Args:
            memories (List[Memory]): a list of inputs.
        '''
        if self._is_memory_observer:
            for memory in memories:
                memory.add_memory_observer(self)

        self._inputs += memories

    #@alias.alias("addOutput")
    def add_output(self, memory:Memory) -> None:
        '''
        Add a memory to the output list.

        Args:
            memory (Memory): one output to set.
        '''
        self._outputs.append(memory)

    #@alias.alias("removesOutput")
    def removes_output(self, memory:Memory) -> None:
        '''
        Removes a given memory from the output list.

        Args:
            memory (Memory): the memory to be removed from output.
        '''
        self._outputs.remove(memory)

    #@alias.alias("removesInput")
    def removes_input(self, memory:Memory) -> None:
        '''
        Removes a given memory from the input list.

        Args:
            memory (Memory): the memory to be removed from input.
        '''
        self._inputs.remove(memory)

    #@alias.alias("removeFromOutput")
    def remove_from_output(self, memories:List[Memory]) -> None:
        '''
        Removes a given memory list from the output list.

        Args:
            memories (List[Memory]): the list of memories to be removed from output.
        '''
        self._outputs = [m for m in self._outputs if m not in memories]

    #@alias.alias("removeFromInput")
    def remove_from_input(self, memories:List[Memory]) -> None:
        '''
        Removes a given list of memories from the input list.

        Args:
            memories (List[Memory]): the list of memories to be removed from input.
        '''
        self._inputs = [m for m in self._inputs if m not in memories]

    #@alias.alias("addOutputs")
    def add_outputs(self, memories:List[Memory]) -> None:
        '''
        Adds a list of memories to the output list.

        Args:
            memories (List[Memory]): the list of memories to be added to the output.
        '''
        if self._is_memory_observer:
            for memory in memories:
                memory.add_memory_observer(self)

        self._outputs += memories

    #@alias.alias("getOutputsOfType")
    def get_outputs_of_type(self, type:str) -> List[Memory]:
        '''
        Gets a list of output memories of a certain type.

        Args:
            type (str): the type of memories to be fetched from the output.

        Returns:
            List[Memory]: the list of all memory objects in output of a given type.
        '''
        outputs_of_type = []

        if self._outputs is not None:
            for m in self._outputs:
                if m.compare_name(type):
                    outputs_of_type.append(m)

        return outputs_of_type

    #@alias.alias("getInputsOfType")
    def get_inputs_of_type(self, type:str) -> List[Memory]:
        '''
        Gets a list of input memories of a certain type.

        Args:
            type (str): the type of memories to be retrieved.

        Returns:
            List[Memory]: the list of memory objects in input of a given type.
        '''
        inputs_of_type = []

        if self._inputs is not None:
            for m in self._inputs:
                if m.compare_name(type):
                    inputs_of_type.append(m)

        return inputs_of_type

    #@alias.alias("addBroadcast")
    def add_broadcast(self, memory:Memory) -> None:
        '''
        Adds a memory to the broadcast list.

        Args:
            memory (Memory): one broadcast input to set.
        '''
        if self._is_memory_observer:
            memory.add_memory_observer(self)
        
        self._broadcast.append(memory)

    #@alias.alias("addBroadcasts")
    def add_broadcasts(self, memories:List[Memory]) -> None:
        '''
        Adds a list of memories to the broadcast input list.

        Args:
            memories (List[Memory]): one input to set.
        '''
        if self._is_memory_observer:
            for memory in memories:
                memory.add_memory_observer(self)

        self._broadcast += memories


    #@alias.alias("getThreadName")
    def get_thread_name(self) -> str:
        '''
        Gets the codelet's thread name, for debugging purposes.

        Returns:
            str: The name of the thread running this Codelet.
        '''
        return threading.current_thread().name
    
    #@alias.alias("to_string", "toString")
    def __str__(self) -> str:
        max_len = 10

        result = f"Codelet [activation={self._activation}, name={self._name}, "

        if self._broadcast is not None:
            result += "broadcast="
            result += str(self._broadcast[:min(len(self._broadcast), max_len)])
            result += ", "

        if self._inputs is not None:
            result += "inputs="
            result += str(self._inputs[:min(len(self.inputs), max_len)])
            result += ", "

        if self._outputs is not None:
            result += "outputs="
            result += str(self._outputs[:min(len(self._outputs), max_len)])
        
        result += "]"

        return result
    
    def _get_memory(self, search_list:List[Memory], type:Optional[str]=None, 
                    index:Optional[int]=None, name:Optional[str]=None) -> Memory|None:
        '''
        This method returns an memory from a list. If it couldn't
        find the given M, it sets this codelet as not able to perform proc(), and
        keeps trying to find it.

        Can search by the memory's name, or type and index.

        Args:
            search_list (List[Memory]): list to search memories.
            type (Optional[str], optional): type of memory it needs. If None, searches by the name. Defaults to None.
            index (Optional[int], optional): position of memory in the sublist. If None, searches by the name. Defaults to None.
            name (Optional[str], optional): the name of the memory being searched. If None, searches by the type and index. Defaults to None.

        Returns:
            Memory|None: the memory searched or None if not found.
        '''

        found_MO = None

        if type is not None and index is not None:
            list_MO :List[Memory] = []

            if search_list is not None:
                for m in search_list:
                    if m.compare_name(type):
                        list_MO.append(m)

            if len(list_MO) >= index+1:
                found_MO = list_MO[index]        

        elif name is not None:
            for m in search_list:
                if m.compare_name(name):
                    found_MO = m
                    break

        if found_MO is None:
            self._enabled = False
            self._enable_count += 1
        else:
            self.enabled = True

        return found_MO

    #@alias.alias("getInput")
    def get_input(self, type:Optional[str]=None, index:Optional[int]=None, name:Optional[str]=None) -> Memory|None:
        '''
        This method returns an input memory from its input list. If it couldn't
	    find the given M, it sets this codelet as not able to perform proc(), and
	    keeps trying to find it.

        Args:
            type (Optional[str], optional): type of memory it needs. If None, searches by the name. Defaults to None.
            index (Optional[int], optional): position of memory in the sublist. If None, searches by the name. Defaults to None.
            name (Optional[str], optional): the name of the memory being searched. If None, searches by the type and index. Defaults to None.

        Returns:
            Memory|None: the memory searched or None if not found.
        '''
        return self._get_memory(self._inputs, type, index, name)

    #@alias.alias("getOutput")
    def get_output(self, type:Optional[str]=None, index:Optional[int]=None, name:Optional[str]=None) -> Memory|None:
        '''
        This method returns an output memory from its output list. If it couldn't
	    find the given M, it sets this codelet as not able to perform proc(), and
	    keeps trying to find it.

        Args:
            type (Optional[str], optional): type of memory it needs. If None, searches by the name. Defaults to None.
            index (Optional[int], optional): position of memory in the sublist. If None, searches by the name. Defaults to None.
            name (Optional[str], optional): the name of the memory being searched. If None, searches by the type and index. Defaults to None.

        Returns:
            Memory|None: the memory searched or None if not found.
        '''
        return self._get_memory(self._outputs, type, index, name)

    #@alias.alias("getBroadcast")
    def get_broadcast(self, type:Optional[str]=None, index:Optional[int]=None, name:Optional[str]=None) -> Memory|None:
        '''
        This method returns an broadcast memory from its broadcast list. If it couldn't
	    find the given M, it sets this codelet as not able to perform proc(), and
	    keeps trying to find it.

        Args:
            type (Optional[str], optional): type of memory it needs. If None, searches by the name. Defaults to None.
            index (Optional[int], optional): position of memory in the sublist. If None, searches by the name. Defaults to None.
            name (Optional[str], optional): the name of the memory being searched. If None, searches by the type and index. Defaults to None.

        Returns:
            Memory|None: the memory searched or None if not found.
        '''
        return self._get_memory(self._broadcast, type, index, name)

    
    #@alias.alias("setPublishSubscribe")
    def set_publish_subscribe(self, enable:bool) -> None:
        '''
        Defines if codelet runs in publish-subscribe mode, executing when any input changes.

        Args:
            enable (bool): True if should run in publish-subscribe mode.
        '''
        if enable:
            self.is_memory_observer = True

            for m in self._inputs:
                m.add_memory_observer(self)

        else:
            for m in self._inputs:
                m.remove_memory_observer(self)

            self.is_memory_observer = False

            try:
                self._additional_wait += 300
            except Exception:
                pass

            self.run()


    #@alias.alias("setCodeletProfiler")
    def set_codelet_profiler(self, *args, **kargs) -> None:
        '''
        Sets Codelet Profiler

        Raises:
            NotImplementedError: this method is not implemented yet.
        '''
        raise NotImplementedError()
    

    #@alias.alias("raiseException")
    def _raise_exception(self) -> None:
        raise RuntimeError(f"This codelet could not find a memory object it needs: {self.name}")

    #@alias.alias("notifyCodelet")
    def notify_codelet(self) -> None:
        '''
        Runs when codelet is a memory observer and memory input changes
        '''
        try:
            if self._is_profiling:
                start_time = time.time()
            
            self.access_memory_objects()

            if self._enable_count == 0:
                self.calculate_activation()

                if self.activation >= self.threshold:
                    self.proc()
            else:
                self._raise_exception()

        except Exception as e:
            traceback.print_exception(e)
            #TODO Logging
        
        finally:
            if self._codelet_profiler is not None:
                self._codelet_profiler.profile(self)
            
            if self._is_profiling:
                end_time = time.time()
                duration = (end_time-start_time)

                #TODO profiling


    def _scheduled_run(self):
        run = True

        while run:
            run = False

            start_time = 0.0
            end_time = 0.0
            duration = 0.0

            try:
                if not self._is_memory_observer:
                    self.access_memory_objects()
                
                if self._enable_count == 0:
                    if not self._is_memory_observer:
                        self.calculate_activation()

                        if self._activation >= self._threshold:
                            self.proc()

                else:
                    self._raise_exception()

            
            except Exception as e:
                print(traceback.format_exc())
                #logging
                pass

            finally:
                if not self._is_memory_observer and self._loop:
                    run = True
                
                #Profiling

            if run:
                #Not right, must wait anytime
                time_to_sleep = self._additional_wait + self._time_step
                time_to_sleep /= 1000 #ms to s
                time.sleep(time_to_sleep)