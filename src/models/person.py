# person.py
import base64

from src.models.key import Key
from src.models.vouchertransaction import VoucherTransaction
from src.models.transactionmanager import TransactionManager
from src.services.utils import get_timestamp, dprint
import json

class Person:
    def __init__(self, name, address, gender, email, phone, service_offer, coordinates, seed=None):
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
        self.vouchers = [] # list of vouchers

    def init_empty_voucher(self):
        from src.models.minuto_voucher import MinutoVoucher
        self.current_voucher = MinutoVoucher()

    def create_voucher(self, amount, region, validity):
        """ Erstellt einen neuen MinutoVoucher. """
        from src.models.minuto_voucher import MinutoVoucher
        self.current_voucher = MinutoVoucher.create(self.id, self.name, self.address, self.gender, self.email, self.phone, self.service_offer, self.coordinates, amount, region, validity)

    def read_voucher_and_save_voucher(self, filename, virtual = False):
        """read the voucher and stores it to persons voucher list"""
        self.read_voucher(filename, virtual)
        self.vouchers.append(self.current_voucher)

    def read_voucher(self, filename, virtual = False):
        """read the voucher"""
        self.init_empty_voucher()
        self.current_voucher = self.current_voucher.read_from_file(filename, virtual)

    def save_voucher(self, filename = None, virtual = False):
        return self.current_voucher.save_to_disk(filename, virtual)

    def sign_voucher_as_guarantor(self, voucher=None):
        """ Signs the voucher including the guarantor's personal details. """
        voucher = voucher or self.current_voucher

        if voucher.creator_id == self.id:
            print("Guarantors cannot sign their own vouchers.")
            return

        # Prepare guarantor information for signature
        guarantor_info = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "coordinates": self.coordinates,
            "signature_time": get_timestamp()
        }

        # Combine voucher data with guarantor information to create data for signing
        data_to_sign = voucher.get_voucher_data_for_signing() + json.dumps(guarantor_info, sort_keys=True)
        signature = self.key.sign(data_to_sign, base64_encode=True)

        # Append the signed guarantor information to the voucher
        voucher.guarantor_signatures.append((guarantor_info, signature))

    def verify_guarantor_signatures(self, voucher=None):
        """ Validates all guarantor signatures on the voucher. """
        voucher = voucher or self.current_voucher
        return voucher.verify_all_guarantor_signatures(voucher)

    def sign_voucher_as_creator(self, voucher=None):
        """ Signs the voucher as its creator and initialize the transaction list"""
        voucher = voucher or self.current_voucher

        if voucher.creator_id != self.id:
            print("Can only sign own voucher as creator!")
            return
        # Schöpfer signiert den Gutschein, inklusive der Bürgen-Signaturen
        data_to_sign = voucher.get_voucher_data_for_signing(include_guarantor_signatures=True)
        voucher.creator_signature = (self.key.sign(data_to_sign, base64_encode=True))
        # Initialize first transaction
        transaction = VoucherTransaction(voucher)
        transaction_data = transaction.get_initial_transaction(self.key)
        voucher.transactions.append(transaction_data)

    def verify_creator_signature(self, voucher=None):
        """ Verifies the signature of the voucher's creator. """
        voucher = voucher or self.current_voucher
        return voucher.verify_creator_signature(voucher)

    def send_amount(self, amount, recipient_id):
        """
        Send a specified amount to a recipient using available vouchers.

        :param amount: The amount to send.
        :param recipient_id: The ID of the recipient.
        :return: List of vouchers used for the transaction.
        """
        return TransactionManager.process_transactions(self, amount, recipient_id)

    def append_transaction_to_voucher(self, amount, recipient_id, voucher=None):
        if voucher is None:
            print("No voucher selected")
            return

        # Erstellen einer neuen Transaktion
        transaction = VoucherTransaction(voucher)

        # Transaktionsdaten generieren und signieren
        transaction_data = transaction.do_transaction(amount, self.id, recipient_id, self.key)

        # Füge die Transaktion der Transaktionsliste des Gutscheins hinzu
        voucher.transactions.append(transaction_data)

    def __str__(self):
        return f"Person({self.id}, {self.name}, {self.address}, {self.gender}, {self.email}, {self.phone}, {self.service_offer}, {self.coordinates})"
