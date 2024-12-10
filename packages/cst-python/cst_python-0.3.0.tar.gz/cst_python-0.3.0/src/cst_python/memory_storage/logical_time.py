from __future__ import annotations

import abc
import functools


class LogicalTime(abc.ABC):
    '''
    A logical time for distributed communication.
    '''

    @abc.abstractmethod
    def increment(self) -> "LogicalTime":
        '''
        Returns a time with the self time incremented by one. 

        Returns:
            LogicalTime: incremented time.
        '''
        ...


    @abc.abstractmethod
    def __str__(self) -> str:
        ...
    
    @classmethod
    @abc.abstractmethod
    def from_str(cls, string:str) -> "LogicalTime":
        '''
        Creates a instance from a string.

        Args:
            string (str): String to create time, 
                generated with str(LogicalTime).

        Returns:
            LogicalTime: Created time.
        '''
        ...

    @classmethod
    @abc.abstractmethod
    def synchronize(cls, time0:"LogicalTime", time1:"LogicalTime") -> "LogicalTime":
        '''
        Compares two times, and return the current time.

        Args:
            time0 (LogicalTime): first time to compare.
            time1 (LogicalTime): second time to compare.

        Returns:
            LogicalTime: current time.
        '''
        ...

    @abc.abstractmethod
    def __eq__(self, other) -> bool:
        ...
    
    @abc.abstractmethod
    def __lt__(self, other) -> bool:
        ...

    @abc.abstractmethod
    def __le__(self, other) -> bool:
        ...

    @abc.abstractmethod
    def __gt__(self, other) -> bool:
        ...

    @abc.abstractmethod
    def __ge__(self, other) -> bool:
        ...


@functools.total_ordering
class LamportTime(LogicalTime):
    '''
    Logical time implementation using Lamport times.
    '''

    #Methods that total_ordering will overwrite
    __le__ = object.__lt__ # type: ignore
    __gt__ = object.__gt__ # type: ignore
    __ge__ = object.__ge__ # type: ignore


    def __init__(self, initial_time:int=0):
        '''
        LamportTime initializer.

        Args:
            initial_time (int, optional): time to start the clock. Defaults to 0.
        '''
        super().__init__()
        self._time = initial_time

    def increment(self) -> "LamportTime":
        return LamportTime(initial_time=self._time+1)

    def __eq__(self, other) -> bool:
        return self._time == other._time

    def __lt__(self, other) -> bool:
        return self._time < other._time   

    def __str__(self) -> str:
        return str(self._time)

    @classmethod
    def from_str(cls, string:str) -> "LamportTime":
        return LamportTime(int(string))

    @classmethod
    def synchronize(cls, time0, time1) -> "LamportTime":
        if not (isinstance(time0, LamportTime) and isinstance(time1, LamportTime)):
            raise ValueError("LamportTime can only synchonize LamportTime instances")
        
        new_time = 0
        if time0 < time1:
            new_time = time1._time
        else:
            new_time = time0._time

        new_time += 1

        return LamportTime(new_time)