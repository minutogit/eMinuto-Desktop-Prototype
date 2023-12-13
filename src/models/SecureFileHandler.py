import json
from src.services.crypto_utils import symmetric_decrypt, symmetric_encrypt, generate_shared_secret, extract_compressed_pubkey_from_public_ID
import os
from pathlib import Path


class SecureFileHandler:
    def encrypt_and_save(self, obj, password, file_path):
        """
        Encrypts an object using symmetric encryption and saves it to a file.

        :param obj: The object to encrypt.
        :param password: The password used for encryption.
        :param file_path: Path to the file where the encrypted data will be saved.
        """

        # create folder if not exist
        directory = os.path.dirname(file_path)
        Path(directory).mkdir(parents=True, exist_ok=True)

        encrypted_data = symmetric_encrypt(obj, password)
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

    def encrypt_with_shared_secret_and_save(self, obj, file_path, private_key, peer_user_id):
        """
        Encrypts an object with a shared secret derived from ECDH using symmetric encryption and saves it to a file,
        using the encrypt_and_save method.

        :param obj: The object to encrypt.
        :param file_path: Path to the file where the encrypted data will be saved.
        :param private_key: The private key used in ECDH to generate the shared secret.
        :param peer_user_id: The user ID of the peer with whom communication is intended.

        """
        peer_compressed_public_key = extract_compressed_pubkey_from_public_ID(peer_user_id)
        shared_secret = generate_shared_secret(private_key, peer_compressed_public_key)
        self.encrypt_and_save(obj, shared_secret, file_path)

    def decrypt_with_shared_secret_and_load(self, file_path, private_key, peer_user_id, obj=None):
        """
        Decrypts data from a file using a shared secret derived from ECDH with symmetric encryption,
        using the decrypt_and_load method.

        :param file_path: Path to the file containing the encrypted data.
        :param private_key: The private key used in ECDH to generate the shared secret.
        :param peer_user_id: The user ID of the peer with whom communication is intended.

        :return: The decrypted object.
        """
        peer_compressed_public_key = extract_compressed_pubkey_from_public_ID(peer_user_id)
        shared_secret = generate_shared_secret(private_key, peer_compressed_public_key)
        return self.decrypt_and_load(file_path, shared_secret, obj)

