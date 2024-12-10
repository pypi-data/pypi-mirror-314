from contextlib import redirect_stdout
import io
import unittest

from cst_python.core.entities import RawMemory, MemoryBuffer, MemoryObject

@unittest.skip("MemoryBuffer not implemented")
class MemoryBufferTest(unittest.TestCase):

    @unittest.skip("'setType' is not implemented in Python as is deprecated")
    def test_basic_call(self) -> None:
        rawMemory = RawMemory()
        memoryBuffer = MemoryBuffer(3, rawMemory)

        testList : list[MemoryObject] = [MemoryObject(), MemoryObject(), MemoryObject()]
        testList[0].setType("memory_0")
        testList[1].setType("memory_1")
        testList[2].setType("memory_2")

        memoryBuffer.putList(testList)

        self.assertEqual(3, len(memoryBuffer))
        self.assertEqual(memoryBuffer.get(), memoryBuffer.getAll())
        self.assertEqual(testList[2], memoryBuffer.getMostRecent())
        self.assertEqual(testList[0], memoryBuffer.getOldest())
    

    @unittest.skip("'setType' is not implemented in Python as is deprecated")
    def test_puts_more_than_max(self) -> None:
        rawMemory = RawMemory()
        memoryBuffer = MemoryBuffer(3, rawMemory)

        testList : list[MemoryObject] = [MemoryObject(), MemoryObject(), MemoryObject(), MemoryObject()]
        testList[0].setType("memory_0")
        testList[1].setType("memory_1")
        testList[2].setType("memory_2")
        testList[3].setType("memory_3")
        memoryBuffer.putList(testList)

        self.assertEqual(3, len(memoryBuffer))
        self.assertEqual(memoryBuffer.get(), memoryBuffer.getAll())
        self.assertEqual(testList[1], memoryBuffer.get()[0])

        memoryBuffer.put(MemoryObject())
        self.assertEqual(testList[2], memoryBuffer.get()[0])
    

    @unittest.skip("'setType' is not implemented in Python as is deprecated")
    def test_put_pop(self) -> None:
        rawMemory = RawMemory()
        memoryBuffer = MemoryBuffer(3, rawMemory)

        testMemory = MemoryObject()
        testMemory.setType("memory_0")
        memoryBuffer.put(testMemory)

        self.assertEqual(testMemory, memoryBuffer.pop())
        self.assertEqual(0, len(memoryBuffer))
    

    
    def test_null_oldest_and_newest(self) -> None:
        rawMemory = RawMemory()
        memoryBuffer = MemoryBuffer(3, rawMemory)

        self.assertIsNone(memoryBuffer.getOldest())
        self.assertIsNone(memoryBuffer.getMostRecent())
    

    @unittest.skip("'setType' is not implemented in Python as is deprecated")
    def test_remove_and_clear(self) -> None:
        rawMemory = RawMemory()
        memoryBuffer = MemoryBuffer(3, rawMemory)

        testList : list[MemoryObject] = [MemoryObject(), MemoryObject(), MemoryObject()]
        testList[0].setType("memory_0")
        testList[1].setType("memory_1")
        testList[2].setType("memory_2")

        memoryBuffer.putList(testList)
        memoryBuffer.remove(testList[1])

        self.assertEqual(2, len(memoryBuffer))
        self.assertEqual(testList[2], memoryBuffer.get()[1])

        memoryBuffer.clear()
        self.assertEqual(0, len(memoryBuffer))
    

    @unittest.skip("'setType' is not implemented in Python as is deprecated")
    def test_pint_status(self) -> None:
        rawMemory = RawMemory()
        memoryBuffer = MemoryBuffer(3, rawMemory)

        testList : list[MemoryObject] = [MemoryObject()]
        testList[0].setType("memory_0")
        memoryBuffer.putList(testList)

        expectedMessage ='''"###### Memory Buffer ########\n# Content: [MemoryObject [idmemoryobject=null, timestamp=null, evaluation=0.0, I=null, name=memory_0]]" +
                "\n# Size: 1\n###############################'''
        
        with redirect_stdout(io.StringIO()) as f:
            memoryBuffer.printStatus()
        
        printed = f.getvalue().replace("\r\n", "\n")
        expectedMessage = expectedMessage.replace("\r\n", "\n")

        self.assertTrue(expectedMessage in printed)
    