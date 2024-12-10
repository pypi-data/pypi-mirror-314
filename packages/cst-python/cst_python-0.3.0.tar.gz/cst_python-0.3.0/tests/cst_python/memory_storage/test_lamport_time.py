import functools
import json
import threading
import threading
import time
import types
import unittest
from typing import Any

from cst_python.memory_storage.logical_time import LamportTime

class TestLamportTime(unittest.TestCase):

    def test_initial_time(self):
        time0 = LamportTime(initial_time=123)

        assert time0._time == 123

    def test_str(self):
        time0 = LamportTime(initial_time=456)

        assert str(time0) == "456"

    def test_from_str(self):
        time0 = LamportTime(initial_time=987)
        
        assert LamportTime.from_str(str(time0)) == time0

    def test_increment(self):
        time0 = LamportTime()
        time0_time = time0._time

        time1 = time0.increment()

        assert time0._time == time0_time
        assert time1._time == time0_time+1

    def test_synchronize(self):
        time0 = LamportTime(initial_time=-10)
        time1 = LamportTime(initial_time=55)

        time_s = LamportTime.synchronize(time0, time1)

        assert time_s > time0
        assert time_s > time1
        assert time_s._time == 56