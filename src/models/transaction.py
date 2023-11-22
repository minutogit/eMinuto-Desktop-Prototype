# transaction.py
import json
from src.models.key import Key
from src.services.utils import get_timestamp
from src.services.crypto_utils import get_transaction_hash

class Transaction:
    def __init__(self, voucher):
        self.voucher = voucher
        self.sender_id = ''
        self.sender_signature = ''
        self.t_id = ''  # transaction id
        self.t_time = ''  # transaction timestamp
        self.sender_remaining_amount = ''  # remaining amount after transaction
        self.t_type = ''  # type of transaction
        self.sender_note = ''  # encrypted note for the sender
        self.recipient_note = ''  # encrypted note for the recipient

    def get_initial_transaction(self, key_for_signing: Key):
        # Initial transaction to initialize the transaction chain with the voucher creator's ID
        self.recipient_id = self.voucher.creator_id
        self.amount = self.voucher.amount
        self.t_type = 'init'  # type for the initial transaction
        data = self.voucher.get_voucher_data_for_signing(include_guarantor_signatures=True, creator_signature=True).encode()
        self.previous_hash = get_transaction_hash(data)
        self.t_time = get_timestamp()
        transaction_data = self._assemble_transaction_data()
        return self._sign_transaction_data(key_for_signing, transaction_data)

    def get_transaction(self, amount, recipient_id, key_for_signing: Key, sender_note='', recipient_note=''):
        self.amount = amount
        self.recipient_id = recipient_id
        self.t_type = ''
        self.sender_note = sender_note  # Encrypted note for the sender itself
        self.recipient_note = recipient_note  # Encrypted note from sender for recipient

        # Check if there are transactions and use the hash of the last transaction
        if self.voucher.transactions:
            last_transaction = self.voucher.transactions[-1]
            previous_transaction = json.dumps(last_transaction, sort_keys=True).encode()
        else:
            # Raise an error if no previous transactions exist
            raise ValueError("No previous transactions exist for this voucher.")

        self.previous_hash = get_transaction_hash(previous_transaction)
        self.sender_id = key_for_signing.get_compressed_public_key()
        self.t_time = get_timestamp()
        transaction_data = self._assemble_transaction_data()
        return self._sign_transaction_data(key_for_signing, transaction_data)

    def _assemble_transaction_data(self):
        # Assemble the transaction data with all fields
        transaction_data = {
            "previous_hash": self.previous_hash,
            "recipient_id": self.recipient_id,
            "amount": self.amount,
            "sender_id": self.sender_id,
            "t_time": self.t_time,
            "t_type": self.t_type,
            "sender_note": self.sender_note,
            "recipient_note": self.recipient_note,
            "sender_remaining_amount": self.sender_remaining_amount
        }

        # Remove keys with empty string values
        transaction_data = {k: v for k, v in transaction_data.items() if v != ''}

        # Generate t_id from current transaction data
        current_transaction_data = json.dumps(transaction_data, sort_keys=True).encode()
        self.t_id = get_transaction_hash(current_transaction_data)
        transaction_data["t_id"] = self.t_id

        return transaction_data

    def _sign_transaction_data(self, key, transaction_data):
        data_to_sign = json.dumps(transaction_data, sort_keys=True)
        self.sender_signature = key.sign(data_to_sign, base64_encode=True)
        transaction_data["sender_signature"] = self.sender_signature
        return transaction_data
