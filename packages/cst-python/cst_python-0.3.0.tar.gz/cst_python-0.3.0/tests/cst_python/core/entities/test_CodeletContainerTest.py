import unittest
import time

from cst_python.core.entities import Codelet, CodeletContainer, Mind, MemoryObject, Memory

class CodeletToTestOne(Codelet):
    def __init__(self, name:str):
        self.counter = 0
        
        self.name = name

    def access_memory_objects(self): #NOSONAR
        pass
    
    def calculate_activation(self):
        self.activation = self.counter

    def proc(self):
        self.counter += 1
        if (self.outputs is not None and len(self.outputs) != 0):
            self.outputs[0].set_info("CODELET 1 OUTPUT")

class CodeletToTestTwo(Codelet):
    def __init__(self, name:str):
        self.counter = 0
        
        self.name = name

    def access_memory_objects(self): #NOSONAR
        pass
    
    def calculate_activation(self): #NOSONAR
        pass

    def proc(self):
        self.counter += 2

class CodeletToTestThree(Codelet):
    def __init__(self, name:str):
        self.counter = 0
        
        self.name = name

    def access_memory_objects(self): #NOSONAR
        pass
    
    def calculate_activation(self):
        self.activation = self.counter

    def proc(self):
        self.counter += 3
        if (self.outputs is not None and len(self.outputs) != 0):
            self.outputs[0].set_info("CODELET 3 OUTPUT")

