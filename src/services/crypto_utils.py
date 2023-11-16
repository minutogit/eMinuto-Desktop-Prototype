from mnemonic import Mnemonic
from ecdsa import SigningKey, SECP256k1
import hashlib
import base58
from Crypto.Hash import RIPEMD160

def generate_seed():
    """ Generates a random seed of 12 words. """
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)

def create_key_pair(seed_words):
    """ Creates a key pair from the seed. """
    mnemo = Mnemonic("english")
    seed_bytes = mnemo.to_seed(seed_words, passphrase="")
    private_key = SigningKey.from_string(seed_bytes[:32], curve=SECP256k1)
    return private_key, private_key.verifying_key

def sign_message(private_key, message):
    """ Signs a message using the private key. """
    return private_key.sign(message.encode('utf-8'))

def verify_signature(public_key, message, signature):
    """ Verifies the signature using the public key. """
    return public_key.verify(signature, message.encode('utf-8'))

def create_public_address(public_key):
    """ Creates a public address (ID) from the public key. """
    public_key_bytes = public_key.to_string("uncompressed")
    sha256_bpk = hashlib.sha256(public_key_bytes)
    ripemd160_bpk = RIPEMD160.new(sha256_bpk.digest())
    encoded_ripemd160_bpk = base58.b58encode(ripemd160_bpk.digest())
    address_with_prefix = "MC" + encoded_ripemd160_bpk.decode()
    checksum = hashlib.sha256(address_with_prefix.encode()).digest()[:4]
    final_address = address_with_prefix + base58.b58encode(checksum).decode()[-4:]
    return final_address

def verify_address_checksum(address):
    """ Verifies the checksum of an address. """
    main_part = address[:-4]
    existing_checksum = address[-4:]
    calculated_checksum = hashlib.sha256(main_part.encode()).digest()[:4]
    calculated_checksum_encoded = base58.b58encode(calculated_checksum).decode()[-4:]
    return calculated_checksum_encoded == existing_checksum
