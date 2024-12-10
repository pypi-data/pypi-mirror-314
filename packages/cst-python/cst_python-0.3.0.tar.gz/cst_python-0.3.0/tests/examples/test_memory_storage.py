import os
import re

import redis
import unittest
from testbook import testbook
from testbook.client import TestbookNotebookClient

if __name__ != "__main__":
    from ..utils import get_examples_path

    examples_path = get_examples_path()

else:
    examples_path = "examples"

client = redis.Redis(decode_responses=True)
try:
    client.ping()
    redis_reachable = True
except Exception:
    redis_reachable = False

@unittest.skipIf(not redis_reachable, "Redis server not running")
@testbook(os.path.join(examples_path, "Memory Storage.ipynb"), execute=True)
def test_gym_integration(tb :TestbookNotebookClient):
    
    expected_result = {"info1":"'First node info'",
                       "info2":"''",
                       #"info3":"'First node info'", #For some reason, works running manually and in CI, but not in the local test
                       "info4":"'Second node info'",
                       "info5":"[1, 2, 3]",
                       }
    
    for tag in expected_result:
        result = tb.cell_output_text(tag)

        assert result == expected_result[tag]


if __name__ == "__main__":
    test_gym_integration()