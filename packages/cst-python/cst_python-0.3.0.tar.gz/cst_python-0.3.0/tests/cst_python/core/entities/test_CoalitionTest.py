import unittest

from cst_python.core.entities import Coalition
from .utils import CodeletMock

@unittest.skip("Coalition not implemented")
class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.test_codelet = CodeletMock()
        self.other_codelet = CodeletMock()

    
    def test_calculateActivationTest(self) -> None:
        coalition = Coalition([self.test_codelet, self.other_codelet])
        try:
            coalition.getCodeletsList().get(0).setActivation(1.0)
        except CodeletActivationBoundsException as e: 
            e.printStackTrace()
        

        self.assertEqual(0.5, coalition.calculateActivation(), 0)
    

    
    def test_setCodeletListTest(self) -> None:
        coalition = Coalition([self.test_codelet])

        list_test = [self.test_codelet, self.other_codelet]
        coalition.setCodeletsList(list_test)

        self.assertEqual(list_test, coalition.getCodeletsList())
    

    
    def test_activation_test(self) -> None:
        coalition = Coalition([self.test_codelet])

        activation_test = 0.8
        coalition.setActivation(activation_test)

        self.assertEqual(0.8, coalition.getActivation(), 0)
    

    
    def test_toStringTest(self) -> None:
        list_test = [self.test_codelet, self.other_codelet]
        coalition = Coalition([self.test_codelet, self.other_codelet])
        coalition.setActivation(0.8)

        expect_message = f"Coalition [activation={0.8}, codeletsList={list_test}]"

        self.assertIn(str(coalition), expect_message)
       