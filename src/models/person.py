# person.py
import base64

from src.models.key import Key
from datetime import datetime
import json

class Person:
    def __init__(self, name, address, gender, email, phone, service_offer, coordinates, validity, seed=None):
        self.key = Key(seed) if seed else Key()
        self.id = self.key.id
        self.pubkey_short = self.key.get_compressed_public_key()
        self.name = name
        self.address = address
        self.gender = gender  # 0 für unbekannt, 1 für männlich, 2 für weiblich
        self.email = email
        self.phone = phone
        self.service_offer = service_offer  # Angebot / Fähigkeiten
        self.coordinates = coordinates

        self.current_voucher = None  # Initialisierung von current_voucher


    def init_empty_voucher(self):
        from src.models.minuto_voucher import MinutoVoucher
        self.current_voucher = MinutoVoucher()

    def create_voucher(self, amount, region, validity):
        """ Erstellt einen neuen MinutoVoucher. """
        from src.models.minuto_voucher import MinutoVoucher
        self.current_voucher = MinutoVoucher.create(self.id, self.name, self.address, self.gender, self.email, self.phone, self.service_offer, self.coordinates, amount, region, validity)

    def read_voucher_from_file(self, filename):
        self.init_empty_voucher()
        self.current_voucher = self.current_voucher.read_from_file(filename)

    def sign_voucher_as_guarantor(self, voucher):
        """ Bürgen signieren den Gutschein mit erweiterten Informationen. """
        # ... [Rest des Codes bleibt gleich]

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
        data_to_sign = voucher.get_voucher_data_for_signing() + json.dumps(guarantor_info, sort_keys=True)
        signature = self.key.sign(data_to_sign, base64_encode=True)
        print(voucher.guarantor_signatures)
        voucher.guarantor_signatures.append((guarantor_info, self.pubkey_short, signature))
        print(voucher.guarantor_signatures)

    def verify_guarantor_signatures(self, voucher):
        """ Verifies whether all guarantor signatures on the voucher are valid. """
        for guarantor_info, pubkey_short, signature in voucher.guarantor_signatures:
            # Combining the voucher data with guarantor info for verification
            data_to_verify = voucher.get_voucher_data_for_signing() + json.dumps(guarantor_info, sort_keys=True)
            # Verifying the signature. Note: the signature is decoded from Base64 format
            print("signature:",signature)
            if not self.key.verify(data_to_verify, base64.b64decode(signature), pubkey_short, compressed_pubkey=True):
                return False  # Return False if any signature is invalid
        return True  # Return True if all signatures are valid

    def sign_voucher_as_creator(self, voucher):
        # todo fehler abfangen - nur unterschreiben wenn voucher einem selbst gehört
        # Schöpfer signiert den Gutschein, inklusive der Bürgen-Signaturen
        data_to_sign = voucher.get_voucher_data_for_signing(include_guarantor_signatures=True)
        voucher.creator_signature = (self.pubkey_short, self.key.sign(data_to_sign, base64_encode=True))

    def __str__(self):
        return f"Person({self.id}, {self.name}, {self.address}, {self.gender}, {self.email}, {self.phone}, {self.service_offer}, {self.coordinates})"
