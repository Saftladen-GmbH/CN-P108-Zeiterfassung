import pytest
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from app import create_app

def test_app_existence():
    assert create_app