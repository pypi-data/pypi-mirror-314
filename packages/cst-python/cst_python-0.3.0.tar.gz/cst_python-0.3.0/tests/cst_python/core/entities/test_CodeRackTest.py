import unittest

from cst_python.core.entities import CodeRack, MemoryObject, Codelet
from .utils import CodeletMock

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.test_codelet = CodeletMock()
        self.other_codelet = CodeletMock()

    
    def test_setAllCodeletTest(self) -> None:
        code_rack = CodeRack()
        test_list : list[Codelet] = [self.test_codelet, self.other_codelet]

        code_rack.all_codelets = test_list
        self.assertEqual(test_list, code_rack.all_codelets)
    

    
    def test_insertCodeletTest(self) -> None:
        code_rack = CodeRack()
        test_list : list[Codelet] = [self.test_codelet]

        code_rack.insert_codelet(self.test_codelet)

        self.assertEqual(test_list, code_rack.all_codelets)
    

    
    def test_createCodeletTest(self) -> None:
        code_rack = CodeRack()
        mem_input_test = [MemoryObject(), MemoryObject()]
        mem_output_test = [MemoryObject()]

        code_rack.create_codelet(0.5, None, mem_input_test, mem_output_test, self.test_codelet)

        self.assertEqual(self.test_codelet, code_rack.all_codelets[0])
    
    def test_destroyCodeletTest(self) -> None:
        code_rack = CodeRack()
        mem_input_test = [MemoryObject(), MemoryObject()]
        mem_output_test = [MemoryObject()]

        code_rack.create_codelet(0.5, None, mem_input_test, mem_output_test, self.test_codelet)

        code_rack.destroy_codelet(self.test_codelet)

        self.assertEqual(0, len(code_rack.all_codelets))
    
    
    def test_startStopTest(self) -> None:
        code_rack = CodeRack()
        test_list : list[Codelet] = [self.test_codelet, self.other_codelet]

        code_rack.all_codelets = test_list
        code_rack.start()
        self.assertTrue(code_rack.all_codelets[0].loop)

        code_rack.stop()
        self.assertFalse(code_rack.all_codelets[0].loop)
    