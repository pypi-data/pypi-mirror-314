import os
import re

from testbook import testbook
from testbook.client import TestbookNotebookClient

from ..utils import get_examples_path

examples_path = get_examples_path()

@testbook(os.path.join(examples_path, "Gymnasium Integration.ipynb"), execute=True)
def test_gym_integration(tb :TestbookNotebookClient):
    
    expected_result = {"observation0":"{'observation': MemoryObject [idmemoryobject=0, timestamp=, evaluation=0.0, I=(15, 2, 0), name=observation]}",
                       "observation1":"(15, 2, 0)",
                       "step_count":"0",
                       "action0":"{'action': MemoryObject [idmemoryobject=1, timestamp=, evaluation=0.0, I=, name=action]}",
                       "step_count+observation0":"(1, (25, 2, 0))",
                       "terminated0":"True",
                       "reward0":"-1.0",
                       "observation2":"(15, 2, 0)",
                       "observation3":"(15, 2, 0)",
                       "terminated+reward0":"(True, 1.0)",

                       "observation4":'''{'dealer_card': MemoryObject [idmemoryobject=0, timestamp=, evaluation=0.0, I=2, name=dealer_card],
 'player_sum': MemoryObject [idmemoryobject=1, timestamp=, evaluation=0.0, I=15, name=player_sum],
 'usable_ace': MemoryObject [idmemoryobject=2, timestamp=, evaluation=0.0, I=0, name=usable_ace]}''',

                        "observation5":"{'dealer_card': 2, 'player_sum': 15, 'usable_ace': 0}",
                        "action1":"{'hit': MemoryObject [idmemoryobject=3, timestamp=, evaluation=0.0, I=, name=hit]}",
                        "terminated+reward1":"(True, 1.0)"
                       }
    
    clear_info = ["action0", "action1"]

    for tag in expected_result:
        result = tb.cell_output_text(tag)
        result = re.sub(r"timestamp=[0-9]+", "timestamp=", result)
        
        if tag in clear_info:
            result = re.sub(r"I=[0-9]+", "I=", result)

        assert result == expected_result[tag]


