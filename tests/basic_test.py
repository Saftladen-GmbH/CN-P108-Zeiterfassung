import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
# Module imports here
from utility import (random_password,
                     hash_password,
                     verify_password,
                     image2blob,
                     blob2image)


def test_test():
    assert 1 == 1, "1 is not equal to 1"


def test_image2blob():
    image_path = "tests/test_image.png"
    blob = image2blob(image_path)
    assert isinstance(blob, bytes), "Blob is not of type bytes"


def test_blob2image():
    image_path = "tests/test_image.png"
    blob = image2blob(image_path)
    blob2image(blob, "tests/test_image_copy.png")
    assert os.path.exists("tests/test_image_copy.png"), "Image not saved"
    os.remove("tests/test_image_copy.png")


def test_random_password():
    pw = random_password()
    assert len(pw) == 10, "Password length is not 10"


def test_hash_password():
    pw = "password"
    hashed_pw = hash_password(pw)
    assert hashed_pw != pw, "Password is not hashed"


def test_verify_password():
    pw = "password"
    hashed_pw = hash_password(pw)
    assert verify_password(hashed_pw, pw), "Password verification failed"
