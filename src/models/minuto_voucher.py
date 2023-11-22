# minuto_voucher.py
import base64
import json
import uuid
from src.models.key import Key
from src.services.utils import get_timestamp


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
        self.validit_until = ''
        self.region = ''
        self.coordinates = ''
        self.email = ''
        self.phone = ''
        self.creation_date = ''
        self.guarantor_signatures = []  # Guarantor signatures
        self.creator_signature = None  # Creator's signature
        self.is_test_voucher = False  # Indicates if the voucher is a test voucher
        self.transactions = [] # list of transactions

    @classmethod
    def create(cls, creator_id: str, creator_name: str, creator_address, creator_gender: int, email: str, phone: str, service_offer: str, coordinates: str,
               amount: float, region: str, validity: int, is_test_voucher: bool = False):
        # Create a new voucher instance with provided details
        voucher = cls()
        voucher.creator_id = creator_id
        voucher.voucher_id = str(uuid.uuid4())  # Generate a unique voucher ID
        voucher.creation_date = get_timestamp()
        voucher.creator_name = creator_name
        voucher.creator_address = creator_address
        voucher.creator_gender = creator_gender
        voucher.amount = amount
        voucher.service_offer = service_offer
        voucher.validit_until = get_timestamp(validity, end_of_year=True)
        voucher.region = region
        voucher.coordinates = coordinates
        voucher.email = email
        voucher.phone = phone
        voucher.is_test_voucher = is_test_voucher
        return voucher

    def get_voucher_data_for_signing(self, include_guarantor_signatures=False, creator_signature= False):
        # Dynamically generate the data, including optional guarantor signatures
        data = {
            "voucher_id": self.voucher_id,
            "creator_id": self.creator_id,
            "creator_name": self.creator_name,
            "creator_address": self.creator_address,
            "creator_gender": self.creator_gender,
            "email": self.email,
            "phone": self.phone,
            "service_offer": self.service_offer,
            "amount": self.amount,
            "validit_until": self.validit_until,
            "region": self.region,
            "coordinates": self.coordinates,
            "creation_date": self.creation_date,
            "is_test_voucher": self.is_test_voucher
        }

        if include_guarantor_signatures:
            data["guarantor_signatures"] = self.guarantor_signatures

        if creator_signature:
            data["creator_signature"] = self.creator_signature


        return json.dumps(data, sort_keys=True, ensure_ascii=False)

    def is_valid(self):
        # Überprüft die Gültigkeit des Gutscheins
        return len(self.guarantor_signatures) >= 2 and self.creator_signature is not None

    def save_to_disk(self, file_path):
        # Speichern aller Attribute des MinutoVoucher-Objekts
        data_to_save = self.__dict__.copy()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_to_save, sort_keys=True, indent=4, ensure_ascii=False))

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
            voucher.validit_until = data.get('validit_until', '')
            voucher.is_test_voucher = data.get('is_test_voucher', False)  # Read the test voucher status
            voucher.transactions = data.get('transactions', [])


            # Set additional fields
            voucher.voucher_id = data.get('voucher_id', voucher.voucher_id)
            voucher.creation_date = data.get('creation_date', voucher.creation_date)

            if data.get('creator_signature'):
                voucher.creator_signature = data['creator_signature']

            guarantor_signatures = []
            for guarantor_info, signature in data.get('guarantor_signatures', []):
                guarantor_signatures.append((guarantor_info, signature))

            voucher.guarantor_signatures = guarantor_signatures
            return voucher

    def verify_all_guarantor_signatures(self, voucher):
        """ Validates all guarantor signatures on the given voucher. """
        for guarantor_info, signature in voucher.guarantor_signatures:
            if Key.check_user_id(guarantor_info["id"]) == False:
                 return False
            pubkey_short = Key.get_pubkey_from_id(guarantor_info["id"])

            data_to_verify = voucher.get_voucher_data_for_signing() + json.dumps(guarantor_info, sort_keys=True)
            if not Key.verify_signature(data_to_verify, base64.b64decode(signature), pubkey_short):
                return False

        return True

    def verify_creator_signature(self, voucher):
        """ Verifies the creator's signature on the given voucher. """
        signature = voucher.creator_signature
        if Key.check_user_id(voucher.creator_id) == False:
            return False
        pubkey_short = Key.get_pubkey_from_id(voucher.creator_id)

        data_to_verify = voucher.get_voucher_data_for_signing(include_guarantor_signatures=True)
        return Key.verify_signature(data_to_verify, base64.b64decode(signature), pubkey_short)

    def __str__(self):
        # String representation of the voucher for easy debugging and comparison
        guarantor_signatures_str = ', '.join([f"{g[0]}: {g[1]}" for g in self.guarantor_signatures])
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
            f"  Valid Until: {self.validit_until}\n"
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