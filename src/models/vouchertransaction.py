# vouchertransaction.py
import json
from src.models.key import Key
from src.services.utils import get_timestamp, amount_precision
from src.services.crypto_utils import get_hash

class VoucherTransaction:
    def __init__(self, voucher):
        self.voucher = voucher
        self.sender_id = ''
        self.sender_signature = ''
        self.t_id = ''  # transaction id
        self.t_time = ''  # transaction timestamp
        self.sender_remaining_amount = ''  # remaining amount of sender after transaction
        self.t_type = ''  # type of transaction
        self.sender_note = ''  # encrypted note for the sender
        self.recipient_note = ''  # encrypted note for the recipient

    def get_initial_transaction(self, key_for_signing: Key):
        # Initial transaction to initialize the transaction chain with the voucher creator's ID
        self.recipient_id = self.voucher.creator_id
        self.sender_id = self.voucher.creator_id
        self.amount = self.voucher.amount
        self.t_type = 'init'  # type for the initial transaction
        data = self.voucher.get_voucher_data_for_signing(include_guarantor_signatures=True, creator_signature=True).encode()
        self.previous_hash = get_hash(data)
        self.t_time = get_timestamp()
        transaction_data = self._assemble_transaction_data()
        return self._sign_transaction_data(key_for_signing, transaction_data)

    def do_transaction(self, send_amount, sender_id, recipient_id, key_for_signing: Key, sender_note='',
                       recipient_note=''):
        """
        Create a new transaction with the specified parameters.

        :param send_amount: The amount to be sent in the transaction.
        :param sender_id: The ID of the sender of the transaction.
        :param recipient_id: The ID of the recipient of the transaction.
        :param key_for_signing: The key used for signing the transaction.
        :param sender_note: An encrypted note for the sender.
        :param recipient_note: An encrypted note for the recipient.
        :return: The signed transaction data.
        """
        # Calculate available amount for the sender
        available_amount = self.voucher.get_voucher_amount(sender_id)
        # Check if the send amount is within the available amount
        if (send_amount > available_amount or available_amount == 0) and send_amount > 0:
            raise ValueError(f"Insufficient available amount for the transaction. (available: {available_amount} try to send: {send_amount})")

        # Set transaction type and calculate remaining amount if transaction is a split
        if send_amount < available_amount:
            self.t_type = 'split'
            self.sender_remaining_amount = amount_precision(available_amount - send_amount)

        # Set up the transaction data
        self.sender_id = sender_id # Always insert sender_id for easier transaction verification.
        self.amount = amount_precision(send_amount)
        self.recipient_id = recipient_id
        self.sender_note = sender_note  # Encrypted note for the sender
        self.recipient_note = recipient_note  # Encrypted note from sender for recipient

        # Use the hash of the last transaction, if available
        if self.voucher.transactions:
            last_transaction = self.voucher.transactions[-1]
            previous_transaction = json.dumps(last_transaction, sort_keys=True).encode()
            self.previous_hash = get_hash(previous_transaction)
        else:
            raise ValueError("No previous transactions exist for this voucher.")


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

        # Remove empty keys to save space
        transaction_data = {k: v for k, v in transaction_data.items() if v != ''}

        transaction_data["t_id"] = self.calculate_transaction_id(transaction_data)

        return transaction_data

    def _sign_transaction_data(self, key, transaction_data):
        # signs transatction an der returns the complete transaction data
        self.sender_signature = key.sign(transaction_data["t_id"], base64_encode=True)
        transaction_data["sender_signature"] = self.sender_signature
        return transaction_data

    @staticmethod
    def calculate_transaction_id(transaction_data):
        """
        Calculate the transaction ID (t_id) for a given transaction.

        :param transaction_data: A dictionary representing the transaction.
        :return: The calculated transaction ID.
        """
        # Remove 't_id' and 'sender_signature' keys if they exist in the transaction data
        transaction_data = {k: v for k, v in transaction_data.items() if k not in ['t_id', 'sender_signature']}

        # Convert the transaction data to JSON and encode it
        encoded_transaction_data = json.dumps(transaction_data, sort_keys=True).encode()

        # Generate and return the transaction hash
        return get_hash(encoded_transaction_data)
