#crypto_utils.py
import base64

from ecdsa import VerifyingKey, BadSignatureError
from mnemonic import Mnemonic
from ecdsa import SigningKey, SECP256k1
import hashlib
import base58

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

def is_base64(s):
    try:
        base64.b64decode(s)
        return True
    except Exception:
        return False

def sign_message(private_key, message):
    """ Signs a message using the private key. """
    return private_key.sign(message.encode('utf-8'))

def verify_message_signature(compressed_public_key, message, signature):
    """
    Verifies the signature from the message using a Base58 encoded compressed public key.
    """
    try:
        public_key = decompress_public_key(compressed_public_key)
        # Check if signature is base64 encoded and decode if necessary
        if is_base64(signature):
            signature = base64.b64decode(signature)
        return public_key.verify(signature, message.encode('utf-8'))
    except (BadSignatureError, ValueError, TypeError):
        return False

def create_user_ID(public_key):
    """
    Generates an user_id (I)D from the compressed public key with a specified prefix and a checksum.

    :param public_key: The public key to be used.
    :return: A string representing the user_id with the prefix and checksum.
    """

    prefix = "MC" # prefix to be added to the user_id. MC as MinutoCash
    compressed_key = compress_public_key(public_key)
    address = prefix + compressed_key
    checksum = base58.b58encode(hashlib.sha256(address.encode()).digest()).decode()[-4:]

    # add checksum
    full_address = address + checksum
    return full_address

def verify_user_ID(user_id):
    """
    Verifies the checksum of a given user id.

    :param user_id: The address whose checksum is to be verified.
    :return: True if the checksum is valid, False otherwise.
    """
    # Split the user_id into the main part and the checksum
    main_part, checksum = user_id[:-4], user_id[-4:]

    # Calculate the new checksum from the main part of the user_id
    new_checksum = base58.b58encode(hashlib.sha256(main_part.encode()).digest()).decode()[-4:]

    # Compare the calculated checksum with the one in the user_id (both as strings)
    return new_checksum == checksum

def extract_compressed_pubkey_from_public_ID(public_ID):
    """
    Extracts the compressed public key from a public ID.

    :param public_ID: The public ID from which the compressed public key is to be extracted.
    :return: A string representing the compressed public key.
    """
    prefix = "MC"  # The prefix used in the public ID
    prefix_length = len(prefix)
    # Assuming the checksum is always 4 characters long
    checksum_length = 4

    # Extract the compressed public key (between the prefix and the checksum)
    compressed_pubkey = public_ID[prefix_length:-checksum_length]
    return compressed_pubkey


def compress_public_key(public_key):
    """
    Encodes the public key in its compressed form to a Base58 string.

    :param public_key: The public key to be compressed and encoded.
    :return: A Base58 encoded string of the compressed public key.
    """
    public_key_bytes = public_key.to_string("compressed")  # compressed format
    return base58.b58encode(public_key_bytes).decode()

def decompress_public_key(compressed_public_key):
    """
    Decompresses a Base58 encoded, compressed public key back into a VerifyingKey object.

    :param compressed_public_key: The Base58 encoded, compressed public key.
    :return: A VerifyingKey object.
    """
    public_key_bytes = base58.b58decode(compressed_public_key)
    return VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)


def get_hash(data):
    """
    Calculates the SHA-256 hash of the given data and encodes it in Base58.

    :param data: The data to be hashed. This should be in bytes.
    :return: A Base58 encoded string representing the hash of the data.
    """
    # Berechnen des SHA-256 Hashes
    hash_obj = hashlib.sha256(data)
    hash_digest = hash_obj.digest()

    # Kodierung des Hashes in Base58
    hash_base58 = base58.b58encode(hash_digest)
    return hash_base58.decode()


