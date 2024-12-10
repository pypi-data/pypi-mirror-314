import os
import math

from testbook import testbook
from testbook.client import TestbookNotebookClient

from ..utils import get_examples_path

examples_path = get_examples_path()

@testbook(os.path.join(examples_path, "Publisher-Subscriber.ipynb"), execute=True)
def test_publisher_subscriber(tb :TestbookNotebookClient):
    expected_results : list[list] = [10, 15, 10, 15, 10, 15]
    
    for i, excepted_result in enumerate(expected_results): 
        result = tb.cell_output_text(f"check_average{i}")
        result = eval(result)
        
        assert math.isclose(result, excepted_result)