import unittest

from cst_python import Mind, MemoryObject
from .utils import CodeletMock


class TestMind(unittest.TestCase):
    def setUp(self) -> None:
        self.test_codelet = CodeletMock()
        self.mind = Mind()

    def test_create_codelet_group(self) -> None:
        self.mind.create_codelet_group("testGroup")
        
        assert "testGroup" in self.mind.codelet_groups
    

    def test_create_memory_group(self) -> None:
        self.mind.create_memory_group("testGroup")
        
        assert "testGroup" in self.mind.memory_groups
    

    def test_insert_codelet_group(self) -> None:
        self.mind.create_codelet_group("testGroup")
        self.mind.insert_codelet(self.test_codelet, "testGroup")

        
        assert 1 == len(self.mind.code_rack.all_codelets)
        assert "testGroup" in self.mind.codelet_groups
        assert self.test_codelet == self.mind.get_codelet_group_list("testGroup")[0]    

    def test_register_memory_group(self) -> None:
        mo = MemoryObject()

        self.mind.create_memory_group("testGroup")
        self.mind.register_memory(mo, "testGroup")

        assert "testGroup" in self.mind.memory_groups
        assert mo == self.mind.memory_groups["testGroup"][0]
        assert 1 == len(self.mind.get_memory_group_list("testGroup"))
    

    def test_register_memory_by_name(self) -> None:
        mo = MemoryObject()
        mo.set_name("testName")

        self.mind.create_memory_group("testGroup")
        self.mind.raw_memory.add_memory(mo)
        self.mind.register_memory("testName", "testGroup")

        assert "testGroup" in self.mind.memory_groups
        assert mo == self.mind.memory_groups.get("testGroup")[0]
        assert 1 == len(self.mind.memory_groups.get("testGroup"))
    