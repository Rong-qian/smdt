###############################################################################
#   File: test_data.py
#   Author(s): Paul Johnecheck
#   Date Created: 19 April, 2021
#
#   Purpose: This is the parent class of the various station's tests.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])


class TestData:
    def __init__(self):
        pass

    def fail(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
