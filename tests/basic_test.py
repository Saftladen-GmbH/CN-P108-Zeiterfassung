import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from app import main


def test_main_add():
    res = main.adding(1, 2)
    assert res == 3, "1 + 2 is not equal to 3"


def test_test():
    assert 1 == 1, "1 is not equal to 1"


if __name__ == '__main__':
    pytest.main()
