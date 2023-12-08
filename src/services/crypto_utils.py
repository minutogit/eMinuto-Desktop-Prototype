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
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key, salt


def generate_symmetric_key(password, salt=None):

    if isinstance(password, str):
        password = password.encode()
    if salt is None:
        salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key, salt

def symmetric_encrypt(obj, password):
    key, salt = generate_symmetric_key(password)
    f = Fernet(key)

    # Verwenden Sie die to_dict-Methode, um das Objekt in ein Dictionary umzuwandeln
    # und dann mit json.dumps zu serialisieren
    obj_dict = obj.to_dict() if isinstance(obj, Serializable) else obj
    serialized_data = json.dumps(obj_dict).encode('utf-8')
    compressed_data = gzip.compress(serialized_data)

    encrypted_data = f.encrypt(compressed_data)
    return {
        'encrypted_data': base64.b64encode(encrypted_data).decode(),
        'salt': base64.b64encode(salt).decode()
    }

def symmetric_decrypt(encrypted_data, password, cls=None):
    """
    Decrypts and decompresses the given encrypted data using the provided password.
    Optionally instantiates and initializes an object of the specified class with the decrypted data.
    If no class is provided, returns the decrypted data as a dictionary.

    :param encrypted_data: The encrypted data as a dictionary containing the encrypted payload and salt.
    :param password: The password used for generating the decryption key.
    :param cls: Optional. The class to instantiate and initialize with the decrypted data.
                Should be a subclass of Serializable and have a no-argument constructor.
    :return: An instance of the specified class initialized with the decrypted data if a class is provided;
             otherwise, a dictionary of the decrypted data.
    """
    salt = base64.b64decode(encrypted_data['salt'])
    key, _ = generate_symmetric_key(password, salt=salt)
    f = Fernet(key)

    decrypted_data = f.decrypt(base64.b64decode(encrypted_data['encrypted_data']))

    # Decompressing and then deserializing the object
    decompressed_data = gzip.decompress(decrypted_data)
    deserialized_data = json.loads(decompressed_data.decode('utf-8'))

    if cls:
        # Instantiate an object of the provided class
        obj = cls()
        for key, value in deserialized_data.items():
            setattr(obj, key, value)  # Set each attribute from the deserialized data
        return obj
    else:
        # Return the deserialized dictionary if no class was provided
        return deserialized_data




