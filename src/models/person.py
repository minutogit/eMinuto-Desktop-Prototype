# person.py
from src.models.key import Key
from datetime import datetime
import json

class Person:
    def __init__(self, name, address, gender, email, phone, service_offer, coordinates, validity, seed=None):
        self.key = Key(seed) if seed else Key()
        self.id = self.key.id
        self.name = name
        self.address = address
        self.gender = gender  # 0 für unbekannt, 1 für männlich, 2 für weiblich
        self.email = email
        self.phone = phone
        self.service_offer = service_offer  # Angebot / Fähigkeiten
        self.coordinates = coordinates

        self.current_voucher = None  # Initialisierung von current_voucher

    def create_voucher(self, amount, region, validity):
        """ Erstellt einen neuen MinutoVoucher. """
        from src.models.minuto_voucher import MinutoVoucher
        self.current_voucher = MinutoVoucher(self, amount, region, validity)

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
