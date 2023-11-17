# key.py
import base64

from src.services.crypto_utils import (
    generate_seed, 
    create_key_pair, 
    create_public_address,
    sign_message, 
    verify_signature,
    compress_public_key
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
            self.id = create_public_address(self.public_key)

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

    def verify(self, message, signature):
        """ Verify a signature using the public key. """
        return verify_signature(self.public_key, message, signature)

    def get_compressed_public_key(self):
        """ Returns the compressed form of the public key. """
        if self.public_key:
            return compress_public_key(self.public_key)
        else:
            return None

    def __str__(self):
        return f"Key(Public Address: {self.id}, Seed Words: {self.seed_words})"
