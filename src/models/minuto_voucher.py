# minuto_voucher.py
import base64
import json
import uuid
from src.models.key import Key
from src.services.utils import get_timestamp
from src.services.crypto_utils import get_hash
from src.models.transaction import Transaction


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
        self.is_test_voucher = False  # Indicates if the voucher is a test voucher
        self.guarantor_signatures = []  # Guarantor signatures
        self.creator_signature = None  # Creator's signature
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
        """
        Checks the validity of the voucher.
        A voucher is considered valid if it has at least two guarantor signatures and a creator signature.
        """
        # Check the validity of the voucher
        return len(self.guarantor_signatures) >= 2 and self.creator_signature is not None

    def save_to_disk(self, file_path):
        """
        Saves all attributes of the MinutoVoucher object to a specified file path.

        :param file_path: The path of the file where the voucher data will be saved.
        """
        # Save all attributes of the MinutoVoucher object
        data_to_save = self.__dict__.copy()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_to_save, sort_keys=False, indent=4, ensure_ascii=False))

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

    def verify_initial_transaction(self):
        """
        Verifies the initial transaction of the voucher.

        :return: True if the initial transaction is valid, False otherwise.
        """
        # Check if there are any transactions
        if not self.transactions:
            return False

        # Retrieve the initial transaction from the transaction list
        initial_transaction = self.transactions[0]

        # Validate that the initial transaction meets expected conditions
        if initial_transaction['t_type'] != 'init' or \
                initial_transaction['recipient_id'] != self.creator_id or \
                initial_transaction['amount'] != self.amount or \
                initial_transaction['sender_id'] != self.creator_id:
            return False

        # Verify the linkage to the voucher - verify hash from complete voucher data
        data_for_prev_hash = self.get_voucher_data_for_signing(include_guarantor_signatures=True,
                                                               creator_signature=True).encode()
        if get_hash(data_for_prev_hash) != initial_transaction['previous_hash']:
            return False

        # Verify transaction ID and the correct signature of the sender (creator)
        if Transaction.calculate_transaction_id(initial_transaction) != initial_transaction['t_id']:
            return False

        # Verify the signature of the transaction ID
        is_signature_valid = self.verify_transaction_ids_signature(initial_transaction)

        return is_signature_valid

    def verify_transaction_ids_signature(self, transaction):
        """
        Verifies whether the transaction ID is correctly calculated and properly signed by the sender_id (creator of the transaction).
        Note: This is not a complete verification in context with the previous transaction! (linkage, amount, sender's authorization, etc., need to be checked separately.)
        Receives a transaction.
        Returns True if the signature from the sender is correct.
        """

        # Check if the transaction ID is correct
        if not transaction["t_id"] == Transaction.calculate_transaction_id(transaction):
            return False

        # Verify the signature against the sender's public key
        pubkey = Key.get_pubkey_from_id(transaction['sender_id'])
        is_signature_valid = Key.verify_signature(transaction["t_id"],
                                                  base64.b64decode(transaction['sender_signature']),
                                                  pubkey)
        return is_signature_valid

    def verify_all_transactions(self, verbose=False):
        """
        Verifies all transactions in the voucher.

        :param verbose: If set to True, print detailed messages during the verification process.
        :return: True if all transactions are valid, False otherwise.
        """

        # Check if there are any transactions
        if not self.transactions:
            if verbose:
                print("No transactions to verify.")
            return False

        # Verify the initial transaction
        if not self.verify_initial_transaction():
            if verbose:
                print("Initial transaction verification failed.")
            return False

        # Loop through and verify each subsequent transaction
        for i in range(1, len(self.transactions)):
            current_transaction = self.transactions[i]
            previous_transaction = self.transactions[i - 1]

            if verbose:
                print(f"Verifying transaction: {i}  -  {current_transaction['t_id']}")

            # Verify the transaction ID and the sender's signature
            if not self.verify_transaction_ids_signature(current_transaction):
                if verbose:
                    print("Transaction ID or sender's signature verification failed.")
                return False

            if verbose:
                print("Transaction ID and Signature are okay")

            # Verify if the sender was authorized to send
            allowed_senders = [previous_transaction['recipient_id']]
            if previous_transaction.get('type', '') == 'split':
                allowed_senders.append(previous_transaction['sender_id'])
            if current_transaction['sender_id'] not in allowed_senders:
                if verbose:
                    print(f"Sender {current_transaction['sender_id']} was not authorized to send.")
                return False

            if verbose:
                print(f"Sender {current_transaction['sender_id']} was allowed to send")

            # Verify if the sent amount was permissible
            allowed_amount = previous_transaction[
                'amount']  # Typically, the recipient of the last transaction is the sender of the current transaction
            if previous_transaction.get('type', '') == 'split' and current_transaction['sender_id'] == \
                    previous_transaction['sender_id']:
                allowed_amount = previous_transaction[
                    'sender_remaining_amount']  # available remaining amount from the sender
            if current_transaction['amount'] > allowed_amount:
                if verbose:
                    print(f"Too much sent! {current_transaction['amount']} Minuto (max allowed {allowed_amount})")
                return False

            if verbose:
                print(f"Received {current_transaction['amount']} Minuto (max allowed {allowed_amount})")

            # Verify the linkage to the previous transaction
            previous_transaction_hash = get_hash(json.dumps(previous_transaction, sort_keys=True).encode())
            if current_transaction['previous_hash'] != previous_transaction_hash:
                if verbose:
                    print("Linkage to the previous transaction failed.")
                return False

            if verbose:
                print("Linkage (Hash of the previous transaction) is correct\n")

        if verbose:
            print("All transactions are okay")
        return True

    def verify_complete_voucher(self):
        """
        Verifies the entire voucher including guarantor signatures, creator's signature, and all transactions.

        :return: True if the entire voucher is valid, False otherwise.
        """
        # Verify guarantor signatures
        if not self.verify_all_guarantor_signatures(self):
            print("Guarantor signature verification failed.")
            return False

        # Verify creator's signature
        if not self.verify_creator_signature(self):
            print("Creator signature verification failed.")
            return False

        # Verify all transactions
        if not self.verify_all_transactions():
            print("Transaction verification failed.")
            return False

        print("The entire voucher is verified and valid.")
        return True

    def __str__(self):
        # String representation of the voucher for easy debugging and comparison
        guarantor_signatures_str = ', '.join([f"{g[0]}: {g[1]}" for g in self.guarantor_signatures])
        creator_signature_str = self.creator_signature if self.creator_signature else 'None'
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
            f"  transactions: {self.transactions}\n"
            ")"
        )

    def __eq__(self, other):
        # compare with string representation of the voucher
        if not isinstance(other, MinutoVoucher):
            return False

        return str(self) == str(other)