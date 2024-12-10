import unittest
from typing import Callable

from cst_python.core.entities import MemoryContainer, Memory, MemoryObject

@unittest.skip("Memory Container not implemented")
class MemoryContainerTest (unittest.TestCase):

    def test_memory_container_content(self) -> None:
        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(71, 0.1, "TYPE")
        memoryContainer.set_info(75, 0.2, "TYPE")

        self.assertEqual(75, memoryContainer.get_info())

    def test_memory_container_size(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(71, 0.1, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE3")

        self.assertEqual(2, memoryContainer.getAllMemories().size())

    def test_set_type(self) -> None:
        # memoryContainer = MemoryContainer()
        # memoryContainer.setType("TYPE")
        # self.assertEqual("TYPE", memoryContainer.get_name())

        memoryContainer = MemoryContainer()
        memoryContainer.set_name("TYPE2")
        self.assertEqual("TYPE2", memoryContainer.get_name())

        memoryContainer = MemoryContainer("TYPE3")
        self.assertEqual("TYPE3", memoryContainer.get_name())

    def test_get_type(self) -> None:
        memoryContainer = MemoryContainer("TYPE-Container")
        memoryContainer.set_info("value", 1.0, "TYPE")
        self.assertEqual(memoryContainer.get_info("TYPE"), "value")
        print("-- This test will raise a warning ...")
        self.assertIsNone(memoryContainer.get_info("TYPE2"))

    def test_get_i(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(71, 0.1, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")

        self.assertEqual(70, memoryContainer.get_info())
        self.assertEqual(75, memoryContainer.get_info(0))
        print("-- This test will raise a warning ...")
        # This test will raise a warning for index greater than the number of stored memories
        self.assertIsNone(memoryContainer.get_info(2))
        self.assertEqual(70, memoryContainer.get_info("TYPE3"))

    def test_get_i_predicate(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(71, 0.1, "TYPE2")
        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")
        memoryContainer.set_info(70, 0.25)

        pred: Callable[[Memory], bool] = lambda m: m.get_name() == "TYPE2"

        self.assertEqual(75, memoryContainer.get_info(pred))

    def test_get_i_accumulator(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")
        memoryContainer.set_info(80)

        binaryOperator: Callable[[Memory, Memory], Memory] = lambda mem1, mem2: mem1 if mem1.get_evaluation(
        ) <= mem2.get_evaluation() else mem2

        self.assertEqual(80, memoryContainer.get_info(binaryOperator))

    def test_set_i_specific(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")
        memoryContainer.set_info(80)

        memoryContainer.set_info(60, 1)
        memoryContainer.set_info(90, 0.5, 2)

        self.assertEqual(60, memoryContainer.get_info(1))
        self.assertEqual(90, memoryContainer.get_info())
        self.assertEqual(0.5, memoryContainer.get_evaluation(), 0)

    def test_set_evaluation(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")

        memoryContainer.set_info(90, 0.5, 2)

        self.assertEqual(70, memoryContainer.get_info())
        memoryContainer.set_evaluation(0.5, 0)
        self.assertEqual(75, memoryContainer.get_info())

    def test_set_evaluation_last(self) -> None:
        memoryContainer = MemoryContainer("TYPE")
        print("-- This test will raise a warning ...")
        memoryContainer.set_evaluation(2.0)
        self.assertEqual(memoryContainer.get_evaluation(), None)
        memoryContainer.set_info("message")
        memoryContainer.set_evaluation(2.0)
        self.assertEqual(memoryContainer.get_evaluation(), 2.0)

    def test_get_timestamp_not_valid(self) -> None:
        memoryContainer = MemoryContainer("TYPE")
        print("-- This test will raise a warning ...")
        ts: int = memoryContainer.get_timestamp()
        self.assertEqual(ts, None)
        memoryContainer.set_info("message")
        ts = memoryContainer.get_timestamp()
        self.assertTrue(ts != None)

    def test_add(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")
        memoryContainer.add(MemoryObject())

        self.assertEqual(3, memoryContainer.getAllMemories().size())

    def test_get_internal(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")

        self.assertEqual(
            75, memoryContainer.getInternalMemory("TYPE2").get_info())
        self.assertIsNone(memoryContainer.getInternalMemory("TYPE4"))

    def test_get_timestamp(self) -> None:

        memoryContainer = MemoryContainer("TYPE")

        memoryContainer.set_info(75, 0.2, "TYPE2")
        memoryContainer.set_info(70, 0.3, "TYPE3")

        self.assertEqual(memoryContainer.getInternalMemory("TYPE3").get_timestamp(),
                          memoryContainer.get_timestamp())

    def test_max_policy(self) -> None:
        memoryContainer = MemoryContainer("MAX")
        memoryContainer.setPolicy(Policy.MAX)
        m1 = memoryContainer.set_info(1, 0.2)
        m2 = memoryContainer.set_info(2, 0.4)
        m3 = memoryContainer.set_info(3, 0.8)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 3)
        memoryContainer.set_evaluation(0.1)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 2)
        memoryContainer.set_evaluation(0.1)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 1)
        memoryContainer.set_evaluation(0.1, m1)
        memoryContainer.set_evaluation(0.1, m2)
        memoryContainer.set_evaluation(0.1, m3)

        for j in range(20):
            m: int = memoryContainer.get_info()
            ver: bool = (m == 1 or m == 2 or m == 3)
            self.assertEqual(ver, True)
            # print("max: "+m)

        memoryContainer.set_evaluation(0.05, m1)
        for j in range(20):
            m: int = memoryContainer.get_info()
            ver: bool = (m == 2 or m == 3)
            self.assertEqual(ver, True)
            # print("max2: "+m)

    def test_max_policy_with_same_eval(self) -> None:
        memoryContainer = MemoryContainer("MAX")
        memoryContainer.setPolicy(Policy.MAX)
        m1 = memoryContainer.set_info(1, 0.2)
        m2 = memoryContainer.set_info(2, 0.2)
        m3 = memoryContainer.set_info(3, 0.2)
        i = -1
        oldi = 0
        for j in range(10):
            oldi = i
            # Despite the choice is random, if no chance in I happens, it stays the same
            i: int = memoryContainer.get_info()
            if (j > 0):
                self.assertEqual(oldi, i)

        i2: int = 0
        k = 0

        while True:
            memoryContainer.set_info(1, m1)
            memoryContainer.set_info(2, m2)
            memoryContainer.set_info(3, m3)
            i2: int = memoryContainer.get_info()

            k += 1

            if not (i2 == i and k < 100):
                break

        self.assertTrue(k != 100)

    def test_min_policy_with_same_eval(self) -> None:
        memoryContainer = MemoryContainer("MIN")
        memoryContainer.setPolicy(Policy.MIN)
        m1: int = memoryContainer.set_info(1, 0.2)
        m2: int = memoryContainer.set_info(2, 0.2)
        m3: int = memoryContainer.set_info(3, 0.2)
        i = -1
        oldi = 0
        for j in range(10):
            oldi = i
            # Despite the choice is random, if no chance in I happens, it stays the same
            i: int = memoryContainer.get_info()
            if (j > 0):
                self.assertEqual(oldi, i)

        i2 = 0
        k = 0
        while True:
            # Changing I will trigger a different choice, though !
            memoryContainer.set_info(1, m1)
            memoryContainer.set_info(2, m2)
            memoryContainer.set_info(3, m3)
            i2: int = memoryContainer.get_info()
            k += 1
            if not (i2 == i and k < 100):
                break
        self.assertTrue(k != 100)

    def test_max_unique_policy(self) -> None:
        memoryContainer = MemoryContainer("MAX")
        memoryContainer.setPolicy(Policy.MAX)
        memoryContainer.set_info(1)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 1)

    def test_min_policy(self) -> None:
        memoryContainer = MemoryContainer("MIN")
        memoryContainer.setPolicy(Policy.MIN)
        m1: int = memoryContainer.set_info(1, 0.2)
        m2: int = memoryContainer.set_info(2, 0.4)
        m3: int = memoryContainer.set_info(3, 0.8)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 1)
        memoryContainer.set_evaluation(0.9)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 2)
        memoryContainer.set_evaluation(0.9)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 3)
        memoryContainer.set_evaluation(0.1, m1)
        memoryContainer.set_evaluation(0.1, m2)
        memoryContainer.set_evaluation(0.1, m3)
        for k in range(20):
            m: int = memoryContainer.get_info()
            ver: bool = (m == 1 or m == 2 or m == 3)
            self.assertEqual(ver, True)
            # print("min: "+m)

        memoryContainer.set_evaluation(0.2, m1)
        for k in range(20):
            m: int = memoryContainer.get_info()
            ver: bool = (m == 2 or m == 3)
            self.assertEqual(ver, True)
            # print("min2: "+m)

    def test_random_proportional_policy(self) -> None:
        memoryContainer = MemoryContainer("RANDOMPROPORTIONAL")
        memoryContainer.setPolicy(Policy.RANDOM_PROPORTIONA)
        memoryContainer.set_info(1, 0.2)  # 14 %
        memoryContainer.set_info(2, 0.4)  # 28 %
        memoryContainer.set_info(3, 0.8)  # 57 %
        count = [0, 0, 0]
        for i in range(1000):
            j: int = memoryContainer.get_info()
            count[j-1] += 1

        # print("[0]: "+count[0]+" [1]: "+count[1]+" [2]: "+count[2])
        self.assertEqual(count[0] < count[1], True)
        self.assertEqual(count[1] < count[2], True)
        memoryContainer.set_evaluation(0.8, 0)
        memoryContainer.set_evaluation(0.4, 1)
        memoryContainer.set_evaluation(0.2, 2)
        count = int[3]
        for i in range(1000):
            j: int = memoryContainer.get_info()
            count[j-1] += 1

        # print("[0]: "+count[0]+" [1]: "+count[1]+" [2]: "+count[2])
        self.assertEqual(count[0] > count[1], True)
        self.assertEqual(count[1] > count[2], True)
        memoryContainer.set_info(1, 0.5, 0)
        memoryContainer.set_info(2, 0.0, 1)
        memoryContainer.set_info(3, 0.0, 2)
        for i in range(5):
            j: int = memoryContainer.get_info()
            self.assertEqual(j, 1)

        memoryContainer.set_info(1, 0.0, 0)
        memoryContainer.set_info(2, 0.5, 1)
        memoryContainer.set_info(3, 0.0, 2)
        for i in range(5):
            j: int = memoryContainer.get_info()
            self.assertEqual(j, 2)

        memoryContainer.set_info(1, 0.0, 0)
        memoryContainer.set_info(2, 0.0, 1)
        memoryContainer.set_info(3, 0.5, 2)
        for i in range(5):
            j: int = memoryContainer.get_info()
            self.assertEqual(j, 3)

        memoryContainer.set_info(1, 0.0, 0)
        memoryContainer.set_info(2, 0.0, 1)
        memoryContainer.set_info(3, 0.0, 2)
        count = int[3]
        for i in range(30):
            j: int = memoryContainer.get_info()
            count[j-1] += 1

        # print("[0]: "+count[0]+" [1]: "+count[1]+" [2]: "+count[2])
        self.assertEqual(count[0] > 0, True)
        self.assertEqual(count[1] > 0, True)
        self.assertEqual(count[2] > 0, True)

    def test_random_proportional_stable_policy(self) -> None:
        memoryContainer = MemoryContainer("RANDOMPROPORTIONALSTABLE")
        memoryContainer.setPolicy(Policy.RANDOM_PROPORTIONAL_STABLE)
        n = memoryContainer.set_info(1, 0.2)  # 14 %
        memoryContainer.set_info(2, 0.4)  # 28 %
        memoryContainer.set_info(3, 0.8)  # 57 %
        count = [0, 0, 0]
        first = 0
        for i in range(1000):
            j: int = memoryContainer.get_info()
            if (i == 0):
                first = j-1
            count[j-1] += 1

        # print("[0]: "+count[0]+" [1]: "+count[1]+" [2]: "+count[2]+" first:"+first)
        for i in range(3):
            if (i == first):
                self.assertEqual(count[i] > 0, True)
            else:
                self.assertEqual(count[i] > 0, False)

        count[0] = 0
        count[1] = 0
        count[2] = 0
        for i in range(1000):
            memoryContainer.set_info(1, 0.2, n)
            j: int = memoryContainer.get_info()
            count[j-1] += 1

        # print("[0]: "+count[0]+" [1]: "+count[1]+" [2]: "+count[2])
        self.assertEqual(count[0] < count[1], True)
        self.assertEqual(count[1] < count[2], True)

    def test_random_flat(self) -> None:
        memoryContainer = MemoryContainer("RANDOMFLAT")
        memoryContainer.setPolicy(Policy.RANDOM_FLAT)
        memoryContainer.set_info(1, 0.2)  # 14 %
        memoryContainer.set_info(2, 0.4)  # 28 %
        memoryContainer.set_info(3, 0.8)  # 57 %
        count = [0, 0, 0]
        for i in range(1000):
            j: int = memoryContainer.get_info()
            count[j-1] += 1

        self.assertEqual(count[0] > 0, True)
        self.assertEqual(count[1] > 0, True)
        self.assertEqual(count[2] > 0, True)

    def test_random_flat_stable(self) -> None:
        memoryContainer = MemoryContainer("RANDOMFLATSTABLE")
        memoryContainer.setPolicy(Policy.RANDOM_FLAT_STABLE)
        n1 = memoryContainer.set_info(1, 0.2)  # 14 %
        memoryContainer.set_info(2, 0.4)  # 28 %
        memoryContainer.set_info(3, 0.8)  # 57 %
        count = [0, 0, 0]
        first = 0
        for i in range(1000):
            j: int = memoryContainer.get_info()
            if (i == 0):
                first = j-1
            count[j-1] += 1

        for i in range(3):
            if (i == first):
                self.assertEqual(count[i] > 0, True)
            else:
                self.assertEqual(count[i] > 0, False)

        count[0] = 0
        count[1] = 0
        count[2] = 0
        for i in range(1000):
            memoryContainer.set_info(1, 0.2, n1)
            j: int = memoryContainer.get_info()
            if (i == 0):
                first = j-1
            count[j-1] += 1

        self.assertEqual(count[0] > 0, True)
        self.assertEqual(count[1] > 0, True)
        self.assertEqual(count[2] > 0, True)

    def test_iterate_policy(self) -> None:
        memoryContainer = MemoryContainer("ITERATE")
        memoryContainer.setPolicy(Policy.ITERATE)
        print("-- This test will raise a warning ...")
        k: int = memoryContainer.get_info()
        self.assertIsNone(k)
        memoryContainer.set_info(1)
        memoryContainer.set_info(2)
        memoryContainer.set_info(3)
        for i in range(9):
            j: int = memoryContainer.get_info()
            self.assertEqual(j, i % 3+1)

    def test_get_evaluation(self) -> None:
        memoryContainer = MemoryContainer("TEST")
        self.assertEqual(memoryContainer.get(-1), None)
        self.assertEqual(memoryContainer.get(0), None)
        self.assertEqual(memoryContainer.get(10), None)
        self.assertEqual(memoryContainer.get_name(), "TEST")
        memoryContainer.set_name("TEST-NEW")
        self.assertEqual(memoryContainer.get_name(), "TEST-NEW")
        memoryContainer.setType("TEST-NEW")
        self.assertEqual(memoryContainer.get_name(), "TEST-NEW")
        # Testing the getEvaluation without any included MemoryObject
        self.assertEqual(memoryContainer.get_evaluation(), None)
        self.assertEqual(memoryContainer.get_evaluation(0), None)
        self.assertEqual(memoryContainer.get_evaluation(1), None)
        self.assertEqual(memoryContainer.getPolicy(), Policy.MAX)
        res: float = memoryContainer.get_evaluation()
        self.assertEqual(res, None)
        memoryContainer.set_info(1)
        memoryContainer.set_evaluation(0.5)
        self.assertEqual(memoryContainer.get_evaluation(), 0.5)
        self.assertEqual(memoryContainer.get_evaluation(0), 0.5)
        memoryContainer.setPolicy(Policy.ITERATE)
        self.assertEqual(memoryContainer.getPolicy(), Policy.ITERATE)
        i: int = memoryContainer.get_info()
        self.assertEqual(i, 1)
        i: int = memoryContainer.getLastI()
        self.assertEqual(i, 1)
        mo: MemoryObject = memoryContainer.getLast()
        i: int = mo.get_info()
        self.assertEqual(i, 1)
        memoryContainer.set_evaluation(0.6, 0)
        self.assertEqual(memoryContainer.get_evaluation(), 0.6)
        self.assertEqual(memoryContainer.get_evaluation(0), 0.6)

    def test_get_timestamp(self) -> None:
        memoryContainer = MemoryContainer("TEST")
        # Without any initialization, the timestamp must be None
        self.assertEqual(memoryContainer.get_timestamp(), None)
        print("This test will raise a warning...")
        self.assertEqual(memoryContainer.get_timestamp(0), None)
        print("This test will raise a warning...")
        self.assertEqual(memoryContainer.get_timestamp(1), None)
        # after we initialize the container, the timestamp must be something different from None
        memoryContainer.set_info(1)
        self.assertEqual(memoryContainer.get_timestamp() != None, True)
        self.assertEqual(memoryContainer.get_timestamp(0) != None, True)
        # nevertheless, if we go further, it should remain None
        print("This test will raise a warning...")
        self.assertEqual(memoryContainer.get_timestamp(1), None)
        self.assertEqual(memoryContainer.get(
            0).get_info(), memoryContainer.get_info())

    def test_double_indirection(self) -> None:
        mc1: MemoryContainer = MemoryContainer("TEST1")
        mc2: MemoryContainer = MemoryContainer("TEST2")
        mc2.set_info(0)
        mc1.add(mc2)
        self.assertEqual(mc1.get_info(), 0)
        mc1.set_info(1, 0.5, 0)
        self.assertEqual(mc1.get_info(), 1)
        mc1.set_evaluation(0.6, 0)
        self.assertEqual(mc1.get_evaluation(), 0.6)
