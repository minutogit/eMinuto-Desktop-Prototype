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
        self.transaction_id = ''
        self.transaction_time = ''

    def get_first_transaction(self, key_for_signing: Key):
        # Erste spezielle Transaktion zur ID des Gutschein-Erstellers
        self.recipient_id = self.voucher.creator_id
        self.amount = self.voucher.amount
        data = self.voucher.get_voucher_data_for_signing(include_guarantor_signatures=True, creator_signature=True).encode()
        self.previous_hash = get_transaction_hash(data)
        self.sender_id = key_for_signing.get_user_id_from_pubkey()
        self.transaction_time = get_timestamp()
        transaction_data = self._assemble_transaction_data()
        return self._sign_transaction_data(key_for_signing, transaction_data)

    def get_transaction(self, amount, recipient_id, key_for_signing: Key):
        self.amount = amount
        self.recipient_id = recipient_id

        # Prüfen, ob Transaktionen vorhanden sind und den Hash der letzten Transaktion verwenden
        if self.voucher.transactions:
            last_transaction = self.voucher.transactions[-1]
            previous_transaction = json.dumps(last_transaction, sort_keys=True).encode()
        else:
            # Wenn keine Transaktionen vorhanden sind, wird der Hash des gesamten Gutscheins verwendet
            previous_transaction = self.voucher.get_voucher_data_for_signing(include_guarantor_signatures=True, creator_signature=True).encode()

        self.previous_hash = get_transaction_hash(previous_transaction)
        self.sender_id = key_for_signing.get_compressed_public_key()
        self.transaction_time = get_timestamp()
        transaction_data = self._assemble_transaction_data()
        return self._sign_transaction_data(key_for_signing, transaction_data)

    def _assemble_transaction_data(self):
        return {
            "previous_hash": self.previous_hash,
            "recipient_id": self.recipient_id,
            "amount": self.amount,
            "sender_id": self.sender_id,
            "transaction_time": self.transaction_time
        }

    def _sign_transaction_data(self, key, transaction_data):
        data_to_sign = json.dumps(transaction_data, sort_keys=True)
        self.sender_signature = key.sign(data_to_sign, base64_encode=True)
        transaction_data["sender_signature"] = self.sender_signature
        return transaction_data
