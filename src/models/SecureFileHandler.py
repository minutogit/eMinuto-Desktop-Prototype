import json
from src.services.crypto_utils import symmetric_decrypt, symmetric_encrypt, hybrid_decrypt, hybrid_encrypt

class SecureFileHandler:
    def encrypt_and_save(self, obj, password, file_path):
        """
        Encrypts an object using symmetric encryption and saves it to a file.

        :param obj: The object to encrypt.
        :param password: The password used for encryption.
        :param file_path: Path to the file where the encrypted data will be saved.
        """
        encrypted_data = symmetric_encrypt(obj, password)
        with open(file_path, 'w') as file:
            json.dump(encrypted_data, file)

    def decrypt_and_load(self, file_path, password):
        """
        Decrypts data from a file using symmetric encryption.

        :param file_path: Path to the file containing the encrypted data.
        :param password: The password used for decryption.
        :return: The decrypted object.
        """
        with open(file_path, 'r') as file:
            encrypted_data = json.load(file)
        return symmetric_decrypt(encrypted_data, password)

    def hybrid_encrypt_and_save(self, obj, public_IDs, file_path):
        """
        Encrypts an object using hybrid encryption and saves it to a file.

        :param obj: The object to encrypt.
        :param public_IDs: A list of public IDs used for the hybrid encryption.
        :param file_path: Path to the file where the encrypted data will be saved.
        """
        encrypted_file = hybrid_encrypt(obj, public_IDs)
        with open(file_path, 'w') as file:
            json.dump(encrypted_file, file)

    def hybrid_decrypt_and_load(self, file_path, private_key):
        """
        Decrypts data from a file using hybrid encryption.

        :param file_path: Path to the file containing the encrypted data.
        :param private_key: The private key used for decryption.
        :return: The decrypted object.
        """
        with open(file_path, 'r') as file:
            encrypted_file = json.load(file)
        return hybrid_decrypt(encrypted_file, private_key)

