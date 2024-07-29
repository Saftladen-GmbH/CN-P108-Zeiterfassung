import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
# Module imports here
from app import *


def test_test():
    assert 1 == 1, "1 is not equal to 1"


if __name__ == '__main__':
    pytest.main()
