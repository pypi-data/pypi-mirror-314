import time
from typing import List, Optional, Any

from cst_python.python import alias
from .memory import Memory
from .memory_container import MemoryContainer
from .rest_memory_object import RESTMemoryObject
from .rest_memory_container import RESTMemoryContainer
from .memory_object import MemoryObject

#TODO createMemoryContainer, REST methods

class RawMemory:
    '''
    The Raw Memory contains all memories in the system.
    '''
    
    _last_id = 0

    def __init__(self) -> None:
        '''
        Creates a Raw Memory.
        '''
        self._all_memories : List[Memory] = [] #Should be a set?
    
    #@alias.alias("getAllMemoryObjects", "get_all_memory_objects")
    @property
    def all_memories(self) -> List[Memory]:
        '''
        List of all memories in the system.
        '''
        return self._all_memories
    
    #@alias.alias("setAllMemoryObjects", "set_all_memory_objects")
    @all_memories.setter
    def all_memories(self, value:List[Memory]) -> None:
        self._all_memories = value
        
        for m in self._all_memories:
            if m.get_id() is None:
                m.set_id(self._last_id)
                self._last_id += 1
    
    #@alias.alias("getAllOfType")
    def get_all_of_type(self, type:str) -> List[Memory]:
        '''
        Returns a list of all memories in raw memory of a given type

        Args:
            type (str): type of memory

        Returns:
            List[Memory]: list of Ms of a given type
        '''
        list_of_type = []

        for m in self._all_memories:
            if m.compare_name(type):
                list_of_type.append(m)

        return list_of_type
    
    #@alias.alias("printContent")
    def print_content(self) -> None:
        '''
        Print Raw Memory contents.
        '''
        for m in self._all_memories:
            print(m)

    #@alias.alias("addMemoryObject", "add_memory_object", "addMemory")
    def add_memory(self, m:Memory) -> None:
        '''
        Adds a new Memory to the Raw Memory.

        Args:
            m (Memory): memory to be added.
        '''
        self._all_memories.append(m)
        m.set_id(self._last_id)
        self._last_id += 1

    #@alias.alias("createMemoryContainer")
    def create_memory_container(self, name:str) -> MemoryContainer:
        '''
        Creates a memory container of the type passed.

        Args:
            name (str): the type of the memory container passed.

        Raises:
            NotImplementedError: method is not implemented.

        Returns:
            MemoryContainer: the memory container created.
        '''
        raise NotImplementedError()
    
    #@alias.alias("createRESTMemoryObject")
    def create_rest_memory_object(self, name:str, port:int, hostname:Optional[str]=None) -> RESTMemoryObject:
        '''
        Creates a new RestMemory and adds it to the Raw Memory, using provided
        name, hostname and port .

        Args:
            name (str): memory object type.
            port (int): the port of the REST server
            hostname (Optional[str], optional): the hostname of the REST server. If None, 
        uses 'localhost'. Defaults to None.

        Raises:
            NotImplementedError: method is not implemented.

        Returns:
            RESTMemoryObject: created MemoryObject.
        '''
        raise NotImplementedError()
    
    #@alias.alias("createRESTMemoryContainer")
    def create_rest_memory_container(self, name:str, port:int, hostname:Optional[str]=None) -> RESTMemoryContainer:
        '''
        Creates a new RestMemory and adds it to the Raw Memory, using provided
        name, hostname and port .

        Args:
            name (str): memory object type.
            port (int): the port of the REST server
            hostname (Optional[str], optional): the hostname of the REST server. If None, 
        uses 'localhost'. Defaults to None.

        Raises:
            NotImplementedError: method is not implemented.

        Returns:
            RESTMemoryContainer: created MemoryObject.
        '''
        raise NotImplementedError()
    
    #@alias.alias("createMemoryObject")
    def create_memory_object(self, name:str, info:Optional[Any]=None) -> MemoryObject:
        '''
        Creates a new MemoryObject and adds it to the Raw Memory.

        Args:
            name (str): memory object type.
            info (Optional[Any], optional): memory object info. Defaults to None.

        Returns:
            MemoryObject: created MemoryObject.
        '''
        if info is None:
            info = ""
        
        mo = MemoryObject()

        mo.set_info(info)
        mo.set_evaluation(0.0)
        mo.set_name(name)

        self.add_memory(mo)
        return mo
    
    #@alias.alias("destroyMemoryObject", "destroy_memory_object")
    def destroy_memory(self, m:Memory):
        '''
        Destroys a given memory from raw memory

        Args:
            m (Memory): the memory to destroy.
        '''
        self._all_memories.remove(m)

    #@alias.alias("size")
    def __len__(self) -> int:
        '''
        Gets the size of the raw memory.

        Returns:
            int: size of Raw Memory.
        '''
        return len(self._all_memories)
    
    #@alias.alias("shutDown", "shut_down")
    def shutdown(self) -> None:
        '''
        Removes all memory objects from RawMemory.
        '''
        self._all_memories = []