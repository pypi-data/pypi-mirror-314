import abc

from cst_python.python import alias

class MemoryObserver(abc.ABC):    
    #@alias.alias("notifyCodelet")
    @abc.abstractmethod
    def notify_codelet(self):
        ...