from typing import List, Dict, Optional, Any, Union

from cst_python.python import alias
from .code_rack import CodeRack
from .raw_memory import RawMemory
from .rest_memory_object import RESTMemoryObject
from .rest_memory_container import RESTMemoryContainer
from .memory_object import MemoryObject
from .codelet import Codelet
from .memory import Memory
from .memory_container import MemoryContainer

class Mind:
    '''
    This class represents the Mind of the agent, wrapping all the CST's core
    entities.
    '''
    def __init__(self) -> None:
        '''
        Creates the Mind.
        '''
        self._code_rack = CodeRack()
        self._raw_memory = RawMemory()
        self._codelet_groups : Dict[str, List[Codelet]] = dict()
        self._memory_groups : Dict[str, List[Memory]] = dict()

    #@alias.alias("getCodeRack", "get_code_rack")
    @property
    def code_rack(self) -> CodeRack:
        return self._code_rack

    #@alias.alias("getRawMemory", "get_raw_memory")
    @property
    def raw_memory(self) -> RawMemory:
        return self._raw_memory
    
    #@alias.alias("getCodeletGroups")
    @property
    def codelet_groups(self) -> Dict[str, List[Codelet]]:
        return self._codelet_groups

    #@alias.alias("getMemoryGroups")
    @property
    def memory_groups(self) -> Dict[str, List[Memory]]:
        return self._memory_groups

    #@alias.alias("createCodeletGroup")
    def create_codelet_group(self, group_name:str) -> None:
        '''
        Creates a Codelet Group.

        Args:
            group_name (str): The Group name.
        '''
        self._codelet_groups[group_name] = []

    #@alias.alias("createMemoryGroup")
    def create_memory_group(self, group_name:str) -> None:
        '''
        Creates a Memory Group.

        Args:
            group_name (str): The Group name.
        '''
        self._memory_groups[group_name] = []

    #@alias.alias("getCodeletGroupsNumber")
    def get_codelet_groups_number(self) -> int:
        '''
        Returns the number of registered codelet groups

        Returns:
            int: the number of registered groups
        '''
        return len(self._memory_groups)

    #@alias.alias("getMemoryGroupsNumber")
    def get_memory_groups_number(self) -> int:
        '''
        Returns the number of registered memory groups

        Returns:
            int: the number of registered groups
        '''

        return len(self._memory_groups)
    
    #@alias.alias("createMemoryContainer")
    def create_memory_container(self, name:str) -> Optional[MemoryContainer]:
        '''
        Creates a Memory Container inside the Mind of a given type.

        Args:
            name (str): the type of the Memory Container to be created inside the
	            Mind.

        Returns:
            Optional[MemoryContainer]: the Memory Container created.
        '''
        mc = None

        if self._raw_memory is not None:
            mc = self._raw_memory.create_memory_container(name)

        return mc

    #@alias.alias("createRESTMemoryObject")
    def create_rest_memory_object(self, name:str, 
                                  port:int, 
                                  hostname:Optional[str]=None) -> Optional[RESTMemoryObject]:
        '''
        Creates a new MemoryObject and adds it to the Raw Memory, using provided
	    info and type.

        Args:
            name (str): memory object name.
            port (int): port of the REST server
            hostname (Optional[str], optional): hostname of the REST server. If is None,
                uses 'localhost'. Defaults to None.

        Returns:
            Optional[RESTMemoryObject]: created MemoryObject
        '''

        if hostname is None:
            hostname = "localhost"

        mo = None
        
        if self._raw_memory is not None:
            mo = self._raw_memory.create_rest_memory_object(name, port, hostname)

        return mo

    #@alias.alias("createRESTMemoryContainer")
    def create_rest_memory_container(self, name:str, 
                                     port:int, 
                                     hostname:Optional[str]=None) -> Optional[RESTMemoryContainer]:
        '''
        Creates a new MemoryObject and adds it to the Raw Memory, using provided
	    info and type.

        Args:
            name (str): memory object name.
            port (int): port of the REST server
            hostname (Optional[str], optional): hostname of the REST server. If is None,
                uses 'localhost'. Defaults to None.

        Returns:
            Optional[RESTMemoryContainer]: created MemoryObject
        '''
        if hostname is None:
            hostname = "localhost"

        mc = None
        
        if self._raw_memory is not None:
            mc = self._raw_memory.create_rest_memory_container(name, port, hostname)

        return mc
    

    #@alias.alias("createMemoryObject")
    def create_memory_object(self, name:str, info:Optional[Any]=None) -> Optional[MemoryObject]:
        '''
        Creates a new MemoryObject and adds it to the Raw Memory, using provided
	    type.

        Args:
            name (str): memory object type.
            info (Optional[Any], optional): memory object info. Defaults to None.

        Returns:
            Optional[MemoryObject]: created MemoryObject.
        '''
        mo = None

        if self._raw_memory is not None:
            mo = self._raw_memory.create_memory_object(name, info)

        return mo
    
    #@alias.alias("insertCodelet")
    def insert_codelet(self, co:Codelet, group_name:Optional[str]=None) -> Codelet:
        '''
        Inserts the Codelet passed in the Mind's CodeRack.

        Args:
            co (Codelet): the Codelet passed
            group_name (Optional[str], optional): the Codelet group name. Defaults to None.

        Returns:
            Codelet: the Codelet.
        '''
        if self._code_rack is not None:
            self._code_rack.add_codelet(co)

        if group_name is not None:
            self.register_codelet(co, group_name)

        return co
    
    #@alias.alias("registerCodelet")
    def register_codelet(self, co:Codelet, group_name:str) -> None:
        '''
        Register a Codelet within a group.

        Args:
            co (Codelet): the Codelet.
            group_name (str): the group name.
        '''
        if group_name in self._codelet_groups:
            group_list = self._codelet_groups[group_name]
            group_list.append(co)
    
    #@alias.alias("registerMemory")
    def register_memory(self, memory:Union[Memory,str], group_name:str) -> None:
        '''
        Register a Memory within a group

        Args:
            memory (Union[Memory,str]): the Memory or the memory name.
            group_name (str): the group name
        '''

        if group_name in self._memory_groups:
            to_register = []
            
            if isinstance(memory, str) and self._raw_memory is not None:
                to_register += self._raw_memory.get_all_of_type(memory)
            else:
                to_register.append(memory)

            self._memory_groups[group_name] += to_register
    
    #@alias.alias("getCodeletGroupList")
    def get_codelet_group_list(self, group_name:str) -> List[Codelet]:
        '''
        Get a list of all Codelets belonging to a group

        Args:
            group_name (str): the group name to which the Codelets belong

        Returns:
            List[Codelet]: A list of all codeletGroups belonging to the group indicated by groupName
        '''
        return self._codelet_groups[group_name]
    
    #@alias.alias("getMemoryGroupList")
    def get_memory_group_list(self, group_name:str) -> List[Memory]:
        '''
        Get a list of all Memories belonging to a group

        Args:
            group_name (str): the group name to which the Memory belong

        Returns:
            List[Memory]: A list of all memoryGroups belonging to the group indicated by groupName
        '''
        return self._memory_groups[group_name]
    
    def start(self) -> None:
        '''
        Starts all codeletGroups in coderack.
        '''
        if self._code_rack is not None:
            self._code_rack.start()

    #@alias.alias("shutDown", "shut_down")
    def shutdown(self) -> None:
        '''
        Stops codeletGroups thread.
        '''
        if self._code_rack is not None:
            self._code_rack.shutdow()