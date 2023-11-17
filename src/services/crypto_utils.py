from Crypto.Hash import RIPEMD160
from ecdsa.util import sigdecode_der
from ecdsa import VerifyingKey, BadSignatureError
from ecdsa.curves import SECP256k1
from ecdsa.ecdsa import Public_key
from ecdsa.numbertheory import square_root_mod_prime
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

def compress_public_key(public_key):
    """ Compresses the public key. """
    x, y = public_key.pubkey.point.x(), public_key.pubkey.point.y()
    prefix = '02' if y % 2 == 0 else '03'
    return prefix + hex(x)[2:].zfill(64)

def verify_signature_with_compressed_key(compressed_public_key, message, signature):
    """ Verifies the signature using the compressed public key. """
    if len(compressed_public_key) != 66:
        raise ValueError("Invalid compressed public key length")

    # Decompress the public key
    prefix = compressed_public_key[:2]
    x = int(compressed_public_key[2:], 16)
    y_parity = (prefix == '03')
    curve = SECP256k1.curve
    alpha = (x*x*x + curve.a()*x + curve.b()) % curve.p()
    beta = square_root_mod_prime(alpha, curve.p())
    y = beta if y_parity == (beta % 2 == 1) else curve.p() - beta

    # Reconstruct the public key
    public_key_obj = VerifyingKey.from_public_point(Public_key(curve, curve.point(x, y)).point, curve=SECP256k1)

    try:
        # Verify the signature
        return public_key_obj.verify(signature, message.encode('utf-8'), sigdecode=sigdecode_der)
    except BadSignatureError:
        return False

