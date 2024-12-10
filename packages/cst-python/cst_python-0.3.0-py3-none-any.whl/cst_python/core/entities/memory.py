import abc
from typing import Any

from cst_python.python import alias
from.memory_observer import MemoryObserver

class Memory(abc.ABC):
    '''
    This class represents the interface for all kinds of memories that exist in
    CST. In order to be recognized as a Memory, an entity must implement this
    interface. Currently, there are to kinds of Memory: MemoryObject and
    MemoryContainer. However, other forms of Memory might come up as CST
    develops.
    '''
    
    #@alias.alias("getI", "get_I")
    @abc.abstractmethod
    def get_info(self) -> Any:
        '''
        Gets the info inside this memory.

        Returns:
            Any: the info in memory.
        '''
        ...
    
    #@alias.alias("setT", "set_I")
    @abc.abstractmethod
    def set_info(self, value:Any) -> int:
        '''
        Sets the info inside this Memory.

        Args:
            value (Any): the updated info to set in memory.

        Returns:
            int: index of the memory inside the container or -1 if not a
                container.
        '''
        ...

    #@alias.alias("getEvaluation")
    @abc.abstractmethod
    def get_evaluation(self) -> float:
        '''
        Gets the evaluation of this memory.

        Returns:
            float: the evaluation of this memory.
        '''
        ...

    #@alias.alias("getName")
    @abc.abstractmethod
    def get_name(self) -> str:
        '''
        Gets the type of this memory.

        Returns:
            str: the type of the memory.
        '''
        ...

    #@alias.alias("setName")
    @abc.abstractmethod
    def set_name(self, name:str) -> None:
        '''
        Sets the name of this memory.

        Args:
            name (str): the value to be set as name.
        '''
        ...

    #@alias.alias("setEvaluation")
    @abc.abstractmethod
    def set_evaluation(self, evaluation:float) -> None:
        '''
        Sets the evaluation of this memory.

        Args:
            evaluation (float): the value to be set as evaluation.
        '''
        ...

    #@alias.alias("getTimestamp")
    @abc.abstractmethod
    def get_timestamp(self) -> int:
        '''
        Gets the timestamp of this Memory.

        Returns:
            int: the timestamp of this Memory.
        '''
        ...

    #@alias.alias("addMemoryObserver")
    @abc.abstractmethod
    def add_memory_observer(self, observer:MemoryObserver) -> None:
        '''
        Add a memory observer to its list.

        Args:
            observer (MemoryObserver): MemoryObserver to be added.
        '''
        ...

    #@alias.alias("removeMemoryObserver")
    @abc.abstractmethod
    def remove_memory_observer(self, observer:MemoryObserver) -> None:
        '''
        Remove a memory observer from its list.

        Args:
            observer (MemoryObserver): MemoryObserver to be removed.
        '''
        ...

    #@alias.alias("getId")
    @abc.abstractmethod
    def get_id(self) -> int:
        '''
        Gets the id of the Memory.

        Returns:
            int: the id of the Memory.
        '''
        ...

    #@alias.alias("setId")
    @abc.abstractmethod
    def set_id(self, memory_id:int) -> None:
        '''
        Sets the id of the Memory.

        Args:
            memory_id (int): the id of the Memory to set.
        '''
        ...

    

    def compare_name(self, other_name:str) -> bool:
        '''
        Compares tha name of this memory with another.

        Comparation is case insensitive.

        Args:
            other_name (str): name of the other memory.

        Returns:
            bool: True if is the same name.
        '''
        if self.get_name() is None:
            return False
        
        return self.get_name().lower() == other_name.lower()
    