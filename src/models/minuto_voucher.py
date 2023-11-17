# minuto_voucher.py
import base64
import json
from datetime import datetime
import uuid

class MinutoVoucher:
    def __init__(self):
        # Initialize default values for voucher attributes
        self.voucher_id = ''
        self.creator_id = ''
        self.creator_name = ''
        self.creator_address = ''
        self.creator_gender = 0 # 0 for unknown, 1 for male, 2 for female
        self.amount = 0
        self.service_offer = ''
        self.validity = ''
        self.region = ''
        self.coordinates = ''
        self.email = ''
        self.phone = ''
        self.creation_date = ''
        self.guarantor_signatures = []  # Guarantor signatures
        self.creator_signature = None  # Creator's signature
        self.is_test_voucher = False  # Indicates if the voucher is a test voucher

    @classmethod
    def create(cls, creator_id: str, creator_name: str, creator_address, creator_gender: int, email: str, phone: str, service_offer: str, coordinates: str,
               amount: float, region: str, validity: int, is_test_voucher: bool = False):
        # Create a new voucher instance with provided details
        voucher = cls()
        voucher.creator_id = creator_id
        voucher.voucher_id = str(uuid.uuid4())  # Generate a unique voucher ID
        voucher.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        voucher.creator_name = creator_name
        voucher.creator_address = creator_address
        voucher.creator_gender = creator_gender
        voucher.amount = amount
        voucher.service_offer = service_offer
        voucher.validity = datetime.now().year + validity
        voucher.region = region
        voucher.coordinates = coordinates
        voucher.email = email
        voucher.phone = phone
        voucher.is_test_voucher = is_test_voucher
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
        # Convert byte objects to hex strings for storage
        if self.creator_signature:
            self.creator_signature = base64.b64encode(self.creator_signature).decode()
        self.guarantor_signatures = [(g[0], base64.b64encode(g[1]).decode()) for g in self.guarantor_signatures]

        with open(file_path, 'w') as file:
            file.write(json.dumps(self.__dict__, sort_keys=True, indent=4))

        # Convert the signatures back to bytes to maintain the object's state
        if self.creator_signature:
            self.creator_signature = base64.b64decode(self.creator_signature)
        self.guarantor_signatures = [(g[0], base64.b64decode(g[1])) for g in self.guarantor_signatures]

    @classmethod
    def read_from_file(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Create a new voucher instance with the base data
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
            voucher.is_test_voucher = data.get('is_test_voucher', False)  # Read the test voucher status

            # Set additional fields
            voucher.voucher_id = data.get('voucher_id', voucher.voucher_id)
            voucher.creation_date = data.get('creation_date', voucher.creation_date)

            # Convert the Base64-encoded strings back into byte objects
            if data.get('creator_signature'):
                voucher.creator_signature = base64.b64decode(data['creator_signature'])

            voucher.guarantor_signatures = [(g[0], base64.b64decode(g[1])) for g in
                                            data.get('guarantor_signatures', [])]

            return voucher

    def __str__(self):
        # String representation of the voucher for easy debugging and comparison
        guarantor_signatures_str = ', '.join([f"{g[0]}: {g[1].hex()}" for g in self.guarantor_signatures])
        creator_signature_str = self.creator_signature.hex() if self.creator_signature else 'None'
        test_voucher_status = "Test Voucher" if self.is_test_voucher else "Regular Voucher"

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
            f"  Creator Signature: {creator_signature_str}\n"
            f"  Status: {test_voucher_status}\n"
            ")"
        )

    def __eq__(self, other):
        # Vergleichen Sie die string-Repräsentationen der beiden Objekte.
        if not isinstance(other, MinutoVoucher):
            return False

        return str(self) == str(other)