@unittest.skip("CodeletContainer not implemented")
class CodeletContainerTest (unittest.TestCase):

    def sleep(self, timestep:int) -> None:
        time.sleep(timestep/1000)

    
    def test_noMemoryChangeTest(self) -> None:
        # no codelet runs
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)
        mind.start()
        self.sleep(2000)  
        mind.shutdown()
        
        self.assertEqual(0, codelet_container.getOutputs().size())
        self.assertEqual( [], codelet_container.getOutputs())
        self.assertEqual( [], codelet_container.getOutputs())
        self.assertEqual( [], codelet_container.getOutputs())
        self.assertEqual(0, codelet_container.getEvaluation(), 0)
        
    
    
    
    def test_noMemoryChangeButCodeletAddedIsStartedTest(self) -> None:
        # no codelet runs
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, True)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)
        mind.start()
        self.sleep(2000)
        mind.shutdown()
        
        self.assertEqual(0, len(codelet_container.getOutputs()))
        self.assertEqual( [], codelet_container.getOutputs())
        self.assertEqual( [], codelet_container.getOutputs())
        self.assertEqual( [], codelet_container.getOutputs())
        self.assertEqual(0, codelet_container.getEvaluation(), 0)
        
    
    
    
    def test_runningCodeletChangingInputTest(self) -> None:
        # changes the codelet container input
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory_input1 = mind.create_memory_object("MEMORY_INPUT_1", 0.12)
        memory_input2 = mind.create_memory_object("MEMORY_INPUT_2", 0.32)
        memory_input3 = mind.create_memory_object("MEMORY_INPUT_3", 0.32)
        memory_input4 = mind.create_memory_object("MEMORY_INPUT_4", 0.32)
        memory_output1 = mind.create_memory_object("MEMORY_OUTPUT_1", 0.22)
        memory_output2 = mind.create_memory_object("MEMORY_OUTPUT_2", 0.22)
        memory_output3 = mind.create_memory_object("MEMORY_OUTPUT_3", 0.22)
        
        codelet_one.add_input(memory_input1)
        codelet_one.add_broadcast(memory_input2)
        codelet_one.add_output(memory_output1)
        
        codelet_two.add_broadcast(memory_input3)
        codelet_two.add_output(memory_output2)
        
        codelet_three.add_input(memory_input4)
        codelet_three.add_output(memory_output3)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)
        codelet_container.set_info(10)
        mind.start()
        self.sleep(2000)
        mind.shutdown()
        
        for codelet in codelet_container.getAll():
            for mem in codelet.inputs:
                self.assertEqual(10, mem.get_info())
            
        
        
        for codelet in codelet_container.getAll():
            for mem in codelet.broadcast:
                self.assertEqual(0.32, mem.get_info())
            
        
        
        self.assertEqual(3, codelet_container.getOutputs().size())
        expected_outputs = []
        expected_outputs.append(memory_output1)
        expected_outputs.append(memory_output2)
        expected_outputs.append(memory_output3)
        assert expected_outputs == list(codelet_container.getOutputs())
        self.assertEqual(0.22, codelet_container.getOutputs()[1].get_info())
        self.assertEqual("MEMORY_OUTPUT_3", codelet_container.getOutputs()[2].name)
        self.assertEqual(0, codelet_container.getEvaluation(), 0)
        
    
    
    
    def test_runningCodeletChangingInputCodeletStartedWhenAddedTest(self) -> None:
        # changes the codelet container input
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory_input1 = mind.create_memory_object("MEMORY_INPUT_1", 0.12)
        memory_input2 = mind.create_memory_object("MEMORY_INPUT_2", 0.32)
        memory_input3 = mind.create_memory_object("MEMORY_INPUT_3", 0.32)
        memory_input4 = mind.create_memory_object("MEMORY_INPUT_4", 0.32)
        memory_output1 = mind.create_memory_object("MEMORY_OUTPUT_1", 0.22)
        memory_output2 = mind.create_memory_object("MEMORY_OUTPUT_2", 0.22)
        memory_output3 = mind.create_memory_object("MEMORY_OUTPUT_3", 0.22)
        
        codelet_one.add_input(memory_input1)
        codelet_one.add_broadcast(memory_input2)
        codelet_one.add_output(memory_output1)
        
        codelet_two.add_broadcast(memory_input3)
        codelet_two.add_output(memory_output2)
        
        codelet_three.add_input(memory_input4)
        codelet_three.add_output(memory_output3)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, True)
        
        codelet_container.set_info(10)
        self.sleep(2000)
        
        for codelet in codelet_container.getAll():
            for mem in codelet.inputs:
                self.assertEqual(10, mem.get_info())
            
        
        
        for codelet in codelet_container.getAll():
            for mem in codelet.broadcast:
                self.assertEqual(0.32, mem.get_info())
            
        
        
        codelet_to_test_one : CodeletToTestOne = codelet_container.getCodelet("Codelet 1")
        self.assertEqual(7, codelet_to_test_one.counter)
        self.assertEqual(3, codelet_container.getOutputs().size())
        expected_outputs : list[Memory] = []
        expected_outputs.append(memory_output1)
        expected_outputs.append(memory_output2)
        expected_outputs.append(memory_output3)
        assert expected_outputs == list(codelet_container.getOutputs())
        self.assertEqual(0.22, codelet_container.getOutputs()[1].get_info())
        self.assertEqual("MEMORY_OUTPUT_3", codelet_container.getOutputs()[2].name)
        self.assertEqual(0, codelet_container.getEvaluation(), 0)
        
    
    
    
    def test_addCodeletsToCodeletContainerTest(self) -> None:
        # changes the codelet container input
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory_input1 = mind.create_memory_object("MEMORY_INPUT_1", 0.12)
        memory_input2 = mind.create_memory_object("MEMORY_INPUT_2", 0.32)
        memory_input3 = mind.create_memory_object("MEMORY_INPUT_3", 0.32)
        memory_input4 = mind.create_memory_object("MEMORY_INPUT_4", 0.32)
        memory_output1 = mind.create_memory_object("MEMORY_OUTPUT_1", 0.22)
        memory_output2 = mind.create_memory_object("MEMORY_OUTPUT_2", 0.22)
        memory_output3 = mind.create_memory_object("MEMORY_OUTPUT_3", 0.22)
        
        codelet_one.add_input(memory_input1)
        codelet_one.add_broadcast(memory_input2)
        codelet_one.add_output(memory_output1)
        
        codelet_two.add_broadcast(memory_input3)
        codelet_two.add_output(memory_output2)
        
        codelet_three.add_input(memory_input4)
        codelet_three.add_output(memory_output3)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer()
        codelet_container.addCodelet(codelet_one, False)
        codelet_container.addCodelet(codelet_two, False)
        codelet_container.addCodelet(codelet_three, False)
        
        
        self.assertEqual(3, codelet_container.getOutputs().size())
        expected_outputs : list[Memory] = []
        expected_outputs.append(memory_output1)
        expected_outputs.append(memory_output2)
        expected_outputs.append(memory_output3)
        assert expected_outputs == list(codelet_container.getOutputs())

        self.assertEqual("MEMORY_OUTPUT_1", codelet_container.getOutputs()[0].name)
        self.assertEqual("MEMORY_OUTPUT_2", codelet_container.getOutputs()[1].name)
        self.assertEqual("MEMORY_OUTPUT_3", codelet_container.getOutputs()[2].name)
        self.assertEqual(3, codelet_container.getCodelet(codelet_one.name).outputs.size())
        self.assertEqual(3, codelet_container.getCodelet(codelet_two.name).outputs.size())
        self.assertEqual(3, codelet_container.getCodelet(codelet_three.name).outputs.size())
        
        self.assertEqual(2, codelet_container.getInputs().size())
        expected_inputs : list[Memory] = []
        expected_inputs.append(memory_input1)
        expected_inputs.append(memory_input4)
        assert expected_inputs == list(codelet_container.getInputs())
        self.assertEqual("MEMORY_INPUT_1", codelet_container.getInputs()[0].name)
        self.assertEqual("MEMORY_INPUT_4", codelet_container.getInputs()[1].name)
        self.assertEqual(2, codelet_container.getCodelet(codelet_one.name).inputs.size())
        self.assertEqual(2, codelet_container.getCodelet(codelet_three.name).inputs.size())
        
        self.assertEqual(2, codelet_container.getBroadcast().size())
        expected_broadcast : list[Memory] = []
        expected_broadcast.append(memory_input2)
        expected_broadcast.append(memory_input3)
        assert expected_broadcast == list(codelet_container.getBroadcast())
        self.assertEqual("MEMORY_INPUT_2", codelet_container.getBroadcast()[0].name)
        self.assertEqual("MEMORY_INPUT_3", codelet_container.getBroadcast()[1].name)
        self.assertEqual(2, codelet_container.getCodelet(codelet_one.name).broadcast.size())
        self.assertEqual(2, codelet_container.getCodelet(codelet_two.name).broadcast.size())
    
    
    
    def test_addCodeletsToCodeletContainerWhichHasInputsAndOuputsTest(self) -> None:
        # changes the codelet container input
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory_input1 = mind.create_memory_object("MEMORY_INPUT_1", 0.12)
        # 2 and 3 is not used
        memory_input4 = mind.create_memory_object("MEMORY_INPUT_4", 0.32)
        memory_output1 = mind.create_memory_object("MEMORY_OUTPUT_1", 0.22)
        memory_output2 = mind.create_memory_object("MEMORY_OUTPUT_2", 0.22)
        memory_output3 = mind.create_memory_object("MEMORY_OUTPUT_3", 0.22)
        
        codelet_container = CodeletContainer()
        
        new_inputs : list[Memory] = []
        new_inputs.append(memory_input1)
        new_inputs.append(memory_input4)
        codelet_container.set_infonputs(new_inputs)
        
        new_outputs: list[Memory] = []
        new_outputs.append(memory_output1)
        new_outputs.append(memory_output2)
        new_outputs.append(memory_output3)
        codelet_container.setOutputs(new_outputs)	
        
        codelet_container.addCodelet(codelet_one, False)
        codelet_container.addCodelet(codelet_two, False)
        codelet_container.addCodelet(codelet_three, False)
        
        
        self.assertEqual(3, codelet_container.getOutputs().size())
        expected_outputs : list[Memory] = []
        expected_outputs.append(memory_output1)
        expected_outputs.append(memory_output2)
        expected_outputs.append(memory_output3)
        assert expected_outputs == list(codelet_container.getOutputs())
        self.assertEqual("MEMORY_OUTPUT_1", codelet_container.getOutputs()[0].name)
        self.assertEqual("MEMORY_OUTPUT_2", codelet_container.getOutputs()[1].name)
        self.assertEqual("MEMORY_OUTPUT_3", codelet_container.getOutputs()[2].name)
        self.assertEqual(3, codelet_container.getCodelet(codelet_one.name).outputs.size())
        self.assertEqual(3, codelet_container.getCodelet(codelet_two.name).outputs.size())
        self.assertEqual(3, codelet_container.getCodelet(codelet_three.name).outputs.size())
        
        self.assertEqual(2, codelet_container.getInputs().size())
        expected_inputs : list[Memory] = []
        expected_inputs.append(memory_input1)
        expected_inputs.append(memory_input4)
        assert expected_inputs == list(codelet_container.getInputs())
        self.assertEqual("MEMORY_INPUT_1", codelet_container.getInputs()[0].name)
        self.assertEqual("MEMORY_INPUT_4", codelet_container.getInputs()[1].name)
        self.assertEqual(2, codelet_container.getCodelet(codelet_one.name).inputs.size())
        self.assertEqual(2, codelet_container.getCodelet(codelet_three.name).inputs.size())
        
    
    
    
    def test_removeCodeletsFromCodeletContainerTest(self) -> None:
        # changes the codelet container input
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory_input1 = mind.create_memory_object("MEMORY_INPUT_1", 0.12)
        memory_input2 = mind.create_memory_object("MEMORY_INPUT_2", 0.32)
        memory_input3 = mind.create_memory_object("MEMORY_INPUT_3", 0.32)
        memory_input4 = mind.create_memory_object("MEMORY_INPUT_4", 0.32)
        memory_output1 = mind.create_memory_object("MEMORY_OUTPUT_1", 0.22)
        memory_output2 = mind.create_memory_object("MEMORY_OUTPUT_2", 0.22)
        memory_output3 = mind.create_memory_object("MEMORY_OUTPUT_3", 0.22)
        
        codelet_one.add_input(memory_input1)
        codelet_one.add_broadcast(memory_input2)
        codelet_one.add_output(memory_output1)
        
        codelet_two.add_broadcast(memory_input3)
        codelet_two.add_output(memory_output2)
        
        codelet_three.add_input(memory_input4)
        codelet_three.add_output(memory_output3)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        
        
        self.assertEqual(3, codelet_container.getOutputs().size())
        expected_outputs : list[Memory] = []
        expected_outputs.append(memory_output1)
        expected_outputs.append(memory_output2)
        expected_outputs.append(memory_output3)
        assert expected_outputs == list(codelet_container.getOutputs())
        self.assertEqual("MEMORY_OUTPUT_1", codelet_container.getOutputs()[0].name)
        self.assertEqual("MEMORY_OUTPUT_2", codelet_container.getOutputs()[1].name)
        self.assertEqual("MEMORY_OUTPUT_3", codelet_container.getOutputs()[2].name)
        self.assertEqual(3, codelet_container.getCodelet(codelet_one.name).outputs.size())
        self.assertEqual(3, codelet_container.getCodelet(codelet_two.name).outputs.size())
        self.assertEqual(3, codelet_container.getCodelet(codelet_three.name).outputs.size())
        
        self.assertEqual(2, codelet_container.getInputs().size())
        expected_inputs : list[Memory] = []
        expected_inputs.append(memory_input1)
        expected_inputs.append(memory_input4)
        assert expected_inputs == list(codelet_container.getInputs())
        self.assertEqual("MEMORY_INPUT_1", codelet_container.getInputs()[0].name)
        self.assertEqual("MEMORY_INPUT_4", codelet_container.getInputs()[1].name)
        self.assertEqual(2, codelet_container.getCodelet(codelet_one.name).inputs.size())
        self.assertEqual(2, codelet_container.getCodelet(codelet_three.name).inputs.size())
        
        self.assertEqual(2, codelet_container.getBroadcast().size())
        expected_broadcast : list[Memory] = []
        expected_broadcast.append(memory_input2)
        expected_broadcast.append(memory_input3)
        assert expected_broadcast == list(codelet_container.getBroadcast())
        self.assertEqual("MEMORY_INPUT_2", codelet_container.getBroadcast()[0].name)
        self.assertEqual("MEMORY_INPUT_3", codelet_container.getBroadcast()[1].name)
        self.assertEqual(2, codelet_container.getCodelet(codelet_one.name).broadcast.size())
        self.assertEqual(2, codelet_container.getCodelet(codelet_two.name).broadcast.size())
        
        codelet_container.removeCodelet(codelet_one)
        
        self.assertEqual(2, codelet_container.getOutputs().size())
        expected_outputs = []
        expected_outputs.append(memory_output2)
        expected_outputs.append(memory_output3)
        assert expected_outputs == list(codelet_container.getOutputs())
        self.assertEqual(2, codelet_container.getCodelet(codelet_two.name).outputs.size())
        self.assertEqual(2, codelet_container.getCodelet(codelet_three.name).outputs.size())
        
        self.assertEqual(1, codelet_container.getInputs().size())
        expected_inputs = []
        expected_inputs.append(memory_input4)
        assert expected_inputs == list(codelet_container.getInputs())
        self.assertEqual("MEMORY_INPUT_4", codelet_container.getInputs()[0].name)
        self.assertEqual(1, codelet_container.getCodelet(codelet_three.name).inputs.size())
        
        self.assertEqual(1, codelet_container.getBroadcast().size())
        expected_broadcast = []
        expected_broadcast.append(memory_input3)
        assert expected_broadcast == list(codelet_container.getBroadcast())
        self.assertEqual("MEMORY_INPUT_3", codelet_container.getBroadcast()[0].name)
        self.assertEqual(1, codelet_container.getCodelet(codelet_two.name).broadcast.size())
        
        codelet_container.removeCodelet(codelet_two)
        
        self.assertEqual(1, codelet_container.getOutputs().size())
        expected_outputs = []
        expected_outputs.append(memory_output3)
        assert expected_outputs == list(codelet_container.getOutputs())
        self.assertEqual(1, codelet_container.getCodelet(codelet_three.name).outputs.size())
        
        self.assertEqual(1, codelet_container.getInputs().size())
        expected_inputs = []
        expected_inputs.append(memory_input4)
        assert expected_inputs == list(codelet_container.getInputs())
        self.assertEqual("MEMORY_INPUT_4", codelet_container.getInputs()[0].name)
        self.assertEqual(1, codelet_container.getCodelet(codelet_three.name).inputs.size())
        
        self.assertEqual(0, codelet_container.getBroadcast().size())
        self.assertEqual(0, codelet_container.getCodelet(codelet_three.name).broadcast.size())
        
        
    
    
    
    def test_getEvaluationTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        test_value = 100.0
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)
        memory1.setEvaluation(test_value)
        codelet_container.set_info(10)
        mind.start()
        self.sleep(2000)
        mind.shutdown()
        
    
        
        self.assertEqual(test_value, codelet_container.getEvaluation())
        
        
    
    
    
    def test_getActivationTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        test_value = 6.0
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)
        memory1.setEvaluation(test_value)
        codelet_container.set_info(10)
        mind.start()
        self.sleep(2000)
        mind.shutdown()
        
    
        
        self.assertEqual(test_value, codelet_container.getActivation(), 0)
        
    
    
    
    def test_set_infonputsTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)

        new_inputs : list[Memory] = []
        new_inputs.append(memory1)
        codelet_container.set_infonputs(new_inputs)
        
    
        
        self.assertEqual(new_inputs, codelet_container.getInputs())
        
    
    
    
    def test_setOutputsTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)

        new_outputs: list[Memory] = []
        new_outputs.append(memory1)
        codelet_container.setOutputs(new_outputs)
        
    
        
        self.assertEqual(new_outputs, codelet_container.getOutputs())
        
    
    
    
    def test_setBroadcastTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)

        new_broadcast : list[Memory] = []
        new_broadcast.append(memory1)
        codelet_container.setBroadcast(new_broadcast)
        
    
        
        self.assertEqual(new_broadcast, codelet_container.getBroadcast())
        
    
    
    
    def test_setNameTest(self) -> None:
        codelet_container = CodeletContainer()
        codelet_container.setName("Container")
        self.assertEqual("Container", codelet_container.name)
    
    
    
    def test_setTypeTest(self) -> None:
        codelet_container = CodeletContainer()
        codelet_container.setType("Container")
        self.assertEqual("Container", codelet_container.name)
    
    
    
    def test_setEvaluationTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        codelet_one.add_input(memory1)
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container = CodeletContainer(codelet_container_array, False)
        codelet_container.setEvaluation(5.0)
        self.assertEqual(5.0, codelet_container.getCodelet("Codelet 1").getInputs()[0].getEvaluation(),0)
    
    
    
    def test_addMemoryObserverTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.set_infosMemoryObserver(True)
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        codelet_container.addMemoryObserver(codelet_one)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)
        codelet_container.set_info(10)
        mind.start()
        self.sleep(2000)
        mind.shutdown()
        
    
        codelet_to_test_one : CodeletToTestOne = codelet_container.getCodelet("Codelet 1")
        self.assertEqual(6, codelet_to_test_one.counter)
    
    
    
    def test_getTimestampTest(self) -> None:
        codelet_one = CodeletToTestOne("Codelet 1")
        codelet_two = CodeletToTestTwo("Codelet 2")
        codelet_three = CodeletToTestThree("Codelet 3")
        
        mind = Mind()
        memory1 = mind.create_memory_object("MEMORY1", 0.12)
        memory2 = mind.create_memory_object("MEMORY2", 0.32)
        memory3 = mind.create_memory_object("MEMORY3", 0.32)
        memory4 = mind.create_memory_object("MEMORY4", 0.32)
        
        codelet_one.add_input(memory1)
        codelet_one.add_broadcast(memory2)
        
        codelet_two.add_broadcast(memory3)
        
        codelet_three.add_input(memory4)
        
        codelet_container_array : list[Codelet] = []
        codelet_container_array.append(codelet_one)
        codelet_container_array.append(codelet_two)
        codelet_container_array.append(codelet_three)
        
        codelet_container = CodeletContainer(codelet_container_array, False)
        
        mind.insert_codelet(codelet_one)
        mind.insert_codelet(codelet_two)
        mind.insert_codelet(codelet_three)
        codelet_container.set_info(10)
        mind.start()
        self.sleep(2000)
        mind.shutdown()
        
        self.assertGreater(codelet_container.getTimestamp().doubleValue(), 1)
        
    