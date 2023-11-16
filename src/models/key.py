from src.services.crypto_utils import (
    generate_seed, 
    create_key_pair, 
    create_public_address,
    sign_message, 
    verify_signature
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

    def sign(self, message):
        """ Sign a message using the private key. """
        return sign_message(self.private_key, message)

    def verify(self, message, signature):
        """ Verify a signature using the public key. """
        return verify_signature(self.public_key, message, signature)

    def __str__(self):
        return f"Key(Public Address: {self.id}, Seed Words: {self.seed_words})"
