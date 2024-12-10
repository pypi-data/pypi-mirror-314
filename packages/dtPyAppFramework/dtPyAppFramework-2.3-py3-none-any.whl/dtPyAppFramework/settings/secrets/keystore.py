import os
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import logging

class PasswordProtectedKeystoreWithHMAC:
    """
    PasswordProtectedKeystoreWithHMAC provides a mechanism to securely store key-value pairs
    in a file. The data is protected using encryption and integrity is ensured by HMAC.

    Methods:
        __init__(keystore_path, password):
            Initializes the keystore with the provided path and password.

        _derive_key(salt):
            Derives an encryption key from the password and salt using PBKDF2.

        _generate_hmac(data, key):
            Generates an HMAC for the given data using the derived key.

        _verify_hmac(data, key, expected_hmac):
            Verifies the HMAC for the given data against the expected HMAC.

        _load_keystore():
            Loads the keystore from the file, verifying its integrity and returning the stored data.

        _save_keystore(data):
            Saves the provided data to the keystore file, including the generated HMAC for integrity.

        set(key, value):
            Adds or updates a key-value pair in the keystore.

        get(key):
            Retrieves a value from the keystore by its key.

        delete(key):
            Deletes a key-value pair from the keystore.
    """
    def __init__(self, keystore_path, password):
        self.keystore_path = keystore_path
        self.password = password.encode()

    def _derive_key(self, salt):
        """
        Args:
            salt: A cryptographic salt used for deriving the key, which should be a byte sequence.

        Returns:
            A base64-encoded, url-safe byte sequence representing the derived cryptographic key.
        """
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=20_000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(self.password))

    def _generate_hmac(self, data, key):
        """
        Args:
            data: The data that needs to be protected with an HMAC.
            key: The cryptographic key used for HMAC generation.
        """
        hmac = HMAC(key, SHA256(), backend=default_backend())
        hmac.update(data)
        return hmac.finalize()

    def _verify_hmac(self, data, key, expected_hmac):
        """
        Args:
            data: The data for which the HMAC is to be verified.
            key: The secret key used for the HMAC generation.
            expected_hmac: The HMAC value that is expected for the provided data and key combination.

        Returns:
            bool: True if the computed HMAC matches the expected HMAC, False otherwise.

        """
        hmac = HMAC(key, SHA256(), backend=default_backend())
        hmac.update(data)
        try:
            hmac.verify(expected_hmac)
            return True
        except:
            return False

    def _load_keystore(self):
        """
        Loads and decrypts the keystore data from a specified file path.

        If the keystore file exists, it reads the file content and extracts the salt,
        encrypted data, and HMAC. The method then derives the key using the extracted
        salt and verifies the HMAC to ensure data integrity. If the HMAC verification
        fails, a ValueError is raised indicating potential file tampering. After successful
        verification, the method decrypts the data using the derived key and
        returns the decrypted JSON content. If the file does not exist, an empty
        dictionary is returned.

        Raises:
            ValueError: If HMAC verification fails, indicating possible tampering.

        Returns:
            dict: The decrypted content of the keystore file as a dictionary, or an
            empty dictionary if the keystore file does not exist.
        """
        if os.path.exists(self.keystore_path):
            with open(self.keystore_path, 'rb') as file:
                # Read the entire file content
                file_content = file.read()

                # Extract the salt, encrypted data, and HMAC
                salt = file_content[:16]  # First 16 bytes
                encrypted_data = file_content[16:-32]  # Middle bytes
                stored_hmac = file_content[-32:]  # Last 32 bytes

                # Derive the key and verify the HMAC
                derived_key = self._derive_key(salt)
                if not self._verify_hmac(salt + encrypted_data, derived_key, stored_hmac):
                    raise ValueError("HMAC verification failed: File may have been tampered with.")

                # Decrypt the data
                cipher_suite = Fernet(derived_key)
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
        return {}

    def _save_keystore(self, data):
        """
        Args:
            data: The data to be saved in the keystore, which will be encrypted and stored securely.
        """
        # Generate a random 16-byte salt
        salt = os.urandom(16)

        # Derive the key
        derived_key = self._derive_key(salt)
        cipher_suite = Fernet(derived_key)

        # Encrypt the data
        encrypted_data = cipher_suite.encrypt(json.dumps(data).encode())

        # Generate the HMAC
        hmac = self._generate_hmac(salt + encrypted_data, derived_key)

        # Write the salt, encrypted data, and HMAC to the file
        with open(self.keystore_path, 'wb') as file:
            file.write(salt)
            file.write(encrypted_data)
            file.write(hmac)

    def set(self, key, value):
        """
        Args:
            key: The key to be stored in the keystore.
            value: The value associated with the key to be stored.
        """
        keystore = self._load_keystore()
        keystore[key] = value
        self._save_keystore(keystore)
        logging.debug(f"Key '{key}' stored successfully.")

    def get(self, key):
        """
        Retrieves the value associated with the specified key from the keystore.

        Args:
            key: The key whose associated value is to be returned.

        Returns:
            The value corresponding to the specified key if it exists, otherwise None.
        """
        keystore = self._load_keystore()
        logging.debug(f"Retrieving Key '{key}'")
        return keystore.get(key)

    def delete(self, key):
        """
        Deletes the specified key from the keystore if it exists.

        Args:
            key: The key to be deleted from the keystore.
        """
        keystore = self._load_keystore()
        if key in keystore:
            del keystore[key]
            self._save_keystore(keystore)
            logging.debug(f"Key '{key}' deleted successfully.")
        else:
            logging.debug(f"Key '{key}' not found in the keystore.")