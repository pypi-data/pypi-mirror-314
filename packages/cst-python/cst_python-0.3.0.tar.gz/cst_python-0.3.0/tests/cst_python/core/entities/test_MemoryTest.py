import math
import unittest
from typing import Any

from cst_python.core.entities import Memory, MemoryObject, MemoryObserver

class MemorySubclass(Memory):
    def __init__(self) -> None:
        super().__init__()

        self.I = None
        self.evaluation = 0.0
        self.name = ""
        self.timestamp = 10
        self.id = None

    def get_id(self) -> int:
        return self.id

    def set_id(self, memory_id: int) -> None:
        self.id = memory_id
    
    def get_info(self) -> Any:
        return self.I
    
    def set_info(self, value: Any) -> int:
        self.I = value

    def get_evaluation(self) -> float:
        return self.evaluation

    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str) -> None:
        self.name = name

    def set_evaluation(self, evaluation: float) -> None:
        self.evaluation = evaluation
    
    def get_timestamp(self) -> int:
        return self.timestamp
    
    def add_memory_observer(self, observer: MemoryObserver) -> None:
        # TODO copy from CST when implemented 
        pass

    def remove_memory_observer(self, observer: MemoryObserver) -> None:
        # TODO copy from CST when implemented
        pass

class MemoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_memory = MemorySubclass()
        super().setUp()

    def test_get_set_info(self) -> None:
        assert self.test_memory.get_info() is None

        test_value = 100.0
        self.test_memory.set_info(test_value)

        assert math.isclose(test_value, self.test_memory.get_info())

        test_list : list[Memory] = [MemoryObject(), MemoryObject()]
        self.test_memory.set_info(test_list)

        assert test_list == self.test_memory.get_info()
    
    

    def test_get_set_eval(self) -> None:

        test_value = 100.0
        self.test_memory.set_evaluation(test_value)

        assert math.isclose(test_value, self.test_memory.get_evaluation())
    

    def test_get_timestamp(self) -> None:
        assert 10 == self.test_memory.get_timestamp()
    