# key.py
import base64

from src.services.crypto_utils import (
    generate_seed,
    create_key_pair,
    create_user_ID,
    sign_message,
    verify_message_signature,
    compress_public_key,
    extract_compressed_pubkey_from_public_ID,
    verify_user_ID
)

class Key:
    def __init__(self, seed_words=None, empty=False):
        if empty:
            self.id = None
            self.private_key = None
            self.public_key = None
            self.seed_words = None
        else:
            self.seed_words = seed_words if seed_words else generate_seed()
            self.private_key, self.public_key = create_key_pair(self.seed_words)
            self.id = self.get_user_id_from_pubkey()

    def sign(self, message, base64_encode=False):
        """
        Sign a message using the private key.
        If base64_encode is True, return the signature in Base64 encoded format.
        """
        signature = sign_message(self.private_key, message)
        if base64_encode:
            return base64.b64encode(signature).decode('utf-8')
        else:
            return signature

    @staticmethod
    def verify_signature(message, signature, public_key):
        """ Verify a signature using the public key. """
        return verify_message_signature(public_key, message, signature)

    def get_compressed_public_key(self):
        """ Returns the compressed form of the public key. """
        if self.public_key:
            return compress_public_key(self.public_key)
        else:
            return None

    def get_user_id_from_pubkey(self):
        """ Returns user ID generated from public key."""
        return create_user_ID(self.public_key)

    @staticmethod
    def get_pubkey_from_id(id):
        """ Returns public key extracted from user ID."""
        return extract_compressed_pubkey_from_public_ID(id)

    @staticmethod
    def check_user_id(user_id):
        """
        Verifies the checksum of a given user id.
        :return: True if the checksum is valid, False otherwise.
        """
        return verify_user_ID(user_id)

    def __str__(self):
        return f"Key(Public Address: {self.id}, Seed Words: {self.seed_words})"
