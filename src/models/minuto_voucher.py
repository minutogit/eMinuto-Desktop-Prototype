# minuto_voucher.py
import json
import os
from src.models.key import Key
from src.services.utils import get_timestamp, dprint, amount_precision, Serializable, random_string, get_years_valid
from src.services.crypto_utils import get_hash
from src.models.voucher_transaction import VoucherTransaction
from enum import Enum

class VoucherStatus(Enum):
    UNFINISHED = "unfinished"  # List of vouchers which are not ready because of missing guarantor sign etc.
    USED = "used"  # List of used vouchers without amount
    OWN = "own"  # List of own created vouchers with amount.
    OTHER = "other"  # List of vouchers from other users with amount.
    TEMP = "temp"  # Temporary vouchers.
    DELETED = "deleted"  # Deleted vouchers (to keep until full deletion).
    CORRUPT = "corrupt"  # Vouchers where the verification fails (signature etc).


class MinutoVoucher(Serializable):
    def __init__(self):
        # Initialize default values for voucher attributes
        self.region = ''
        self.amount = 0
        self.description = ""
        self.valid_until = ''
        self.creator_id = ''
        self.creator_organization = ''
        self.creator_first_name = ''
        self.creator_last_name = ''
        self.creator_address = ''
        self.phone = ''
        self.email = ''
        self.creator_gender = 0  # 0 for unknown, 1 for male, 2 for female
        self.service_offer = ''
        self.creator_signature = None  # Creator's signature
        self.coordinates = ''
        self.guarantor_signatures = []  # Guarantor signatures
        self.needed_guarantors = 2 # minimum number of needed guarators signatures (included for possible future feature requests of more guarantors)
        self.transactions = []  # list of transactions
        self.creation_date = ''
        self.voucher_id = ''
        self.footnote = ""
        self.is_test_voucher = False  # Indicates if the voucher is a test voucher

        # local management values (not stored in voucher files)
        self._file_path = None # to store the local file locattion
        self._local_voucher_id = None # determined from the voucher


    @classmethod
    def create(cls, creator_id: str, creator_first_name: str, creator_last_name: str, creator_organization: str, creator_address, creator_gender: int, email: str, phone: str, service_offer: str, coordinates: str,
               amount: float, region: str, validity: int, is_test_voucher: bool = False, description='', footnote=''):
        # Create a new voucher instance with provided details
        voucher = cls()
        voucher.creator_id = creator_id
        voucher.creation_date = get_timestamp()
        voucher.creator_first_name = creator_first_name
        voucher.creator_last_name = creator_last_name
        voucher.creator_organization = creator_organization
        voucher.creator_address = creator_address
        voucher.creator_gender = creator_gender # unknown = 0, male = 1, female = 2
        voucher.amount = amount_precision(amount)
        if description == "":
            voucher.description = f"Voucher for goods or services worth {amount_precision(amount)} minutes of quality work."
        else:
            voucher.description = description
        if footnote == "":
            voucher.footnote = "Voucher redemption for Minuto players only."
        else:
            voucher.footnote = footnote
        voucher.service_offer = service_offer
        voucher.valid_until = get_timestamp(validity, end_of_year=True)
        voucher.region = region
        voucher.coordinates = coordinates
        voucher.email = email
        voucher.phone = phone
        voucher.is_test_voucher = is_test_voucher
        voucher.voucher_id = voucher.calculate_voucher_id()  # set voucher_id

        return voucher

    def get_voucher_data(self, type):
        # Dynamically generate the data for signing and hashing, including optional guarantor signatures

        # Initially, these keys are excluded from the hashing process.
        excluded_keys = ['guarantor_signatures', 'voucher_id', 'creator_signature',
                         'transactions']
        # By doing this, unknown keys are also dynamically included in the hash, enabling older versions to correctly verify hashes of newer versions with additional parameters.
        # removed keys which  start with _ are only locally needed. Not for hash or signatures.
        data = {key: value for key, value in self.__dict__.items()
                if key not in excluded_keys and not key.startswith('_')}

        # voucher id is hash from all key without the excluded
        if type in ["voucher_id_hashing"]:
            return json.dumps(data, sort_keys=True, ensure_ascii=False)

        # guarantor and creator only signs the voucher id, the initial_transaction_hash is hash from voucher_id
        data = {'voucher_id': self.voucher_id}
        if type in ["guarantor_signature",  "creator_signing", "initial_transaction_hash"]:
            return json.dumps(data, sort_keys=True, ensure_ascii=False)

        # Important: The initial_transaction_hash have to exclude the creator_signature (which changes with each signing)
        # from the hashing process. Also have exclude guarantor_signatures, because different signature from the same guarantor would lead to different previous_hash.
        #
        # This ensures a consistent previous_hash for the initial transaction.
        # A consistent previous_hash is necessary to detect double spending, particularly in cases of multiple
        # initializations of the initial transaction.

        # if unknown type raise error
        raise ValueError("Unknown type")

    def is_valid(self):
        """
        Checks the validity of the voucher.
        A voucher is considered valid if it has at least two guarantor signatures and a creator signature.
        """
        # Check the validity of the voucher
        return len(self.guarantor_signatures) >= 2 and self.creator_signature is not None

    def save_to_disk(self, file_path=None, subfolder=None, simulation=False):
        """
        Saves all attributes of the MinutoVoucher object either to a specified file path or returns the serialized data.
        If simulation mode is activated, the file_path is ignored and the serialized data is returned instead.

        :param file_path: Optional. The path of the file where the voucher data will be saved when not in simulation mode.
        :param subfolder: Optional. The subfolder under the script directory where the file will be saved. If no subfolder the file_path contains path and filename.
        :param simulation: If True, operates in simulation mode and returns the serialized data; otherwise, saves to the specified file path.
        :return: The serialized data if simulation mode is activated.
        """
        # Filter the __dict__ to remove keys starting with '_'
        filtered_data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        data_to_save = json.dumps(filtered_data, sort_keys=False, indent=4, ensure_ascii=False)

        if simulation:
            return data_to_save  # Return the serialized data in simulation mode
        else:
            base_dir = os.getcwd()  # Get the current working directory
            if subfolder:
                full_path = os.path.join(base_dir, subfolder, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
            else:
                full_path = file_path # if no subfolder, file_path contains the full path and name of file

            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(data_to_save)

    @classmethod
    def read_from_file(cls, file_path, subfolder=None, simulation=False):
        """
        Reads and creates a MinutoVoucher object from a file or a simulation variable.
        In simulation mode, the 'file_path' parameter is treated as the content of the simulation variable.

        :param file_path: The path of the file from which the voucher data will be read, or the content of simulation variable.
        :param subfolder: Optional. The subfolder under the script directory from where the file will be read.
        :param simulation: If True, operates in simulation mode for simulation purposes, otherwise performs actual file operations.
        :return: A MinutoVoucher object instantiated with the read data.
        """
        if simulation:
            data_str = file_path  # Treat 'file_path' as the content in simulation mode
        else:
            base_dir = os.getcwd()  # Get the current working directory
            if subfolder:
                full_path = os.path.join(base_dir, subfolder, file_path)
            else:
                full_path = os.path.join(base_dir, file_path)

            with open(full_path, 'r', encoding='utf-8') as file:
                data_str = file.read()

        data = json.loads(data_str)
        voucher = cls()
        for key, value in data.items():
            setattr(voucher, key, value)

        return voucher

    @classmethod
    def read_from_dict(cls, data):
        """
        Creates an instance of MinutoVoucher from a dictionary.

        Args:
            data (dict): The dictionary containing voucher data.

        Returns:
            MinutoVoucher: An instance of MinutoVoucher initialized with the data.
        """
        voucher = cls()

        # Set attributes from the dictionary
        for key, value in data.items():
            setattr(voucher, key, value)

        return voucher


    def get_voucher_amount(self, sender_id, voucher=None):
        """
        Calculates the available amount of the last transaction of the voucher based on the sender_id.
        If no voucher is provided, the method uses the current instance as the voucher.

        :param sender_id: The ID of the sender to calculate the available amount for.
        :param voucher: Optional. The voucher to calculate the amount for. Defaults to the current instance if not provided.
        :return: The calculated available amount.
        """
        # If no voucher is provided, use the current instance
        if voucher is None:
            voucher = self

        # Ensure there are transactions to evaluate
        if not voucher.transactions:
            return 0

        # Retrieve the last transaction
        last_transaction = voucher.transactions[-1]

        # For 'split' type, check if sender_id matches sender or recipient of the last transaction
        if last_transaction.get('t_type') == 'split':
            if sender_id == last_transaction['sender_id']:
                return float(last_transaction['sender_remaining_amount'])
            elif sender_id == last_transaction['recipient_id']:
                return float(last_transaction['amount'])

        # For non-split or undefined t_type, return amount if sender_id matches recipient of the last transaction
        elif sender_id == last_transaction['recipient_id']:
            return float(last_transaction['amount'])

        # Default case for other scenarios
        return 0  # or a suitable error message or logic

    @staticmethod
    def get_transaction_amount(voucher, dspender_id, trans_id):
        """bestimmt den maximal menge für einen voucher wie viele minuto für eine bestimmte transaktion hätten gesendet werden dürfen. Wird benötigt für double spending benötig um zu ermitteln ob auch tatsächlich mehr als erlaubt gesendet wurde."""
        previous_trans = None
        for trans in voucher.transactions:
            if trans["t_id"] == trans_id:
                if previous_trans == None:
                    # if initial transaction then there is no transaction before, voucher
                    return float(voucher.amount)
                else:
                    if previous_trans.get('t_type') == 'split':
                        if dspender_id == previous_trans['sender_id']:
                            return float(previous_trans['sender_remaining_amount'])
                        elif dspender_id == previous_trans['recipient_id']:
                            return float(previous_trans['amount'])

                    # For non-split or undefined t_type, return amount if sender_id matches recipient of the last transaction
                    elif dspender_id == previous_trans['recipient_id']:
                        return float(previous_trans['amount'])

            previous_trans = trans

        # Default case for other scenarios
        return 0

    def verify_all_guarantor_signatures(self, voucher=None):
        """ Validates all guarantor signatures on the given voucher.
        Does only check the signature of every single signature. Not if enough signatures etc."""
        if voucher is None:
            voucher = self
        if not voucher.guarantor_signatures:
            return False
        sign_number = 0

        for guarantor_info, signature in voucher.guarantor_signatures:
            # check if the signature belongs to this voucher
            if voucher.voucher_id != guarantor_info["voucher_id"]:
                return False

            try:
                pubkey_short = Key.get_pubkey_from_id(guarantor_info["id"])
            except:
                return False

            data_to_verify = json.dumps(guarantor_info, sort_keys=True, ensure_ascii=False)

            if not Key.verify_signature(data_to_verify, signature, pubkey_short):
                return False

            sign_number += 1

        return True

    def calculate_voucher_id(self, voucher=None):
        """calculate hash from voucher as voucher_id

        :return: voucher_id
        """
        if voucher is None:
            voucher = self
        data = self.get_voucher_data(type="voucher_id_hashing").encode()
        return get_hash(data)

    def verify_creator_signature(self, voucher=None, verbose=False):
        """ Verifies the creator's signature and voucher_id from voucher. """
        if voucher is None:
            voucher = self
        # check if voucher_id is correct calculated
        if voucher.voucher_id != self.calculate_voucher_id(voucher):
            if verbose:
                print("voucher_id is incorrect")
            return False

        # Check if both male and female guarantor exist
        guarantor_genders = {str(g_sign[0]['gender']) for g_sign in voucher.guarantor_signatures}
        if '1' not in guarantor_genders or '2' not in guarantor_genders:
            print("male and female guarantor needed")
            return False

        # check if enough guarantor signatures
        if len(voucher.guarantor_signatures) < voucher.needed_guarantors:
            print("not enough guarantors")
            return False

        signature = voucher.creator_signature
        if not signature:
            if verbose:
                print("missing creator signature")
            return False

        if Key.check_user_id(voucher.creator_id) == False:
            if verbose:
                print("creator id incorrect. wrong checksum")
            return False
        pubkey_short = Key.get_pubkey_from_id(voucher.creator_id)

        data_to_verify = voucher.get_voucher_data(type="creator_signing")
        signature_valid = Key.verify_signature(data_to_verify, signature, pubkey_short)
        if not signature_valid:
            if verbose:
                print("invalid creator signature")
            return False
        return signature_valid

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

        # to catch key erros when corrupt file
        try:
            # Validate that the initial transaction meets expected conditions
            if initial_transaction['t_type'] != 'init' or \
                    initial_transaction['recipient_id'] != self.creator_id or \
                    initial_transaction['amount'] != self.amount or \
                    initial_transaction['sender_id'] != self.creator_id:
                return False

            # Verify the linkage to the voucher - verify hash from voucher id
            data_for_prev_hash = self.get_voucher_data(type="initial_transaction_hash").encode()
            if get_hash(data_for_prev_hash) != initial_transaction['previous_hash']:
                return False

            # Verify transaction ID and the correct signature of the sender (creator)
            if VoucherTransaction.calculate_transaction_id(initial_transaction) != initial_transaction['t_id']:
                return False
        except:
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
        if not transaction["t_id"] == VoucherTransaction.calculate_transaction_id(transaction):
            return False

        # Verify the signature against the sender's public key
        pubkey = Key.get_pubkey_from_id(transaction['sender_id'])
        is_signature_valid = Key.verify_signature(transaction["t_id"],
                                                  transaction['sender_signature'],
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

        # to catch key erros when corrupt file
        try:

            # Loop through and verify each subsequent transaction
            for i in range(1, len(self.transactions)):
                current_transaction = self.transactions[i]
                previous_transaction = self.transactions[i - 1]

                if verbose:
                    print(f"Verifying transaction: {i} - ID: {current_transaction['t_id'][:6]}...")

                # Verify the transaction ID and the sender's signature
                if not self.verify_transaction_ids_signature(current_transaction):
                    if verbose:
                        print("VoucherTransaction ID or sender's signature verification failed.")
                    return False

                if verbose:
                    print("VoucherTransaction ID and Signature are okay")

                # Verify if the sender was authorized to send
                allowed_senders = [previous_transaction['recipient_id']]
                if previous_transaction.get('t_type', '') == 'split':
                    allowed_senders.append(previous_transaction['sender_id'])
                if current_transaction['sender_id'] not in allowed_senders:
                    if verbose:
                        print(f"Sender {current_transaction['sender_id'][:6]}... was not authorized to send.")
                    return False

                if verbose:
                    print(f"Sender {current_transaction['sender_id'][:6]}... was allowed to send")

                # Verify if the sent amount was permissible
                # Typically, the recipient of the last transaction is the sender of the current transaction
                allowed_amount = float(previous_transaction['amount'])
                if previous_transaction.get('t_type', '') == 'split' and current_transaction['sender_id'] == \
                        previous_transaction['sender_id']:
                    # when after split transaction the sender will send again, the remaining amount of the prev. transaction is the allowed amount
                    allowed_amount = float(previous_transaction['sender_remaining_amount'])
                if float(current_transaction['amount']) > allowed_amount:
                    if verbose:
                        print(f"Too much sent! {float(current_transaction['amount'])} Minuto (max allowed {allowed_amount})")
                    return False

                if verbose:
                    print(f"Received {float(current_transaction['amount'])} Minuto (max allowed {allowed_amount})")

                # Verify the linkage to the previous transaction
                previous_transaction_hash = get_hash(json.dumps(previous_transaction, sort_keys=True).encode())
                if current_transaction['previous_hash'] != previous_transaction_hash:
                    if verbose:
                        print("Linkage to the previous transaction failed.")
                    return False

                if verbose:
                    print("Linkage (Hash of the previous transaction) is correct\n")

        except:
            return False

        if verbose:
            print("All transactions are okay")
        return True

    def verify_complete_voucher(self, verbose=False):
        """
        Verifies the entire voucher including guarantor signatures, creator's signature, and all transactions.

        :return: True if the entire voucher is valid, False otherwise.
        """
        if not self.calculate_voucher_id() == self.voucher_id:
            if verbose:
                print("Incorrect voucher ID.")
            #return False

        # Verify guarantor signatures
        if not self.verify_all_guarantor_signatures(self):
            if verbose:
                print("Guarantor signature verification failed.")
            return False

        # Verify creator's signature
        # Checks also the number of guarantor signatures and if at least one male and female guarantor
        if not self.verify_creator_signature(self):
            if verbose:
                print("Creator signature verification failed.")
            return False

        # Verify all transactions (at least initial transaction need to be done)
        if not self.verify_all_transactions(verbose):
            if verbose:
                print("Voucher Transaction verification failed.")
            return False

        return True


    def voucher_status(self, user_id):  # -> VoucherStatus
        """
        Returns the status of vouchers such as 'used', 'unfinished', etc.
        This method is used for storing vouchers.

        Args:
            user_id: The user ID to check if own voucher.

        Returns:
            VoucherStatus: The status of the vouchers.
        """
        own_voucher = (self.creator_id == user_id)
        if not self.transactions:
            return VoucherStatus.UNFINISHED

        if self.verify_complete_voucher():
            # Own vouchers can only be used when older than 3 years
            if own_voucher:
                if get_years_valid(self.valid_until) > 3 or self.get_voucher_amount(user_id) > 0:
                    return VoucherStatus.OWN
                else:
                    return VoucherStatus.USED

            # Other valid vouchers
            if self.get_voucher_amount(user_id) > 0:
                return VoucherStatus.OTHER  # Vouchers from other users with amount
            elif self.transactions[-1]['sender_id'] == user_id:
                return VoucherStatus.USED
            else:
                return VoucherStatus.DELETED
        else:
            return VoucherStatus.CORRUPT

    def get_local_voucher_id(self, user_id, voucher=None):
        """
        Generates a current local identifier and a list of old local identifiers for a voucher.
        The first element of the returned list is the current local ID (current_local_id), and the following IDs are the old IDs of the voucher.
        Each identifier is constructed from parts of the voucher's global ID and the transaction IDs in which the user was involved as sender or recipient.

        This approach provides a list of all (including previous) local IDs, making it possible to detect and replace older versions
        of the voucher if they exist. This further reduces the likelihood of unintended double spendings due to possible
        program errors or outdated backups being restored.
        If a string of 16 zeros is returned, the voucher was not intended for the local user and is therefore irrelevant. The calling function can use this information to completely delete such vouchers,
        maintaining the integrity of the local voucher data.

        Args:
            user_id: The user ID to check the voucher transactions against.
            voucher (optional): The voucher instance from which to generate the local IDs. If not provided, 'self' is used.

        Returns:
            tuple: A tuple containing the current local ID and a list of old local IDs.
        """
        old_local_ids = []
        if voucher is None:
            voucher = self
        if voucher.transactions:
            # Iterate through transactions from the last to the first and add a local ID for each transaction involving the user
            for transaction in reversed(voucher.transactions):
                if user_id == transaction['recipient_id'] or user_id == transaction['sender_id']:
                    last_transaction_id = transaction['t_id']
                    old_local_ids.append(voucher.voucher_id[:8] + '-' + last_transaction_id[:8])

            # Add a default identifier based on the voucher_id if there are no transactions involving the user
            # and if the voucher's creator is not the user, then the voucher was not intended for the local user and is therefore irrelevant.
            if not old_local_ids and voucher.creator_id != user_id:
                old_local_ids.append('0' * 16)

        # always append this to have always a local_id
        old_local_ids.append(voucher.voucher_id[:16])
        current_local_id = old_local_ids.pop(0) # removes first element of the list and set current_local_id to first element
        return current_local_id, old_local_ids

    def __str__(self):
        # Dynamische Erstellung des String-Formats für alle Attribute
        attrs = vars(self)
        attrs_str = ', '.join([f"{key}: {value}" for key, value in attrs.items()])

        return f"MinutoVoucher({attrs_str})"

    def __eq__(self, other):
        # compare with string representation of the voucher
        if not isinstance(other, MinutoVoucher):
            return False

        return str(self) == str(other)

def is_voucher_dict(data):
    """
    Checks if the dictionary contains all essential keys that are necessary to represent
    a MinutoVoucher. This method is designed to identify if a given dictionary is likely
    to be a representation of a MinutoVoucher instance. The method does not utilize all keys
    as future versions might add new keys or discontinue the use of existing ones. To ensure
    accurate classification of vouchers in the future, only the most critical keys, which are
    likely to remain consistent, are checked.

    Args:
        data (dict): The dictionary to check.

    Returns:
        bool: True if the dictionary contains all essential keys, False otherwise.
    """
    # The most important parameters of the class, which are likely to always remain.
    required_keys = [
        'valid_until', 'creator_id', 'creator_signature', 'guarantor_signatures',
        'transactions', 'creation_date', 'voucher_id'
    ]
    return all(key in data for key in required_keys)