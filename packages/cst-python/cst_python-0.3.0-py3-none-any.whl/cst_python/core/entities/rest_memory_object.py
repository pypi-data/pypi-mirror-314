from typing import Optional

from .memory_object import MemoryObject

class RESTMemoryObject(MemoryObject):
    
    def __init__(self, port: int, 
                 hostname : Optional[str] = None, 
                 pretty:Optional[bool] = None,
                 origin:Optional[str] = None,
                 n_refresh:Optional[float] = None):
        super().__init__()

        if hostname is None:
            hostname = "localhost"
        if pretty is None:
            pretty = False
        if origin is None:
            origin = "*"
        if n_refresh is None:
            n_refresh = 0.0


        self._refresh : float = n_refresh
        self._last_access : float = 0
        self._last_message : str = ""

        raise NotImplementedError()