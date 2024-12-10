import os
import math

import numpy as np
from testbook import testbook
from testbook.client import TestbookNotebookClient

from ..utils import get_examples_path

examples_path = get_examples_path()

@testbook(os.path.join(examples_path, "Activation and Monitoring.ipynb"), execute=True)
def test_activation(tb :TestbookNotebookClient):
    activation_hist = tb.ref("activation_hist.tolist()")
    input_hist = tb.ref("input_hist.tolist()")
    sensory_output_hist = tb.ref("sensory_output_hist.tolist()")
    action_hist = tb.ref("action_hist.tolist()")

    last_sensory_output = sensory_output_hist[0]
    for i, (activation, input_value, sensory_output, action) in enumerate(zip(activation_hist, input_hist, sensory_output_hist, action_hist)):
        assert math.isclose(input_value, i/100)

        assert math.isclose(activation, np.clip(input_value, 0.0, 1.0), abs_tol=0.04)

        if i >= 50 and activation < 0.7:
            expected_sensory = last_sensory_output
        else:
             expected_sensory = input_value * 10

        assert math.isclose(sensory_output, expected_sensory, abs_tol=0.35)

        last_sensory_output = sensory_output

    assert math.isclose(action_hist[0], True )
    assert math.isclose(action_hist[55], False )
    assert math.isclose(action_hist[-1], True )