from src.models.vouchertransaction import VoucherTransaction
from src.services.utils import dprint

class TransactionManager:
    """manages full transactions which con contain multiple voucher-transaction"""
    def __init__(self):
        pass

    @staticmethod
    def process_transactions(person, amount, recipient_id):
        """
        Processes transactions by selecting suitable vouchers and creating transaction data.

        :param person: The person object initiating the transaction.
        :param amount: The amount to send.
        :param recipient_id: The ID of the recipient.
        :return: List of tuples with vouchers and amounts sent.
        """
        selected_vouchers = []
        remaining_amount_to_send = amount

        for voucher in person.vouchers:
            if not voucher.verify_complete_voucher():

                continue  # Use only valid vouchers

            voucher_amount = voucher.get_voucher_amount(person.id)

            if voucher_amount < remaining_amount_to_send:
                selected_vouchers.append((voucher, voucher_amount))
                remaining_amount_to_send -= voucher_amount
            else:
                selected_vouchers.append((voucher, remaining_amount_to_send))
                remaining_amount_to_send = 0
                break

        if remaining_amount_to_send > 0:
            print("Not enough amount to send.")
            return []

        for voucher, amount_to_send in selected_vouchers:
            transaction = VoucherTransaction(voucher)
            transaction_data = transaction.do_transaction(amount_to_send, person.id, recipient_id, person.key)
            voucher.transactions.append(transaction_data)

        return selected_vouchers
