# person.py
from src.models.key import Key
from src.models.vouchertransaction import VoucherTransaction
from src.models.usertransaction import UserTransaction
from src.services.utils import get_timestamp, dprint, amount_precision, get_double_spending_vtransaction_ids
import json

class Person:
    def __init__(self, person_data, seed=None):
        self.key = Key(seed) if seed else Key()
        self.id = self.key.id
        self.pubkey_short = self.key.get_compressed_public_key()

        # Setting attributes from the person_data dictionary
        self.first_name = person_data.get('first_name')
        self.last_name = person_data.get('last_name')
        self.organization = person_data.get('organization')
        self.address = person_data.get('address')
        self.gender = person_data.get('gender')  # 0 for unknown, 1 for male, 2 for female
        self.email = person_data.get('email')
        self.phone = person_data.get('phone')
        self.service_offer = person_data.get('service_offer')  # Offer / Skills
        self.coordinates = person_data.get('coordinates')
        self.current_voucher = None  # Initialization of current_voucher
        self.vouchers = []  # List of vouchers with amount
        self.used_vouchers = []  # List of used vouchers after transaction without amount
        self.usertransaction = UserTransaction()

    def init_empty_voucher(self):
        from src.models.minuto_voucher import MinutoVoucher
        self.current_voucher = MinutoVoucher()

    def create_voucher(self, amount, region, validity):
        """ Erstellt einen neuen MinutoVoucher. """
        from src.models.minuto_voucher import MinutoVoucher
        self.current_voucher = MinutoVoucher.create(self.id, self.first_name, self.last_name, self.organization, self.address, self.gender, self.email, self.phone, self.service_offer, self.coordinates, amount, region, validity)

    def check_double_spending(self):
        """
        Identifies and returns information about double spending incidents on all available vouchers.

        This function checks for transactions that have the same previous_hash across all vouchers,
        indicating potential double spending. For each set of such transactions, it extracts the user_id
        of the double spender, the transaction_ids involved, and the affected voucher_id.

        Returns:
        list of dict: A list where each dictionary contains the following keys:
                      'double_spender_id': The user ID of the person who double spent,
                      'transaction_ids': A list of transaction IDs involved in the double spending,
                      'voucher_id': The ID of the voucher on which double spending occurred.
                      Returns an empty list if no double spending is detected.
        """
        from src.models.minuto_voucher import MinutoVoucher
        all_vouchers = self.vouchers + self.used_vouchers
        double_spends = get_double_spending_vtransaction_ids(all_vouchers)
        number_of_double_spends = len(double_spends)
        if number_of_double_spends == 0:
            return []

        # If double spends, then detect user id that double spends
        double_spend_info = []
        for dspend_t_ids in double_spends:
            for voucher in all_vouchers:
                for transaction in voucher.transactions:
                    if transaction["t_id"] not in dspend_t_ids:
                        continue

                    user_id = transaction["sender_id"]  # The sender is the double spender
                    max_allowed_amount = MinutoVoucher.get_transaction_amount(voucher, user_id, transaction["t_id"])

                    # Find the user's info if it exists
                    user_info = next((info for info in double_spend_info if info['double_spender_id'] == user_id), None)

                    if not user_info:
                        # If user info doesn't exist, add it with the current voucher and transaction
                        double_spend_info.append({
                            "double_spender_id": user_id,
                            "voucher": [{"voucher_id": voucher.voucher_id, "max_allowed_amount": max_allowed_amount, "send_amount" : str(transaction["amount"]),
                                         "transactions": [transaction]}]})
                    else:
                        # Find the voucher info if it exists
                        voucher_info = next((v for v in user_info['voucher'] if v['voucher_id'] == voucher.voucher_id),
                                            None)

                        if not voucher_info:
                            # If voucher info doesn't exist, add it with the current transaction
                            user_info['voucher'].append(
                                {"voucher_id": voucher.voucher_id, "max_allowed_amount": max_allowed_amount, "send_amount" : str(transaction["amount"]),
                                 "transactions": [transaction]})
                        else:
                            # If voucher exists, append transaction_id
                            voucher_info['transactions'].append(transaction)
                            voucher_info["send_amount"] = str(float(voucher_info["send_amount"]) + float(transaction["amount"]))

        return double_spend_info

    def read_voucher_and_save_voucher(self, filename, subfolder=None, simulation = False):
        """read the voucher and stores it to persons voucher list"""
        self.read_voucher(filename, subfolder, simulation)
        self.vouchers.append(self.current_voucher)

    def read_voucher(self, filename, subfolder=None, simulation = False):
        """read the voucher"""
        self.init_empty_voucher()
        self.current_voucher = self.current_voucher.read_from_file(filename, subfolder, simulation)

    def save_voucher(self, filename = None, subfolder=None, voucher=None, simulation = False):
        if voucher == None:
            return self.current_voucher.save_to_disk(filename, subfolder, simulation)
        return voucher.save_to_disk(filename, subfolder, simulation)

    def save_all_vouchers(self, subfolder=None, fileprefix='', prefix_only=False):
        """saves all vouchers to disk"""
        filename = ''
        i = 0
        for voucher in self.vouchers:
            i += 1
            if len(fileprefix) > 0:
                filename = f"{str(fileprefix)}-"
            if not prefix_only:
                filename += f"{str(self.id)[:8]}"
            filename += f"-v{i}.txt"
            self.save_voucher(filename, subfolder, voucher)

    def sign_voucher_as_guarantor(self, voucher=None):
        """ Signs the voucher including the guarantor's personal details. """
        voucher = voucher or self.current_voucher

        if voucher.creator_id == self.id:
            print("Guarantors cannot sign their own vouchers.")
            return

        for g_sign in voucher.guarantor_signatures:
            if g_sign[0]["id"] == self.id:
                print("Vouchers cannot be signed by the same guarantor more than once.")
                return

        # Prepare guarantor information for signature
        guarantor_info = {
            "id": self.id,
            "name": self.first_name,
            "name": self.last_name,
            "name": self.organization,
            "address": self.address,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "coordinates": self.coordinates,
            "signature_time": get_timestamp()
        }

        # get voucher data for signing
        data_to_sign = voucher.get_voucher_data(type="guarantor_signature", guarantor_info=guarantor_info)
        signature = self.key.sign(data_to_sign, base64_encode=True)

        # Append the signed guarantor information to the voucher
        voucher.guarantor_signatures.append((guarantor_info, signature))

    def verify_guarantor_signatures(self, voucher=None):
        """ Validates all guarantor signatures on the voucher. """
        voucher = voucher or self.current_voucher
        return voucher.verify_all_guarantor_signatures(voucher)

    def sign_voucher_as_creator(self, voucher=None):
        """ Calculates voucher_id signs the voucher as its creator and initialize the transaction list"""
        voucher = voucher or self.current_voucher
        voucher.voucher_id = voucher.calculate_voucher_id()  # set voucher_id

        # Check if male and female guarantor exist
        guarantor_genders = {str(g_sign[0]['gender']) for g_sign in voucher.guarantor_signatures}
        if '1' not in guarantor_genders or '2' not in guarantor_genders:
            print("One male and one female guarantor required before signing as creator.")
            return

        if not self.verify_guarantor_signatures():
            print("Signatures of guarantors are invalid.")
            return

        if voucher.creator_id != self.id:
            print("Can only sign own voucher as creator!")
            return

        data_to_sign = voucher.get_voucher_data(type="creator_signing")
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
        Send a specified amount to a person (recipient) using available vouchers.

        :param amount: The amount to send.
        :param recipient_id: The ID of the recipient.
        :return: List of vouchers used for the transaction.
        """
        transaction = self.usertransaction.process_transaction_to_user(self, amount, recipient_id)

        # clean vouchers with empty amount (balance)
        # Create a new list for the remaining vouchers
        remaining_vouchers = []

        for voucher in self.vouchers:
            if voucher.get_voucher_amount(self.id) == 0:
                self.used_vouchers.append(voucher)  # Add empty voucher to the empty vouchers list
            else:
                remaining_vouchers.append(voucher)  # Keep the voucher if it's not empty

        # Update the self.vouchers list with the remaining vouchers
        self.vouchers = remaining_vouchers

        return transaction

    def receive_amount(self, user_transaction):
        """
        Receives a transaction from another person, which may contain multiple vouchers,
        and stores these transactions in the recipient's own list of vouchers.

        This method takes a UserTransaction representing the incoming transaction,
        and appends the vouchers involved in this transaction to the recipient's voucher list.

        :param user_transaction: UserTransaction object containing the transaction details
                                 and the vouchers to be received.
        """
        self.usertransaction.receive_transaction_from_user(user_transaction, self)

    def list_vouchers(self):
        """prints a short list of all vouchers"""
        full_amount = amount_precision(self.get_amount_of_all_vouchers())
        print(f"\033[1m{self.name} {self.id[:6]}.. - {len(self.vouchers)} Vouchers  (Full Amount: {full_amount} Min)\033[0m")
        sorted_vouchers = sorted(self.vouchers, key=lambda voucher: voucher.creator_id)
        creator_id = ''
        linetext = ''
        for voucher in sorted_vouchers:
            if creator_id != voucher.creator_id:
                if creator_id != '':
                    print(linetext)
                linetext = f"V-Creator: {voucher.creator_first_name} {voucher.creator_last_name} \tV-Amounts: {voucher.get_voucher_amount(self.id)}M"
                creator_id = voucher.creator_id
            else:
                linetext += f"  {voucher.get_voucher_amount(self.id)}M"
        print(linetext)


    def get_amount_of_all_vouchers(self):
        """calculates the full amount of all vouchers of the person"""
        full_amount = 0
        for voucher in self.vouchers:
            full_amount += voucher.get_voucher_amount(self.id)
        return full_amount

    def check_duplicate_voucher_objects(self):
        """
        Identifies and reports all duplicate voucher object IDs within the individual's list of vouchers.
        Raises a ValueError if any duplicates are found. This method is primarily intended for debugging
        purposes during simulations and is not required during regular use.
        """

        v_object_id_counts = {}
        for voucher in self.vouchers:
            voucher_id = id(voucher)
            if voucher_id in v_object_id_counts:
                v_object_id_counts[voucher_id] += 1
            else:
                v_object_id_counts[voucher_id] = 1

        duplicates = [v_id for v_id, count in v_object_id_counts.items() if count > 1]

        if duplicates:
            print(f"Duplicate voucher object IDs found: {duplicates}")
            print(v_object_id_counts)
            raise ValueError("Duplicate voucher object(s) detected")

    def __str__(self):
        return f"Person({self.id}, {self.name}, {self.address}, {self.gender}, {self.email}, {self.phone}, {self.service_offer}, {self.coordinates})"
