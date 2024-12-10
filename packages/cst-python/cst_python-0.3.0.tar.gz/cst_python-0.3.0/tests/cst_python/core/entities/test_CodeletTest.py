from contextlib import redirect_stdout
import math
import unittest
import time
import threading
import io

from cst_python import MemoryObject, Mind
from .utils import CodeletMock

class TestCodelet(unittest.TestCase):
    def setUp(self) -> None:
        self.test_codelet = CodeletMock()

    
    def test_get_is_loop_test(self) -> None:
        # Any instantiated Codelet, if not changed, should be looping
        assert self.test_codelet.loop == True

    
    def test_upper_activation_bound_exception(self) -> None:
         
        with self.assertRaises(ValueError) as ve:
            self.test_codelet.activation = 2.0

        assert str(ve.exception) == "Codelet activation must be in (0.0 , 1.0) (value 2.0 is not allowed)."

        assert math.isclose(1.0, self.test_codelet.activation)

    
    def test_lowerActivationBoundException(self) -> None:
        with self.assertRaises(ValueError) as ve:
            self.test_codelet.activation = -0.8

        assert str(ve.exception) == "Codelet activation must be in (0.0 , 1.0) (value -0.8 is not allowed)."

        assert math.isclose(0.0, self.test_codelet.activation)
    

    
    def test_setInputs(self) -> None:
        dummy_inputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.inputs = dummy_inputs
        self.assertEqual(2, len(self.test_codelet.inputs))
    

    
    def test_getInput(self) -> None:
         
        dummy_inputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        dummy_inputs[0].set_name("testName1")
        self.test_codelet.inputs = dummy_inputs


        self.assertEqual(dummy_inputs[0], self.test_codelet.get_input(name="testName1"))
    

    
    def test_getInputNull(self) -> None:
         
        dummy_inputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.inputs = dummy_inputs

        self.assertIsNone(self.test_codelet.get_input(name="testName2"))
    

    
    def test_add_inputs(self) -> None:
         
        dummy_inputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.add_inputs(dummy_inputs)
        self.assertEqual(2, len(self.test_codelet.inputs))
    


    
    def test_removes_input(self) -> None:
         
        to_remove = MemoryObject()

        self.test_codelet.add_input(to_remove)
        self.assertEqual(1, len(self.test_codelet.inputs))

        self.test_codelet.removes_input(to_remove)
        self.assertEqual(0, len(self.test_codelet.inputs))
    

    
    def test_remove_from_input(self) -> None:
         
        to_remove = [MemoryObject(), MemoryObject()]

        self.test_codelet.add_inputs(to_remove)
        self.assertEqual(2, len(self.test_codelet.inputs))

        self.test_codelet.remove_from_input(to_remove)
        self.assertEqual(0, len(self.test_codelet.inputs))
    

    
    def test_remove_from_output(self) -> None:
         
        to_remove = [MemoryObject(), MemoryObject()]

        self.test_codelet.add_outputs(to_remove)
        self.assertEqual(2, len(self.test_codelet.outputs))

        self.test_codelet.remove_from_output(to_remove)
        self.assertEqual(0, len(self.test_codelet.outputs))
    

    
    def test_add_outputs(self) -> None:
         
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.add_outputs(dummy_outputs)
        self.assertEqual(2, len(self.test_codelet.outputs))
    

    
    def test_get_outputs(self) -> None:
         
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.add_outputs(dummy_outputs)
        self.assertEqual(dummy_outputs, self.test_codelet.outputs)
    

    
    def test_get_output(self) -> None:
         
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        dummy_outputs[0].set_name("testName3")
        self.test_codelet.add_outputs(dummy_outputs)
        self.assertEqual(dummy_outputs[0], self.test_codelet.get_output(name="testName3"))
    

    
    def test_get_outputNullReturn(self) -> None:
         
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.add_outputs(dummy_outputs)
        self.assertIsNone(self.test_codelet.get_output("testName4"))
    
        
    
    def test_get_outputEnableFalse(self) -> None:
        self.test_codelet.time_step = 100
        #with self.assertRaises(Exception): #TODO Fix test after Java correction
        with redirect_stdout(io.StringIO()):
            self.test_codelet.name = "thisCodeletWillFail"
            dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
            self.test_codelet.outputs = dummy_outputs
        
        
            self.test_codelet.get_output("testType", 3) # This line will raise an exception
            

            mind = Mind()
            mind.insert_codelet(self.test_codelet)
            mind.start()
            time.sleep(0.1)
            
            mind.shutdown()


        self.assertFalse(self.test_codelet.enabled)
        self.test_codelet.enabled = True
        self.assertTrue(self.test_codelet.enabled)
    

    
    def test_set_outputs(self) -> None:
         
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.outputs = dummy_outputs
        self.assertEqual(2, len(self.test_codelet.outputs))
    

    
    def test_getInputsOfType(self) -> None:
        dummy_inputs : list[MemoryObject] = [MemoryObject(), MemoryObject(), MemoryObject(), MemoryObject()]

        dummy_inputs[0].set_name("toGet")
        dummy_inputs[1].set_name("toGet")

        self.test_codelet.add_inputs(dummy_inputs)
        self.assertEqual(2, len(self.test_codelet.get_inputs_of_type("toGet")))
    

    
    def test_get_outputs_of_type(self) -> None:
         
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject(), MemoryObject(), MemoryObject()]

        dummy_outputs[0].set_name("toGet")
        dummy_outputs[1].set_name("toGet")

        self.test_codelet.add_outputs(dummy_outputs)
        self.assertEqual(2, len(self.test_codelet.get_outputs_of_type("toGet")))
    

    
    def test_get_broadcastNull(self) -> None:
         
        self.assertIsNone(self.test_codelet.get_broadcast("testName5"))
    

    
    def test_get_broadcastType(self) -> None:
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        dummy_outputs[0].set_name("testName6")
        self.test_codelet.add_broadcasts(dummy_outputs)
        self.assertEqual(dummy_outputs[0], self.test_codelet.get_broadcast("testName6", 0))
    

    
    def test_get_broadcastTypeIndex(self) -> None:
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        dummy_outputs[0].set_name("testName")
        dummy_outputs[1].set_name("testName")
        self.test_codelet.add_broadcasts(dummy_outputs)
        self.assertEqual(dummy_outputs[1], self.test_codelet.get_broadcast("testName", 1))
    

    
    def test_addBroadcasts(self) -> None:
        dummy_outputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        self.test_codelet.add_broadcasts(dummy_outputs)
        self.assertEqual(2, len(self.test_codelet.broadcast))
    

    
    def test_get_thread_name(self) -> None:
        threading.current_thread().name = "newThreadName"
        self.assertEqual("newThreadName", self.test_codelet.get_thread_name())
    

    
    def test_toString(self) -> None:
         
        dummy_inputs : list[MemoryObject] = [MemoryObject(), MemoryObject()]
        dummy_broadcasts : list[MemoryObject] = [MemoryObject(), MemoryObject()]

        expected_string = ("Codelet [activation=" + str(0.5) + ", " + "name=" + "testName" + ", "
                + ("broadcast=" + str(dummy_broadcasts[0:min(len(dummy_broadcasts), 10)]) + ", ")
                + ("inputs=" + str(dummy_inputs[0:min(len(dummy_inputs), 10)])) + ", "
                + ("outputs=" + "[]") + "]")

        self.test_codelet.name = "testName"

        self.test_codelet.activation = 0.5
        
        self.test_codelet.inputs = dummy_inputs
        self.test_codelet.broadcast = dummy_broadcasts

        self.assertEqual(expected_string, str(self.test_codelet))
    

    
    def test_setThreshold(self) -> None:
        self.test_codelet.threshold = 0.5

        
        assert math.isclose(0.5, self.test_codelet.threshold)
    

    
    def test_upperThresholdBound(self) -> None:

        with self.assertRaises(ValueError) as ve:
            self.test_codelet.threshold = 2.0

        assert str(ve.exception) == "Codelet threshold must be in (0.0 , 1.0) (value 2.0 is not allowed)."

        assert math.isclose(1.0, self.test_codelet.threshold)

    

    
    def test_lowerThresholdBound(self) -> None:

        with self.assertRaises(ValueError) as ve:
            self.test_codelet.threshold = -1.0

        assert str(ve.exception) == "Codelet threshold must be in (0.0 , 1.0) (value -1.0 is not allowed)."

        assert math.isclose(0.0, self.test_codelet.threshold)


    
    def test_getTimeStep(self) -> None:
         
        self.test_codelet.time_step = 222
        self.assertEqual(222, self.test_codelet.time_step)
    


    @unittest.skip("Codelet profiling not implemented")    
    def test_runProfiling(self) -> None:
         
        self.test_codelet.profiling = True
        self.test_codelet.time_step = 100

        with redirect_stdout(io.StringIO()):
            mind = Mind()
            mind.insert_codelet(self.test_codelet)
            mind.start()

            time.sleep(0.1)
        

        self.assertTrue(self.test_codelet.profiling)
    
