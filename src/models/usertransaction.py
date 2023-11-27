from src.models.vouchertransaction import VoucherTransaction
from src.services.utils import dprint, amount_precision

class UserTransaction:
    """Manages transactions between users (persons). A user transaction can contain multiple vouchers."""

    def __init__(self):
        self.transaction_vouchers = []
        self.transaction_successful = False
        self.transaction_amount = 0
        self.transaction_failure_reason = ""

    def process_transaction_to_user(self, person, amount, recipient_id, verbose=False):
        """
        Processes transactions by selecting suitable vouchers and creating transaction data.

        :param person: The person object initiating the transaction.
        :param amount: The amount to send.
        :param recipient_id: The ID of the recipient.
        :return: A UserTransaction object with the selected vouchers.
        """
        user_transaction = UserTransaction()
        user_transaction.transaction_amount = amount_precision(amount)
        remaining_amount_to_send = amount
        selected_vouchers = []

        for voucher in person.vouchers:
            if not voucher.verify_complete_voucher(verbose):
                continue  # Use only valid vouchers

            voucher_amount = voucher.get_voucher_amount(person.id)
            if voucher_amount == 0:  # use only vouchers with amount, ignore empty vouchers
                continue
            if voucher_amount > remaining_amount_to_send:
                # wähle diesen voucher und sende damit remaining_amount_to_send
                selected_vouchers.append((voucher, remaining_amount_to_send))
                remaining_amount_to_send = 0
                break
            else:
                # voucher nicht genug amount, nutze diese voucher komplett und den remaining_amount_to_send mit dem nächsten
                selected_vouchers.append((voucher, voucher_amount))
                remaining_amount_to_send -= voucher_amount


        if remaining_amount_to_send > 0:
            return self.return_transaction_failure(failure_reason="Not enough amount to send.")

        for voucher, send_amount in selected_vouchers:
            v_transaction = VoucherTransaction(voucher)
            transaction_data = v_transaction.do_transaction(send_amount, person.id, recipient_id, person.key)
            voucher.transactions.append(transaction_data)
            user_transaction.transaction_vouchers.append(voucher)

        user_transaction.transaction_successful = True
        return user_transaction

    def receive_transaction_from_user(self, transaction, person, verbose=False):
        """
        Receives a UserTransaction object and adds its vouchers to the person's list of vouchers.

        :param transaction: The UserTransaction object containing the transaction vouchers.
        :param person: The person object who is receiving the transactions.
        :param verbose: If True, provides detailed output during the process.
        """
        if not transaction.transaction_successful:
            print(f"Received failed transaction from sender. Reason: {transaction.transaction_failure_reason}")
            transaction.transaction_amount = 0
            self.return_transaction_failure("Received failed transaction from sender.")

        # Verify all new incoming vouchers
        for voucher in transaction.transaction_vouchers:
            if not voucher.verify_complete_voucher(verbose):
                if verbose:
                    print("Corrupt transaction received. Voucher verification failed.")
                self.return_transaction_failure("Corrupt voucher received.")

        transaction.transaction_amount = 0  # Reset to 0 and verify again
        for voucher in transaction.transaction_vouchers:
            v_amount = voucher.get_voucher_amount(person.id)
            if v_amount > 0:  # Only use vouchers with a positive amount
                if verbose:
                    print(f"Received voucher with {v_amount} amount.")
                person.vouchers.append(voucher)
                transaction.transaction_amount += v_amount
        return True  # Transaction successfully received

    def return_transaction_failure(self, failure_reason=""):
        """
        Handles a failed transaction by resetting relevant attributes.

        :param failure_reason: Reason for the transaction failure.
        :return: The updated transaction object.
        """
        self.transaction_amount = 0
        self.transaction_successful = False
        self.transaction_failure_reason = failure_reason
        self.transaction_vouchers = []
        return self
