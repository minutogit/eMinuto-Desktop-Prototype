#crypto_utils.py
import base64
import gzip
import secrets
from src.services.utils import Serializable

from mnemonic import Mnemonic
import hashlib
import base58
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Elliptic curve cryptography from:
#https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#

def generate_seed():
    """ Generates a random seed of 12 words. """
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)

def check_word_seed(seed) -> bool:
    """check if word seed is valid"""
    mnemo = Mnemonic('english')
    return mnemo.check(seed)

def create_key_pair(seed_words):
    """ Creates a key pair from the seed. """
    mnemo = Mnemonic("english")
    seed_bytes = mnemo.to_seed(seed_words, passphrase="")
    seed_int = int.from_bytes(seed_bytes[:32], byteorder='big')
    private_key = ec.derive_private_key(seed_int, ec.SECP384R1())
    return private_key, private_key.public_key()

def b64d(encoded_string):
    """
    Decode a Base64 encoded string.

    Args:
    encoded_string (str): The Base64 encoded string to be decoded.

    Returns:
    bytes: The decoded data as bytes.
    """
    return base64.b64decode(encoded_string)

def b64e(data):
    """
    Encode data to Base64 string.

    Args:
    data (bytes): The data to be encoded in bytes.

    Returns:
    str: The Base64 encoded string.
    """
    return base64.b64encode(data).decode()

