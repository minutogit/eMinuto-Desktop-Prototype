#crypto_utils.py
import base64

from cryptography.exceptions import InvalidSignature
from mnemonic import Mnemonic
import hashlib
import base58
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey

# Elliptic curve cryptography from:
#https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#

def generate_seed():
    """ Generates a random seed of 12 words. """
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)

def create_key_pair(seed_words):
    """ Creates a key pair from the seed. """
    mnemo = Mnemonic("english")
    seed_bytes = mnemo.to_seed(seed_words, passphrase="")
    seed_int = int.from_bytes(seed_bytes[:32], byteorder='big')
    private_key = ec.derive_private_key(seed_int, ec.SECP384R1())
    return private_key, private_key.public_key()

def is_base64(s):
    try:
        base64.b64decode(s)
        return True
    except Exception:
        return False

def sign_message(private_key, message):
    """ Signs a message using the private key. """
    return private_key.sign(message.encode('utf-8'),ec.ECDSA(hashes.SHA256()))


def verify_message_signature(compressed_public_key, message, signature):
    """
    Verifies the signature from the message using a Base58 encoded compressed public key.
    """
    try:
        public_key = decompress_public_key(compressed_public_key)
        # Check if signature is base64 encoded and decode if necessary
        if is_base64(signature):
            signature = base64.b64decode(signature)

        # Attempt to verify the signature
        public_key.verify(signature, message.encode('utf-8'), ec.ECDSA(hashes.SHA256()))

        # If no exception occurs, the signature is valid
        return True
    except Exception:
        # If an InvalidSignature error occurs, the signature is invalid
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
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.CompressedPoint
    )
    return base58.b58encode(public_key_bytes).decode()


def decompress_public_key(compressed_public_key):
    """
    Decompresses a Base58 encoded, compressed public key back into a VerifyingKey object.

    :param compressed_public_key: The Base58 encoded, compressed public key.
    :return: A VerifyingKey object.
    """
    public_key_bytes = base58.b58decode(compressed_public_key)
    return EllipticCurvePublicKey.from_encoded_point(ec.SECP384R1(), public_key_bytes)


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

def generate_shared_secret(private_key, peer_compressed_public_key):
    """
    Generates a shared secret using Elliptic Curve Diffie-Hellman Key Exchange (ECDH).

    Parameters:
    private_key (EllipticCurvePrivateKey): The private key for ECDH exchange.
    peer_public_key (EllipticCurvePublicKey): The compressed public key of the peer for ECDH exchange.

    Returns:
    bytes: The generated shared secret.
    """
    # Perform the ECDH exchange to generate the shared secret
    peer_public_key = decompress_public_key(peer_compressed_public_key)
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    return shared_secret

def generate_symmetric_key(password, salt=None):
    """
    Generates a symmetric key using a password and an optional salt.
    """
    if salt is None:
        salt = get_random_bytes(16)
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
    return key, salt


def symmetric_encrypt(data, password):
    """
    Encrypts data symmetrically using AES with a password.
    Converts byte objects to Base64 strings for JSON serialization.
    """
    key, salt = generate_symmetric_key(password)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(data).encode())
    return {
        'ciphertext': base64.b64encode(ciphertext).decode(),  # Konvertiert zu Base64 String
        'tag': base64.b64encode(tag).decode(),
        'nonce': base64.b64encode(cipher.nonce).decode(),
        'salt': base64.b64encode(salt).decode()
    }


def symmetric_decrypt(encrypted_data, password):
    """
    Decrypts data that was encrypted symmetrically using AES with a password.
    Converts Base64 strings back to byte objects before decryption.
    """
    key, _ = generate_symmetric_key(password, salt=base64.b64decode(encrypted_data['salt']))
    cipher = AES.new(key, AES.MODE_GCM, nonce=base64.b64decode(encrypted_data['nonce']))
    plaintext = cipher.decrypt_and_verify(base64.b64decode(encrypted_data['ciphertext']), base64.b64decode(encrypted_data['tag']))
    return json.loads(plaintext.decode())
