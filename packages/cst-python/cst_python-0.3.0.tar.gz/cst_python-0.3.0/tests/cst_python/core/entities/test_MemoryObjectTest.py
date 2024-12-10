import unittest

from cst_python import MemoryObject, Mind

class MemoryObjectTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mo = MemoryObject()

    def test_id(self) -> None:
        self.mo.set_id(2000)

        assert 2000 == self.mo.get_id()

    def test_to_string(self) -> None:
        I = object()

        self.mo.set_id(2000)
        self.mo.set_evaluation(0.8)
        self.mo.set_info(I)
        self.mo.set_type("testName")

        expected_string = f'''MemoryObject [idmemoryobject={2000}, timestamp={self.mo.get_timestamp()}, evaluation={0.8}, I={I}, name={"testName"}]'''

        assert expected_string == str(self.mo)

    def test_hash_code(self):
        I = object()
        self.mo_eval = 0.8
        self.mo_id = 2000
        name = "test_name"

        self.mo.set_id(self.mo_id)
        self.mo.set_evaluation(self.mo_eval)
        self.mo.set_info(I)
        self.mo.set_type(name)

        prime = 31
        excepted_value = 1
        excepted_value = prime * excepted_value + (hash(I))
        excepted_value = prime * excepted_value + (hash(self.mo_eval))
        excepted_value = prime * excepted_value + (hash(self.mo_id))
        excepted_value = prime * excepted_value + (hash(name))
        excepted_value = prime * excepted_value + (0 if self.mo.get_timestamp() is None else hash(self.mo.get_timestamp()))

        #Python truncates the __hash__ return if is too long hashing it, so here we need hash(expected_value)        
        assert hash(excepted_value) == hash(self.mo)

    def test_equals(self):
        other_mo = MemoryObject()
        third_mo = MemoryObject()
        fourth_mo = MemoryObject()

        self.mo.set_info(0.0)
        other_mo.set_info(0.0)
        third_mo.set_info(1.0)

        assert self.mo != fourth_mo
        assert self.mo != third_mo

        self.mo.set_evaluation(0.0)
        other_mo.set_evaluation(0.0)
        third_mo.set_evaluation(1.0)

        fourth_mo.set_info(0.0)
        fourth_mo.set_evaluation(None)

        assert self.mo != fourth_mo
        assert self.mo != third_mo

        self.mo.set_id(1000)
        other_mo.set_id(2000)
        third_mo.set_id(2000)


        fourth_mo.set_evaluation(0.0)
        fourth_mo.set_id(None)

        assert fourth_mo != self.mo
        assert self.mo != other_mo

        other_mo.set_id(1000)
        fourth_mo.set_id(1000)

        self.mo.set_type("firstName")
        other_mo.set_type("firstName")
        third_mo.set_type("secondName")

        assert fourth_mo != self.mo
        assert self.mo != third_mo

        fourth_mo.set_type("firstName")

        self.mo.timestamp = 100
        other_mo.timestamp = 100
        third_mo.timestamp = 200
        fourth_mo.timestamp = None

        assert fourth_mo != self.mo
        assert self.mo != third_mo

        fourth_mo.timestamp = 200
        assert fourth_mo != self.mo

        assert self.mo == other_mo

    def test_equals_false_None(self) -> None:
        other_mo = MemoryObject()
        third_mo = MemoryObject()
        fourth_mo = MemoryObject()

        self.mo.set_info(0.0)
        other_mo.set_info(0.0)
        third_mo.set_info(1.0)

        assert fourth_mo != self.mo
        assert self.mo != third_mo

        self.mo.set_evaluation(0.0)
        other_mo.set_evaluation(0.0)
        third_mo.set_evaluation(1.0)

        assert fourth_mo != self.mo
        assert self.mo != third_mo


        self.mo.set_id(100)
        other_mo.set_id(100)
        third_mo.set_id(200)

        assert fourth_mo != self.mo
        assert self.mo != third_mo


        self.mo.set_type("firstName")
        other_mo.set_type("firstName")
        third_mo.set_type("secondName")

        assert fourth_mo != self.mo
        assert self.mo != third_mo


        self.mo.timestamp = 10
        other_mo.timestamp = 10
        third_mo.timestamp = 20
        fourth_mo.timestamp = None

        assert fourth_mo != self.mo
        assert self.mo != third_mo

        assert self.mo == other_mo