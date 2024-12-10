import os
import json

from testbook import testbook
from testbook.client import TestbookNotebookClient

from ..utils import get_examples_path

examples_path = get_examples_path()

@testbook(os.path.join(examples_path, "Introduction to CST-Python.ipynb"), execute=True)
def test_introduction(tb :TestbookNotebookClient):
    result = tb.cell_output_text("check_interface")
    assert result == "True"

    result = tb.cell_output_text("basic_memory_members")
    assert result == "(0, 'My Memory')"

    result = tb.cell_output_text("check_empty_memory")
    assert result == "True"

    result = tb.cell_output_text("set_info")
    assert result == "-1"

    result = tb.cell_output_text("check_info_change")
    result = eval(result)
    assert result[0] == "My Memory's data"

    result = tb.cell_output_text("check_codelet_working")
    assert result == "1"

    result = tb.cell_output_text("check_mind_scheduling")
    assert result == "1"

    result = tb.cell_output_text("example_change_memory")
    assert result == "124"


