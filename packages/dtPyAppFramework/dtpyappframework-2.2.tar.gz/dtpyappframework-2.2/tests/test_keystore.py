import base64
import json
import os
from unittest import mock

import pytest
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# Import the class to test
from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC

# The path to a temporary file for testing purposes
TEMP_FILE_PATH = "/tmp/test_keystore.db"


def teardown_function(function):
    if os.path.exists(TEMP_FILE_PATH):
        os.remove(TEMP_FILE_PATH)


@pytest.fixture
def keystore():
    return PasswordProtectedKeystoreWithHMAC(TEMP_FILE_PATH, 'test_password')


def test_init(keystore):
    assert keystore.keystore_path == TEMP_FILE_PATH
    assert keystore.password == 'test_password'.encode()


def test_derive_key(keystore):
    salt = os.urandom(16)
    key = keystore._derive_key(salt)
    assert (isinstance(key, bytes))
    assert (len(key) == 44)  # Length of base64 encoded 256-bit key


def test_generate_hmac(keystore):
    salt = os.urandom(16)
    key = keystore._derive_key(salt)
    data = os.urandom(16)
    hmac = keystore._generate_hmac(data, key)
    assert (isinstance(hmac, bytes))
    assert (len(hmac) == 32)  # Length of SHA256 hash


def test_verify_hmac(keystore):
    salt = os.urandom(16)
    key = keystore._derive_key(salt)
    data = os.urandom(16)
    hmac = keystore._generate_hmac(data, key)
    assert keystore._verify_hmac(data, key, hmac) is True


def test_save_and_load_keystore(keystore):
    test_data = {"test_key": "test_value"}
    keystore._save_keystore(test_data)
    loaded_data = keystore._load_keystore()

    assert loaded_data == test_data


def test_set_get_delete_methods(keystore):
    keystore.set("test_key", "test_value")
    assert keystore.get("test_key") == "test_value"
    keystore.delete("test_key")
    assert keystore.get("test_key") is None
