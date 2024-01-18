# secure_file_handler.py
import json
from src.services.crypto_utils import symmetric_decrypt, symmetric_encrypt, generate_shared_secret, extract_compressed_pubkey_from_public_ID
import os
from pathlib import Path


class SecureFileHandler:
    def __init__(self, private_key=None):
        """
        Initialize the SecureFileHandler with an optional private key.

        :param private_key: Optional. The private key used for encryption/decryption.
        """
        self.private_key = private_key
    def encrypt_and_save(self, obj, file_path, password="", second_password=None, key=None, salt=None):
        """
        Encrypts an object using symmetric encryption and saves it to a file.

        :param obj: The object to encrypt.
        :param file_path: Path to the file where the encrypted data will be saved.
        :param password: The password used for encryption.
        """

        # create folder if not exist
        directory = os.path.dirname(file_path)
        Path(directory).mkdir(parents=True, exist_ok=True)

        encrypted_data = symmetric_encrypt(obj, password=password, second_password=second_password, key=key, salt=salt)
        with open(file_path, 'w') as file:
            json.dump(encrypted_data, file)

    def decrypt_and_load(self, file_path, password, obj=None):
        """
        Decrypts data from a file using symmetric encryption.

        :param file_path: Path to the file containing the encrypted data.
        :param password: The password used for decryption.
        :return: The decrypted object.
        """
        with open(file_path, 'r') as file:
            encrypted_data = json.load(file)
        return symmetric_decrypt(encrypted_data, password, obj)

    def encrypt_with_shared_secret_and_save(self, obj, file_path, peer_user_id, private_key=None):
        """
        Encrypts an object with a shared secret derived from ECDH using symmetric encryption and saves it to a file,
        using the encrypt_and_save method.

        :param obj: The object to encrypt.
        :param file_path: Path to the file where the encrypted data will be saved.
        :param private_key: Optional. The private key used in ECDH to generate the shared secret.
                           If not provided, the instance's private key is used.
        :param peer_user_id: The user ID of the peer with whom communication is intended.
        """
        if private_key is None:
            private_key = self.private_key

        if private_key is None:
            raise ValueError("Private key is required but not provided.")

        peer_compressed_public_key = extract_compressed_pubkey_from_public_ID(peer_user_id)
        shared_secret = generate_shared_secret(private_key, peer_compressed_public_key)
        self.encrypt_and_save(obj, file_path, shared_secret)

    def decrypt_with_shared_secret_and_load(self, file_path, peer_user_id, private_key=None, obj=None):
        """
        Decrypts data from a file using a shared secret derived from ECDH with symmetric encryption,
        using the decrypt_and_load method.

        :param file_path: Path to the file containing the encrypted data.
        :param private_key: Optional. The private key used in ECDH to generate the shared secret.
                            If not provided, the instance's private key is used.
        :param peer_user_id: The user ID of the peer with whom communication is intended.
        :return: The decrypted object.
        """
        if private_key is None:
            private_key = self.private_key

        if private_key is None:
            raise ValueError("Private key is required but not provided.")

        peer_compressed_public_key = extract_compressed_pubkey_from_public_ID(peer_user_id)
        shared_secret = generate_shared_secret(private_key, peer_compressed_public_key)
        return self.decrypt_and_load(file_path, shared_secret, obj)