def is_base64(s):
    """
    Checks if the given string is composed of characters in the Base64 character set.
    This is a lenient check and does not strictly validate the string as proper Base64-encoded data.
    It's designed to detect strings that are likely to be Base64 without being overly strict,
    which is suitable for the purpose of detection where strict adherence to full Base64 encoding standards
    is not necessary.

    Args:
        s (str): The string to be checked.

    Returns:
        bool: True if the string is composed of Base64 characters, False otherwise.
    """
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
    Calculates the double SHA-256 hash of the given data and encodes it in Base58.
    Double hashing is used to increase the resistance against attacks on the hash function
    and to mitigate potential vulnerabilities.

    Args:
        data (bytes): The data to be hashed. This should be in bytes.

    Returns:
        str: A Base58 encoded string representing the double hash of the data.
    """
    # Calculate the first SHA-256 hash
    first_hash = hashlib.sha256(data).digest()

    # Calculate the second SHA-256 hash on the result of the first hash
    double_hash = hashlib.sha256(first_hash).digest()

    # Encode the double hash in Base58
    hash_base58 = base58.b58encode(double_hash)
    return hash_base58.decode()


def hash_bytes(input_string, length=16):
    """
    Generates a hash from the input string and returns it as bytes truncated to the specified length.

    Args:
        input_string (str): The input string to hash.
        length (int): The desired length of the output bytes. Defaults to 16.

    Returns:
        bytes: The hashed output truncated to the specified length.
    """
    # Calculate the SHA256 hash of the input string
    hash_obj = hashlib.sha256(input_string.encode())

    # Get the hash bytes and truncate to the desired length
    hash_bytes = hash_obj.digest()[:length]

    return hash_bytes

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


def generate_symmetric_key(password, salt=None, b64_string=False):
    """
    Generates a symmetric key using a password and optional salt.

    Args:
        password (str): The password used to generate the key.
        salt (bytes, optional): A salt for the key derivation. If None, a random salt is generated.
        b64_string (bool, optional): If True, both key and salt are returned as Base64 encoded strings. Defaults to False.

    Returns:
        Tuple[str | bytes, str | bytes]: The generated key and salt, either as bytes or Base64 encoded strings.
    """
    if isinstance(password, str):
        password = password.encode()
    if salt is None:
        salt = secrets.token_bytes(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    if b64_string:
        return key.decode(), b64e(salt)

    return key, salt

def symmetric_encrypt(obj, password="", second_password=None, key=None, salt=None):
    """
    Encrypts and compresses the provided object using symmetric encryption and concatenates
    the encrypted data, salt, and optionally the encrypted key, separated by '|'.
    If 'key' is not provided, it is generated using the provided password and optional salt.
    If a second password is provided, the encryption key itself is encrypted with this second password.
    Providing 'key' directly facilitates faster encryption and decryption as the key generation step is skipped.

    Args:
        obj (Serializable or dict): The object to be encrypted.
        password (str, optional): The password used for generating the encryption key. Defaults to an empty string.
        second_password (str, optional): A second password used to encrypt the encryption key.
        key (bytes, optional): Directly provided encryption key for faster processing.
        salt (bytes, optional): Salt used in conjunction with the password to generate the encryption key.

    Returns:
        str: A string containing the base64 encoded encrypted data, salt, and optionally the encrypted key, separated by '|'.
    """
    if password == "" and key == None:
        raise Exception("No key or password provided.")

    if key is not None and not isinstance(key, bytes):
        raise TypeError("Key must be a byte string.")

    if salt is None:
        salt = secrets.token_bytes(16)

    if key is None:
        key, _ = generate_symmetric_key(password, salt)

    f = Fernet(key)
    obj_dict = obj.to_dict() if isinstance(obj, Serializable) else obj
    serialized_data = json.dumps(obj_dict).encode('utf-8')
    compressed_data = gzip.compress(serialized_data)
    encrypted_data = f.encrypt(compressed_data)

    # Encrypt the key with the second password if provided
    if second_password:
        second_key, _ = generate_symmetric_key(second_password, salt)
        f2 = Fernet(second_key)
        encrypted_key = f2.encrypt(key)
        return '|'.join([b64e(encrypted_data), b64e(salt), b64e(encrypted_key)])
    else:
        return '|'.join([b64e(encrypted_data), b64e(salt)])


def symmetric_decrypt(encrypted_string, password="", cls=None, key=None):
    """
    Decrypts and decompresses the given encrypted string, which contains the encrypted data, salt,
    and optionally the encrypted key, separated by '|'. Uses the provided password or directly provided key for decryption.
    If 'key' is provided, it facilitates faster decryption by skipping the key generation step.
    Optionally instantiates and initializes an object of the specified class with the decrypted data.

    Args:
        encrypted_string (str): The encrypted string containing the encrypted payload, salt, and optionally the encrypted key.
        password (str, optional): The password used for generating the decryption key. Defaults to an empty string.
        cls (class, optional): The class to instantiate with the decrypted data.
        key (bytes, optional): Directly provided decryption key for faster processing.

    Returns:
        object or dict: An instance of the specified class initialized with the decrypted data, or a dictionary of the decrypted data.
    """
    parts = encrypted_string.split('|')
    encrypted_data = base64.b64decode(parts[0])
    salt = base64.b64decode(parts[1])
    encrypted_key = base64.b64decode(parts[2]) if len(parts) > 2 else None

    # Try to decrypt the data with the provided or generated key
    if key is None:
        key, _ = generate_symmetric_key(password, salt=salt)
    f = Fernet(key)
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except Exception:
        if encrypted_key is not None:
            # If decryption fails and encrypted key exists, try to decrypt the key
            key, _ = generate_symmetric_key(password, salt=salt)
            f2 = Fernet(key)
            try:
                decrypted_key = f2.decrypt(encrypted_key)
                f_final = Fernet(decrypted_key)
                decrypted_data = f_final.decrypt(encrypted_data)
            except Exception:
                raise Exception("Invalid decryption key, password, or second password")
        else:
            raise Exception("Invalid decryption key or password")

    # Decompressing and then deserializing the object
    decompressed_data = gzip.decompress(decrypted_data)
    deserialized_data = json.loads(decompressed_data.decode('utf-8'))

    if cls:
        # Instantiate an object of the provided class
        obj = cls()
        for k, value in deserialized_data.items():
            setattr(obj, k, value)  # Set each attribute from the deserialized data
        return obj
    else:
        # Return the deserialized dictionary if no class was provided
        return deserialized_data


def is_encrypted_string(s):
    """
    Checks if the given string is formatted as an encrypted string from symmetric_encrypt.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is formatted correctly, False otherwise.
    """
    # Split the string on '@' in case of double encryption
    encrypted_parts = s.split('@')

    for part in encrypted_parts:
        # Split on '|' and check if each segment is a valid base64-encoded string
        segments = part.split('|')

        # Check for correct number of segments
        if len(segments) not in [2, 3]:
            return False

        # Check each segment for valid base64 encoding
        if not all(is_base64(seg) for seg in segments):
            return False

    return True
