# %%
import time

import redis

import cst_python as cst
from cst_python.memory_storage import MemoryStorageCodelet

import logging
import sys
import threading

from numpy.testing import assert_array_almost_equal

sleep_time = 0.2

#ch = logging.StreamHandler(sys.stdout)
#ch.setLevel(logging.INFO)
#
#logging.getLogger("MemoryStorageCodelet").addHandler(ch)

client = redis.Redis(decode_responses=True)
client.flushall()

mind = cst.Mind()
memory1 = mind.create_memory_object("Memory1", "")

ms_codelet = MemoryStorageCodelet(mind)
ms_codelet.time_step = 100

mind.insert_codelet(ms_codelet)
mind.start()

assert memory1.get_info() == ""

memory1.set_info([1,1,1])

time.sleep(sleep_time)

members = client.smembers("default_mind:nodes")
assert len(members) == 1
assert "node" in members

result = client.hgetall("default_mind:memories:Memory1")
expected_result = {"name":"Memory1", "evaluation":"0.0", "I":"", "id":"0", "owner":"node", "logical_time":"0"}
assert result == expected_result


mind2 = cst.Mind()
mind2_memory1 = mind2.create_memory_object("Memory1", "")
mind2_ms_codelet = MemoryStorageCodelet(mind2)
mind2_ms_codelet.time_step = 100
mind2.insert_codelet(mind2_ms_codelet)
mind2.start()

assert mind2_memory1.get_info() == ""

assert mind2_ms_codelet._node_name == "node1"

members = client.smembers("default_mind:nodes")
assert len(members) == 2
assert "node" in members
assert "node1" in members

time.sleep(sleep_time)

assert_array_almost_equal(memory1.get_info(), [1,1,1])
assert_array_almost_equal(mind2_memory1.get_info(), [1,1,1])

result = client.hgetall("default_mind:memories:Memory1")
expected_result = {"name":"Memory1", "evaluation":"0.0", "I":"[1, 1, 1]", "id":"0", "owner":""}

assert "logical_time" in result
assert "timestamp" in result
del result["logical_time"]
del result["timestamp"]
assert result == expected_result

memory1.set_info("INFO")
time.sleep(sleep_time)

assert memory1.get_info() == "INFO"
assert mind2_memory1.get_info() == "INFO"

mind2_memory1.set_info("INFO2")
time.sleep(sleep_time)

assert memory1.get_info() == "INFO2"
assert mind2_memory1.get_info() == "INFO2"

memory1.set_info(1)
time.sleep(sleep_time)

assert memory1.get_info() == 1
assert mind2_memory1.get_info() == 1

memory1.set_info("1")
time.sleep(sleep_time)


assert memory1.get_info() == "1"
assert mind2_memory1.get_info() == "1"

memory1.set_info(True)
time.sleep(sleep_time)

assert memory1.get_info() == True
assert mind2_memory1.get_info() == True


mind2_memory1.set_info([1,2,3])
time.sleep(sleep_time)

assert_array_almost_equal(memory1.get_info(), [1,2,3])
assert_array_almost_equal(mind2_memory1.get_info(), [1,2,3])

mind.shutdown()
mind2.shutdown()

time.sleep(sleep_time)
assert threading.active_count() == 1