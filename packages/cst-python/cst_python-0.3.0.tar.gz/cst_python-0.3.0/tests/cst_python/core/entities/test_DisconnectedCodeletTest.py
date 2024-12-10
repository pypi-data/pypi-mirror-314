import unittest

from .utils import CodeletMock

class disconnected_codeletTest (unittest.TestCase):
    def setUp(self) -> None:
        self.message = ""

    def tearDown(self) -> None:
        super().tearDown()

    
    def test_disconnected_codelet(self) -> None:
            
        disconnected_codelet = CodeletMock()
    
        disconnected_codelet.name = "Disconnected Codelet"
        try:
            disconnected_codelet.start()
            disconnected_codelet.getInput("TYPE", 0)
            disconnected_codelet.stop()
        except Exception as e:
            message = repr(e)
            #print("Testing disconnected_codelet:"+e.getMessage())
        
        disconnected_codelet.stop()
        #print("Codelet stopped !")