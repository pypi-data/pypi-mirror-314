import time

import cst_python as cst
from cst_python.memory_storage import MemoryStorageCodelet

import logging
import sys

if __name__ == "__main__":
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    logging.getLogger("MemoryStorageCodelet").addHandler(ch)

    SLEEP_TIME = 0.75

    mind = cst.Mind()
    memory1 = mind.create_memory_object("Memory1", "")

    last_timestamp = memory1.get_timestamp()

    ms = MemoryStorageCodelet(mind)
    ms.time_step = 100
    mind.insert_codelet(ms)

    mind.start()


    valid = False
    for i in range(30):
        time.sleep(0.1)

        if last_timestamp != memory1.get_timestamp() and not memory1.get_info():
            valid = True
            memory1.set_info(True)
            break
        
    time.sleep(SLEEP_TIME)

    assert memory1.get_info() == "JAVA_INFO"

    memory1.set_info("OTHER_INFO")
    time.sleep(SLEEP_TIME)

    assert memory1.get_info() == 1

    memory1.set_info(-1)
    time.sleep(SLEEP_TIME)

    assert memory1.get_info() == 1.0

    memory1.set_info(5.0)
    #time.sleep(SLEEP_TIME)