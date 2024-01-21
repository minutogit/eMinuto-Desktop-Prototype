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

    def encrypt_with_shared_secret_and_save(self, obj, file_path, peer_user_id, own_user_id=None, private_key=None):
        """
        Encrypts an object with a shared secret derived from ECDH using symmetric encryption and saves it to a file,
        using the encrypt_and_save method. Optionally, encrypts and appends the own user ID with a special marker.

        Args:
            obj (Serializable or dict): The object to encrypt.
            file_path (str): Path to the file where the encrypted data will be saved.
            peer_user_id (str): The user ID of the peer with whom communication is intended.
            private_key (bytes, optional): The private key used in ECDH to generate the shared secret.
                                          If not provided, the instance's private key is used.
            own_user_id (str, optional): The own user ID to encrypt and append to the encrypted data.

        Raises:
            ValueError: If the private key is not provided and not set in the instance.
        """
        if private_key is None:
            private_key = self.private_key

        if private_key is None:
            raise ValueError("Private key is required but not provided.")

        peer_compressed_public_key = extract_compressed_pubkey_from_public_ID(peer_user_id)
        shared_secret = generate_shared_secret(private_key, peer_compressed_public_key)

        encrypted_data = symmetric_encrypt(obj, password=shared_secret)

        # Encrypt and append the own user ID with a special marker if provided
        if own_user_id is not None:
            encrypted_own_user_id = symmetric_encrypt(own_user_id, password=peer_user_id)
            encrypted_data += '@' + encrypted_own_user_id

        with open(file_path, 'w') as file:
            file.write(encrypted_data)

    def decrypt_with_shared_secret_and_load(self, file_path, peer_user_id=None, own_user_id=None, private_key=None,
                                            obj=None):
        """
        Decrypts data from a file using a shared secret derived from ECDH with symmetric encryption.
        If 'peer_user_id' is not provided, attempts to decrypt and extract it using 'own_user_id'.
        The function handles data optionally appended with an encrypted 'own_user_id'.

        Args:
            file_path (str): Path to the file containing the encrypted data.
            peer_user_id (str, optional): The user ID of the peer. Used if provided.
            own_user_id (str, optional): The own user ID used to decrypt the peer user ID if it is not provided.
            private_key (bytes, optional): The private key used in ECDH to generate the shared secret.
                                          If not provided, the instance's private key is used.
            obj (Serializable or dict, optional): The object type to which the decrypted data will be converted.

        Returns:
            Serializable or dict: The decrypted object.

        Raises:
            ValueError: If the private key is not provided and not set in the instance.
        """
        if private_key is None:
            private_key = self.private_key

        if private_key is None:
            raise ValueError("Private key is required but not provided.")

        with open(file_path, 'r') as file:
            encrypted_data = file.read()

        # Check for the special marker '@' and extract encrypted user ID if present
        uid_marker = '@'
        if uid_marker in encrypted_data:
            encrypted_data, encrypted_own_user_id = encrypted_data.split(uid_marker, 1)
            if not peer_user_id and own_user_id:
                # Decrypt the peer_user_id using the own_user_id
                peer_user_id = symmetric_decrypt(encrypted_own_user_id, password=own_user_id)

        if peer_user_id:
            peer_compressed_public_key = extract_compressed_pubkey_from_public_ID(peer_user_id)
            shared_secret = generate_shared_secret(private_key, peer_compressed_public_key)
        else:
            raise ValueError("Peer user ID could not be determined for decryption.")

        return symmetric_decrypt(encrypted_data, shared_secret, obj)


