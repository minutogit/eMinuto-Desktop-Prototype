# minuto_voucher.py
import base64
import json
from datetime import datetime

from .key import Key
import uuid

from .person import Person


class MinutoVoucher:
    def __init__(self):
        self.voucher_id = str(uuid.uuid4())  # Generiert eine eindeutige voucher_id
        self.creator_id = ''
        self.creator_name = ''
        self.creator_address = ''
        self.creator_gender = 0
        self.amount = 0
        self.service_offer = ''
        self.validity = ''
        self.region = ''
        self.coordinates = ''
        self.email = ''
        self.phone = ''
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.guarantor_signatures = []  # Signaturen der Bürgen
        self.creator_signature = None  # Signatur des Schöpfers

    @classmethod
    def create(cls, creator_id, creator_name, creator_address, creator_gender, email, phone, service_offer, coordinates,
               amount, region, validity):
        voucher = cls()
        voucher.creator_id = creator_id
        voucher.creator_name = creator_name
        voucher.creator_address = creator_address
        voucher.creator_gender = creator_gender
        voucher.amount = amount
        voucher.service_offer = service_offer
        voucher.validity = validity
        voucher.region = region
        voucher.coordinates = coordinates
        voucher.email = email
        voucher.phone = phone
        return voucher

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
    def read_from_file(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Erstellen einer neuen Voucher-Instanz mit den Basisdaten
            voucher = cls()
            voucher.creator_id = data.get('creator_id', '')
            voucher.creator_name = data.get('creator_name', '')
            voucher.creator_address = data.get('creator_address', '')
            voucher.creator_gender = data.get('creator_gender', 0)
            voucher.email = data.get('email', '')
            voucher.phone = data.get('phone', '')
            voucher.service_offer = data.get('service_offer', '')
            voucher.coordinates = data.get('coordinates', '')
            voucher.amount = data.get('amount', 0)
            voucher.region = data.get('region', '')
            voucher.validity = data.get('validity', '')

            # Setzen der zusätzlichen Felder
            voucher.voucher_id = data.get('voucher_id', voucher.voucher_id)  # Behalte die ursprüngliche ID bei
            voucher.creation_date = data.get('creation_date', voucher.creation_date)

            # Umwandlung der Base64-kodierten Strings zurück in Byte-Objekte
            if data.get('creator_signature'):
                voucher.creator_signature = base64.b64decode(data['creator_signature'])

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

    def __eq__(self, other):
        # Vergleichen Sie die string-Repräsentationen der beiden Objekte.
        if not isinstance(other, MinutoVoucher):
            return False

        return str(self) == str(other)