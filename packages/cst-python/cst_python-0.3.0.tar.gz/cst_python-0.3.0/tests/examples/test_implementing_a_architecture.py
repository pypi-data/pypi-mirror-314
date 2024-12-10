import os
import math

from testbook import testbook
from testbook.client import TestbookNotebookClient

from ..utils import get_examples_path

examples_path = get_examples_path()

@testbook(os.path.join(examples_path, "Implementing a Architecture.ipynb"), execute=True)
def test_implementing_architecture(tb :TestbookNotebookClient):
    expected_results : list[list] = [["nan", "nan"],
                        [0, 0],
                        [-0, 2],
                        [3,3]]
    
    for i, excepted_result in enumerate(expected_results): 
        result = tb.cell_output_text(f"equation{i+1}")
        result = result.replace("nan", "'nan'")
        result = eval(result)

        for x in result:
            for y in excepted_result:
                if isinstance(x, str) or isinstance(y,str):
                    if isinstance(x, str) and isinstance(y,str) and x == y:
                            excepted_result.remove(y)
                            break
                    
                elif math.isclose(x, y):
                    excepted_result.remove(y)
                    break
        
        assert len(excepted_result) == 0



