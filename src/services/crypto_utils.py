#crypto_utils.py
import base64

from ecdsa import VerifyingKey, BadSignatureError
from mnemonic import Mnemonic
from ecdsa import SigningKey, SECP256k1
import hashlib
import base58
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import json
from ecdsa.util import randrange_from_seed__trytryagain

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



import secrets

def hybrid_encrypt(data, public_IDs, password=None):
    """
    Encrypts data using a hybrid approach - symmetric encryption with AES and asymmetric for the key.
    Generates a secure random password if none is provided.
    """
    if password is None:
        password = secrets.token_bytes(32)  # Generiert ein sicheres zufälliges 32-Byte Passwort

    encrypted_passwords = []
    for public_ID in public_IDs:
        compressed_pubkey = extract_compressed_pubkey_from_public_ID(public_ID)
        public_key = decompress_public_key(compressed_pubkey)
        encrypted_password = public_key.encrypt(password)
        encrypted_passwords.append(base64.b64encode(encrypted_password).decode())  # Konvertiert zu Base64 String

    encrypted_data = symmetric_encrypt(data, password)
    return {'encrypted_passwords': encrypted_passwords, 'encrypted_data': encrypted_data}



def hybrid_decrypt(encrypted_file, private_key):
    """
    Decrypts data that was encrypted using the hybrid method.
    """
    for encrypted_password in encrypted_file['encrypted_passwords']:
        try:
            password = private_key.decrypt(encrypted_password)
            return symmetric_decrypt(encrypted_file['encrypted_data'], password)
        except Exception:
            continue
    raise Exception("Decryption failed with the provided private key.")

