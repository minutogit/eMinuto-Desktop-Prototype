#code der vorbereitet wurde

import os
import hashlib
import binascii
import base64

import base58
from ecdsa import SigningKey, SECP256k1
from mnemonic import Mnemonic
from Crypto.Hash import RIPEMD160
import json
from datetime import datetime
import uuid

class Key:
    def __init__(self, seed_words=None, empty=False):
        if empty:
            # Erstellt einen "leeren" Schlüssel
            self.id = None
            self.private_key = None
            self.public_key = None
            self.seed_words = None
        else:
            # Verwendet vorgegebene seed_words oder generiert neue
            self.seed_words = seed_words if seed_words else self.generate_seed()
            self.private_key, self.public_key = self.create_key_pair(self.seed_words)
            self.id = self.create_public_address(self.public_key)

    @staticmethod
    def generate_seed():
        """ Generates a random seed of 12 words. """
        mnemo = Mnemonic("english")
        return mnemo.generate(strength=128)

    @staticmethod
    def create_key_pair(seed_words):
        """ Creates a key pair from the seed. """
        mnemo = Mnemonic("english")
        seed_bytes = mnemo.to_seed(seed_words, passphrase="")
        private_key = SigningKey.from_string(seed_bytes[:32], curve=SECP256k1)
        return private_key, private_key.verifying_key

    @staticmethod
    def sign_message(private_key, message):
        """ Signs a message using the private key. """
        return private_key.sign(message.encode('utf-8'))

    @staticmethod
    def verify_signature(public_key, message, signature):
        """ Verifies the signature using the public key. """
        return public_key.verify(signature, message.encode('utf-8'))

    @staticmethod
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

    @staticmethod
    def verify_address_checksum(address):
        """ Verifies the checksum of an address. """
        main_part = address[:-4]
        existing_checksum = address[-4:]
        calculated_checksum = hashlib.sha256(main_part.encode()).digest()[:4]
        calculated_checksum_encoded = base58.b58encode(calculated_checksum).decode()[-4:]
        return calculated_checksum_encoded == existing_checksum

    def __str__(self):
        return f"Key(Public Address: {self.public_address}, Seed Words: {self.seed_words})"

