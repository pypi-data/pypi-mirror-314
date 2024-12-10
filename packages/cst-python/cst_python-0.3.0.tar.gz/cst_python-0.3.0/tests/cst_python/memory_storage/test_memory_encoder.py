import json
import unittest
from typing import Any
import math

from numpy.testing import assert_array_equal

from cst_python.memory_storage.memory_encoder import MemoryEncoder
from cst_python import MemoryObject

class TestMemoryEncoder(unittest.TestCase):

    def test_to_dict(self):
        memory = MemoryObject()
        memory.set_name("MemoryName")
        memory.set_info([1,2,3])
        memory.set_id(123)
        memory.set_evaluation(0.5)


        for i in range(2):
            if i == 0:
                memory_dict = MemoryEncoder.to_dict(memory)

                assert_array_equal(memory_dict["I"], [1,2,3])
            else:
                memory_dict = MemoryEncoder.to_dict(memory, jsonify_info=True)

                assert memory_dict["I"] == "[1, 2, 3]"

            assert memory_dict["timestamp"] == memory.get_timestamp()
            assert math.isclose(memory_dict["evaluation"], 0.5)
            assert memory_dict["name"] == "MemoryName"
            assert memory_dict["id"] == 123

    def test_load_memory(self):
        memory = MemoryObject()
        memory_dict = {"evaluation": "0.5", "id":"123", "I":"[5, 3, 4]"}

        MemoryEncoder.load_memory(memory, memory_dict)

        assert memory.get_evaluation() == 0.5
        assert memory.get_id() == 123
        assert_array_equal(memory.get_info(), [5, 3, 4])

    def test_default(self):
        memory = MemoryObject()
        memory.set_name("MemoryName")
        memory.set_info([1,2,3])
        memory.set_id(123)
        memory.set_evaluation(0.5)

        memory_json = json.dumps(memory, cls=MemoryEncoder)
        memory_dict = json.loads(memory_json)

        assert_array_equal(memory_dict["I"], [1,2,3])
        assert memory_dict["timestamp"] == memory.get_timestamp()
        assert math.isclose(memory_dict["evaluation"], 0.5)
        assert memory_dict["name"] == "MemoryName"
        assert memory_dict["id"] == 123
