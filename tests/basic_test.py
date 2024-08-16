import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
# Module imports here
from utility import *


def test_test():
    assert 1 == 1, "1 is not equal to 1"


def test_random_password():
    pw = random_password()
    assert len(pw) == 10, "Password length is not 10"
    assert not pw.isalnum(), "Password contains no special characters"


def test_hash_password():
    pw = "password"
    hashed_pw = hash_password(pw)
    assert hashed_pw != pw, "Password is not hashed"


def test_verify_password():
    pw = "password"
    hashed_pw = hash_password(pw)
    assert verify_password(hashed_pw, pw), "Password verification failed"
