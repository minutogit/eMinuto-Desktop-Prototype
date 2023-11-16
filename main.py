#code der vorbereitet wurde

import os
import hashlib
import binascii
import base58
from ecdsa import SigningKey, SECP256k1
from mnemonic import Mnemonic
from Crypto.Hash import RIPEMD160
import json
from datetime import datetime
import uuid

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

    # Base58-encode the RIPEMD160 hash
    encoded_ripemd160_bpk = base58.b58encode(ripemd160_bpk.digest())

    # Add 'MC' prefix to the encoded RIPEMD160 hash
    address_with_prefix = "MC" + encoded_ripemd160_bpk.decode()

    # Calculate checksum for the address with prefix
    checksum = hashlib.sha256(address_with_prefix.encode()).digest()[:4]

    # Base58-encode the checksum and append the last 4 characters to the address
    final_address = address_with_prefix + base58.b58encode(checksum).decode()[-4:]

    return final_address

def verify_address_checksum(address):
    """ Verifies the checksum of an address. """
    # Extract the main part and the checksum part
    main_part = address[:-4]
    existing_checksum = address[-4:]

    # Calculate checksum for the main part
    calculated_checksum = hashlib.sha256(main_part.encode()).digest()[:4]
    calculated_checksum_encoded = base58.b58encode(calculated_checksum).decode()[-4:]

    return calculated_checksum_encoded == existing_checksum




class MinutoVoucher:
    def __init__(self, creator: Person, amount=0, region='', validity = ''):
        self.voucher_id = str(uuid.uuid4())  # Generiert eine eindeutige voucher_id
        self.creator_id = creator.id
        self.creator_name = creator.name
        self.creator_address = creator.address
        self.creator_gender = creator.gender
        self.amount = amount
        self.service_offer = creator.service_offer
        self.validity = validity
        self.region = region
        self.coordinates = creator.coordinates
        self.email = creator.email
        self.phone = creator.phone
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.guarantor_signatures = []  # Signaturen der Bürgen
        self.creator_signature = None  # Signatur des Schöpfers

    # ... (Rest der Methoden bleiben unverändert)


    def sign_voucher_as_guarantor(self, guarantor_id, private_key, guarantor_name, guarantor_address, guarantor_gender, guarantor_email, guarantor_phone, guarantor_coordinates):
        # Bürgen signieren den Gutschein mit erweiterten Informationen
        guarantor_info = {
            "id": guarantor_id,
            "name": guarantor_name,
            "address": guarantor_address,
            "gender": guarantor_gender,
            "email": guarantor_email,
            "phone": guarantor_phone,
            "coordinates": guarantor_coordinates,
            "signature_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        signature_data = self.get_voucher_data() + json.dumps(guarantor_info, sort_keys=True)
        signature = sign_message(private_key, signature_data)
        self.guarantor_signatures.append((guarantor_id, signature))

    def sign_voucher_as_creator(self, private_key):
        # Schöpfer signiert den Gutschein, inklusive der Bürgen-Signaturen
        data_to_sign = self.get_voucher_data(include_guarantor_signatures=True)
        self.creator_signature = sign_message(private_key, data_to_sign)

    def get_voucher_data(self, include_guarantor_signatures=False):
        # Dynamische Generierung der Daten, inklusive optionaler Bürgen-Signaturen
        data = {
            "creator_id": self.creator_id,
            "creator_name": self.creator_name,
            "creator_address": self.creator_address,
            "creator_gender": self.creator_gender,
            "amount": self.amount,
            "service_offer": self.service_offer,
            "validity": self.validity,
            "region": self.region,
            "coordinates": self.coordinates,
            "creation_date": self.creation_date
        }
        if include_guarantor_signatures:
            data["guarantor_signatures"] = self.guarantor_signatures
        return json.dumps(data, sort_keys=True)

    def is_valid(self):
        # Überprüft die Gültigkeit des Gutscheins
        return len(self.guarantor_signatures) >= 2 and self.creator_signature is not None

    def save_to_disk(self, file_path):
        # Speichert den Gutschein als Datei
        with open(file_path, 'w') as file:
            file.write(json.dumps(self.__dict__, sort_keys=True, indent=4))

    @classmethod
    def read_from_disk(cls, file_path):
        # Liest den Gutschein aus einer Datei und erstellt ein Objekt
        with open(file_path, 'r') as file:
            data = json.load(file)
            voucher = cls(
                data.get('creator_id', ''),
                data.get('creator_name', ''),
                data.get('creator_address', ''),
                data.get('creator_gender', 0),
                data.get('amount', 0),
                data.get('service_offer', ''),
                data.get('validity', ''),
                data.get('region', ''),
                data.get('coordinates', '')
            )
            voucher.creation_date = data.get('creation_date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            voucher.guarantor_signatures = data.get('guarantor_signatures', [])
            voucher.creator_signature = data.get('creator_signature')
            return voucher

class Person:
    def __init__(self, id, name, address, gender, email, phone, service_offer, coordinates, validity):
        self.id = id
        self.name = name
        self.address = address
        self.gender = gender  # 0 für unbekannt, 1 für männlich, 2 für weiblich
        self.email = email
        self.phone = phone
        self.service_offer = service_offer  # Angebot / Fähigkeiten
        self.coordinates = coordinates

    def __str__(self):
        return f"Person({self.id}, {self.name}, {self.address}, {self.gender}, {self.email}, {self.phone}, {self.coordinates})"


# Generate seed and create key pair
seed_words = generate_seed()
print("Seed words:", seed_words)

private_key, public_key = create_key_pair(seed_words)

# Create public address
public_address = create_public_address(public_key)
print("Public Address (ID):", public_address)

# Sign a message and verify the signature
message = "This is a sample text."
signature = sign_message(private_key, message)
print("Signature:", binascii.hexlify(signature).decode())

is_valid_signature = verify_signature(public_key, message, signature)
print("Is the signature valid?", is_valid_signature)

# Check the checksum of the address
is_checksum_valid = verify_address_checksum(public_address)
print("Is the address checksum valid?", is_checksum_valid)