class Person:
    def __init__(self, key: Key, name, address, gender, email, phone, service_offer, coordinates, validity):
        self.key = key
        self.id = key.id
        self.name = name
        self.address = address
        self.gender = gender  # 0 für unbekannt, 1 für männlich, 2 für weiblich
        self.email = email
        self.phone = phone
        self.service_offer = service_offer  # Angebot / Fähigkeiten
        self.coordinates = coordinates

    def create_voucher(self, amount, region, validity):
        """ Erstellt einen neuen MinutoVoucher. """
        return MinutoVoucher(self, amount, region, validity)

    def sign_voucher_as_guarantor(self, voucher):
        """ Bürgen signieren den Gutschein mit erweiterten Informationen. """
        guarantor_info = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "coordinates": self.coordinates,
            "signature_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        signature_data = voucher.get_voucher_data() + json.dumps(guarantor_info, sort_keys=True)
        signature = self.key.sign_message(self.key.private_key, signature_data)
        voucher.guarantor_signatures.append((guarantor_info, signature))

    def sign_voucher_as_creator(self, voucher):
        # Schöpfer signiert den Gutschein, inklusive der Bürgen-Signaturen
        data_to_sign = voucher.get_voucher_data(include_guarantor_signatures=True)
        voucher.creator_signature = self.key.sign_message(self.key.private_key, data_to_sign)

    def __str__(self):
        return f"Person({self.id}, {self.name}, {self.address}, {self.gender}, {self.email}, {self.phone}, {self.service_offer}, {self.coordinates})"

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
        # Konvertiert Byte-Objekte in hexadezimale Strings für die Speicherung
        if self.creator_signature:
            self.creator_signature = base64.b64encode(self.creator_signature).decode()
        self.guarantor_signatures = [(g[0], base64.b64encode(g[1]).decode()) for g in self.guarantor_signatures]

        with open(file_path, 'w') as file:
            file.write(json.dumps(self.__dict__, sort_keys=True, indent=4))

        # Konvertiert die Signaturen zurück in Bytes, um den Zustand des Objekts beizubehalten
        if self.creator_signature:
            self.creator_signature = base64.b64decode(self.creator_signature)
        self.guarantor_signatures = [(g[0], base64.b64decode(g[1])) for g in self.guarantor_signatures]


    @classmethod
    def read_from_disk(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Erstelle ein temporäres Person-Objekt mit den geladenen Daten
            temp_person = Person(
                key=Key(empty=True),  # Empty Key Object
                name=data.get('creator_name', ''),
                address=data.get('creator_address', ''),
                gender=data.get('creator_gender', 0),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                service_offer=data.get('service_offer', ''),
                coordinates=data.get('coordinates', ''),
                validity=data.get('validity', '')
            )

            # Erstelle ein MinutoVoucher-Objekt mit dem temporären Person-Objekt
            voucher = cls(
                creator=temp_person,
                amount=data.get('amount', 0),
                region=data.get('region', ''),
                validity=data.get('validity', '')
            )
            voucher.voucher_id = data.get('voucher_id', str(uuid.uuid4()))
            voucher.creation_date = data.get('creation_date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Konvertiert die hexadezimalen Strings zurück in Byte-Objekte
            voucher.creator_signature = base64.b64decode(data.get('creator_signature', '')) if data.get(
                'creator_signature') else None
            voucher.guarantor_signatures = [(g[0], base64.b64decode(g[1])) for g in
                                            data.get('guarantor_signatures', [])]

            return voucher

    def __str__(self):
        guarantor_signatures_str = ', '.join([f"{g[0]}: {g[1].hex()}" for g in self.guarantor_signatures])
        return (
            f"MinutoVoucher(\n"
            f"  Voucher ID: {self.voucher_id}\n"
            f"  Creator ID: {self.creator_id}\n"
            f"  Creator Name: {self.creator_name}\n"
            f"  Creator Address: {self.creator_address}\n"
            f"  Creator Gender: {self.creator_gender}\n"
            f"  Amount: {self.amount}\n"
            f"  Service Offer: {self.service_offer}\n"
            f"  Validity: {self.validity}\n"
            f"  Region: {self.region}\n"
            f"  Coordinates: {self.coordinates}\n"
            f"  Email: {self.email}\n"
            f"  Phone: {self.phone}\n"
            f"  Creation Date: {self.creation_date}\n"
            f"  Guarantor Signatures: [{guarantor_signatures_str}]\n"
            f"  Creator Signature: {self.creator_signature.hex() if self.creator_signature else 'None'}\n"
            ")"
        )






# Erstelle eine Person
hansdampf = Person(Key("adapt buddy actress swear early offer grow comic code sting hawk marble"), "Max Mustermann", "Musterstraße 1", 1, "max@example.com", "0123456789", "IT-Support", "50.1109, 8.6821", "2023-12-31")
buerge_weiblich = Person(Key("rookie era bamboo industry group furnace axis disorder economy silly action invite"), "Susi Musterfrau", "Musterstraße 2", 2, "susi@example.com", "0123456789", "Backen", "50.1109, 8.6821", "2023-12-31")
buerge_maennlich = Person(Key("strong symptom minor attract math clock pool elite half guess album close"), "Max Mustermann", "Musterstraße 1", 1, "max@example.com", "0123456789", "IT-Support", "50.1109, 8.6821", "2023-12-31")

# Erstelle einen MinutoVoucher mit dieser Person als Ersteller
voucher = hansdampf.create_voucher(100, "Frankfurt", "2028")
voucher.save_to_disk("minutoschein.txt")

b1_load_voucher = MinutoVoucher.read_from_disk("minutoschein.txt")
buerge_maennlich.sign_voucher_as_guarantor(b1_load_voucher)
b1_load_voucher.save_to_disk("minutoschein-b1.txt")

print(voucher)
print(b1_load_voucher)


