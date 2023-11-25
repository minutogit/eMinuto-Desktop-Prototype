from src.models.vouchertransaction import VoucherTransaction
from src.services.utils import dprint

class UserTransaction:
    """Manages transactions between users (persons). A user transaction can contain multiple vouchers."""

    def __init__(self):
        self.transaction_vouchers = []
        self.transaction_successful = False

    @staticmethod
    def process_transaction_to_user(person, amount, recipient_id):
        """
        Processes transactions by selecting suitable vouchers and creating transaction data.

        :param person: The person object initiating the transaction.
        :param amount: The amount to send.
        :param recipient_id: The ID of the recipient.
        :return: A UserTransaction object with the selected vouchers.
        """
        user_transaction = UserTransaction()
        remaining_amount_to_send = amount
        selected_vouchers = []

        for voucher in person.vouchers:
            if not voucher.verify_complete_voucher():
                continue  # Use only valid vouchers

            voucher_amount = voucher.get_voucher_amount(person.id)

            if voucher_amount < remaining_amount_to_send:
                selected_vouchers.append(voucher)
                remaining_amount_to_send -= voucher_amount
            else:
                selected_vouchers.append(voucher)
                remaining_amount_to_send = 0
                break

        if remaining_amount_to_send > 0:
            print("Not enough amount to send.")
            return user_transaction

        for voucher in selected_vouchers:
            transaction = VoucherTransaction(voucher)
            transaction_data = transaction.do_transaction(remaining_amount_to_send, person.id, recipient_id, person.key)
            voucher.transactions.append(transaction_data)
            user_transaction.transaction_vouchers.append(voucher)

        user_transaction.transaction_successful = True
        return user_transaction

    def receive_transaction_from_user(self, transaction, person):
        """
        Receives a UserTransaction object and adds its vouchers to the person's vouchers.

        :param person: The person object who is receiving the transactions.
        :param transaction: The UserTransaction object containing the transaction vouchers.
        """
        if not transaction.transaction_successful:
            print("receive_transaction_from_user fails")
        for voucher in transaction.transaction_vouchers:
            person.vouchers.append(voucher)
