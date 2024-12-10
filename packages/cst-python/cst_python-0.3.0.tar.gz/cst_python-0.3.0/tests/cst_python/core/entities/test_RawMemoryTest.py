import unittest
import io
from contextlib import redirect_stdout

from cst_python.core.entities import RawMemory, MemoryObject, Memory

class TestRawMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_memory = RawMemory()

    
    def test_getAllOfType(self) -> None:
        test_list : list[Memory] = [MemoryObject(), MemoryObject(), MemoryObject(), MemoryObject()]
        test_list[0].set_name("TYPE")
        test_list[1].set_name("TYPE")
        self.raw_memory.all_memories = test_list

        assert 2 == len(self.raw_memory.get_all_of_type("TYPE"))
        assert test_list[0:2] == self.raw_memory.get_all_of_type("TYPE")

    
    def test_printContent(self) -> None:
        mem = MemoryObject()
        mem.set_name("TYPE")
        self.raw_memory.add_memory(mem)
        expected_message = f'''MemoryObject [idmemoryobject={mem.get_id()}, timestamp={mem.get_timestamp()}, evaluation={0.0}, I={None}, name={"TYPE"}]'''

        with redirect_stdout(io.StringIO()) as f:
            self.raw_memory.print_content()
        
        printed = f.getvalue().splitlines()[0]
        
        assert printed == expected_message
    

    
    def test_createAndDestroyMemoryObject(self) -> None:
        self.raw_memory.create_memory_object("TYPE")

        assert 1 == len(self.raw_memory)
        self.raw_memory.destroy_memory(self.raw_memory.all_memories[0])

        assert 0 == len(self.raw_memory)
    

    
    def test_shutdown(self) -> None:
        test_list : list[Memory] = [MemoryObject(), MemoryObject(), MemoryObject(), MemoryObject()]
        self.raw_memory.all_memories = test_list

        assert 4 == len(self.raw_memory)

        self.raw_memory.shutdown()
        assert 0 == len(self.raw_memory)
    