# user_transaction.py
from src.models.voucher_transaction import VoucherTransaction
from src.services.utils import dprint, amount_precision, Serializable, get_timestamp
from src.models.minuto_voucher import VoucherStatus, MinutoVoucher


class UserTransaction(Serializable):
    """Manages transactions between users (persons). A user transaction can contain multiple vouchers."""

    def __init__(self):
        self.transaction_sender_id = ""
        self.transaction_recipient_id = ''
        self.transaction_amount = 0
        self.transaction_purpose = ""
        self.transaction_start_timestamp = ""
        self.transaction_end_timestamp = ""
        self.transaction_vouchers = []
        self.transaction_successful = False
        self.transaction_failure_reason = ""

    def process_transaction_to_user(self, person, amount, recipient_id, purpose = "", verbose=False):
        """
        Processes transactions by selecting suitable vouchers and creating transaction data.

        :param person: The person object initiating the transaction.
        :param amount: The amount to send.
        :param recipient_id: The ID of the recipient.
        :return: A UserTransaction object with the selected vouchers.
        """
        user_transaction = UserTransaction()
        user_transaction.transaction_start_timestamp = get_timestamp()
        user_transaction.transaction_sender_id = person.id
        user_transaction.transaction_recipient_id = recipient_id
        user_transaction.transaction_amount = amount_precision(amount)
        user_transaction.transaction_purpose = purpose
        remaining_amount_to_send = amount
        selected_vouchers = []

        for list_type in [VoucherStatus.OTHER.value, VoucherStatus.OWN.value]:
            for voucher in person.voucherlist[list_type]:
                if not voucher.verify_complete_voucher(verbose):
                    continue  # Use only valid vouchers

                voucher_amount = voucher.get_voucher_amount(person.id)
                if voucher_amount == 0:  # use only vouchers with amount, ignore empty vouchers
                    continue
                if voucher_amount >= remaining_amount_to_send:
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
        user_transaction.transaction_end_timestamp = get_timestamp()
        #dprint(user_transaction)
        return user_transaction

    def receive_transaction_from_user(self, transaction, person, verbose=False, receive_temp = False):
        """
        Receives a UserTransaction object and adds its vouchers to the person's list of vouchers.

        :param transaction: The UserTransaction object containing the transaction vouchers.
        :param person: The person object who is receiving the transactions.
        :param verbose: If True, provides detailed output during the process.
        :param receive_temp: If True, vouchers will stored to temp list. (not to integrate the vouchers immediately but to respond to user interaction if necessary)
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

        person.voucherlist[VoucherStatus.TEMP.value] = [] # clear temp voucher list
        transaction.transaction_amount = 0  # Reset to 0 and verify again
        for voucher in transaction.transaction_vouchers:
            v_amount = voucher.get_voucher_amount(person.id)
            if v_amount > 0:  # Only use vouchers with a positive amount
                if verbose:
                    print(f"Received voucher with {v_amount} amount.")
                if receive_temp:
                    person.voucherlist[VoucherStatus.TEMP.value].append(voucher)
                else:
                    voucher_status = voucher.voucher_status(person.id)
                    person.voucherlist[voucher_status.value].append(voucher) # append to the relevant list
                transaction.transaction_amount += v_amount
        return True  # Transaction successfully received

    def return_transaction_failure(self, failure_reason=""):
        """
        Handles a failed transaction by resetting relevant attributes.

        :param failure_reason: Reason for the transaction failure.
        :return: The updated transaction object.
        """

        self.transaction_sender_id = ""
        self.transaction_recipient_id = ''
        self.transaction_amount = 0
        self.transaction_purpose = ""
        self.transaction_start_timestamp = ""
        self.transaction_end_timestamp = ""
        self.transaction_vouchers = []
        self.transaction_successful = False
        self.transaction_failure_reason = failure_reason
        return self


    def to_dict(self):
        """
        Extends the base to_dict method to ensure all MinutoVoucher objects are also properly converted to dicts.
        """
        data = super().to_dict()  # Get the base dict from Serializable
        # Convert all vouchers to dicts
        data['transaction_vouchers'] = [voucher.to_dict() for voucher in self.transaction_vouchers]
        return data

    @classmethod
    def from_dict(cls, dict_):
        instance = cls()  # Erstellen einer neuen Instanz von UserTransaction

        # Wiederherstellen der Grundattribute
        for key, value in dict_.items():
            if key != 'transaction_vouchers':
                setattr(instance, key, value)

        # Wiederherstellen der MinutoVoucher-Objekte in der transaction_vouchers Liste
        if 'transaction_vouchers' in dict_:
            voucher_dicts = dict_['transaction_vouchers']
            instance.transaction_vouchers = [MinutoVoucher.from_dict(vd) for vd in voucher_dicts]

        return instance

    def __str__(self):
        # Get the dictionary representation of the object
        object_dict = self.to_dict()
        # Convert the dictionary to a string (you can customize this format as you like)
        return str(object_dict)
