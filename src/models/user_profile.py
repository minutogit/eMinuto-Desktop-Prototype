# user_profile.py
from src.services.utils import convert_json_string_to_dict, file_exists, join_path, Serializable, read_file_content, \
    is_valid_object, dprint, display_balance
from src.services.crypto_utils import generate_symmetric_key, symmetric_encrypt, symmetric_decrypt, b64d, is_encrypted_string, hash_bytes
from src.models.secure_file_handler import SecureFileHandler
from src.models.person import Person
from src.models.minuto_voucher import is_voucher_dict, VoucherStatus, MinutoVoucher, is_user_transaction_dict
from src.models.user_transaction import UserTransaction
class UserProfile(Serializable):
    # Singleton instance of UserProfile.
    # Ensures a single, globally accessible user profile instance across the application.
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Required for singleton instance"""
        if not cls._instance:
            cls._instance = super(UserProfile, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize the profile state
        self.initialize_state()
        self._secure_file_handler: SecureFileHandler = None
        self._user_transaction = UserTransaction()

    def initialize_state(self):
        """Initialize or reset the state of the profile."""
        self.person_data = {
            'first_name': '',
            'last_name': '',
            'organization': '',
            'street': '',
            'zip_code': '',
            'city': '',
            'state_or_region': '',
            'country': '',
            'gender': 0,
            'email': '',
            'phone': '',
            'service_offer': '',
            'coordinates': ''
        }

        self.profile_name = ""
        self.balance = 0
        self.transaction_pin = None
        self.encrypted_seed_words = None
        self.encryption_key = None # key for profile encryption
        self.encryption_salt = None
        self.data_folder = 'mdata'  # static folder for the app
        self.profile_filename = 'userprofile.dat'
        self.person = Person()
        self._profile_initialized = False
        self.file_enc_key = None # key for encyption of local files (vouchers)

        # Initialize the vouchers management dictionary. This dictionary is used for managing vouchers in memory and
        # won't be stored on disk (excluded in the self.to_dict method). It is initialized at startup.
        self.vouchers = {}

    def init_existing_profile(self,password):
        if not self.load_profile_from_disk(password):
            return False
        seed = symmetric_decrypt(self.encrypted_seed_words, password)
        self.person = Person(self.person_data, seed=seed)
        self._secure_file_handler = SecureFileHandler(self.person.key.private_key, self.person.id) # prvate key needed for encrytion with other users
        self.read_vouchers_from_disk()
        return True

    def read_vouchers_from_disk(self):
        """
        Reads vouchers from disk and categorizes them based on their types.
        It expects the folders to be named according to the VoucherStatus enum.
        """
        import os
        for status in VoucherStatus:  # Iterate over each status in the VoucherStatus enum
            folder_name = status.value  # Get the folder name corresponding to the voucher status
            folder_path = os.path.join(self.data_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # List all files in the directory
            for filename in os.listdir(folder_path):
                # Check if the file is a .mv file
                if filename.endswith('.mv'):
                    full_file_path = os.path.join(folder_path, filename)
                    if status == VoucherStatus.TRASHED:
                        self.open_voucher(full_file_path, trashed=True)
                    else:
                        self.open_voucher(full_file_path)

    def open_file(self, file_path):
        """
        Opens and reads vouchers, signatures, or transactions from user interaction in the GUI.
        Decrypts the content if necessary and processes it based on its type (voucher, transaction, or signature).
        """
        return_info = ""
        file_content = read_file_content(file_path)

        if is_encrypted_string(file_content):
            try:
                # First, try to decrypt received files from other users with a shared secret
                file_content = self._secure_file_handler.decrypt_with_shared_secret_and_load(file_path)
            except:
                try:
                    # If decryption from another user fails, try to decrypt with own file key
                    file_content = symmetric_decrypt(file_content, key=self.file_enc_key)
                except:
                    print("Decryption failed")
                    return None, "Entschlüsselung fehlgeschlagen"

        if is_valid_object(file_content):
            # If the content is a string, then convert it to a dictionary
            if isinstance(file_content, str):
                file_content = convert_json_string_to_dict(file_content)

            # Check if the content is a voucher dictionary
            if is_voucher_dict(file_content):
                self.person.read_voucher_from_dict(file_content)
                voucher_status = self.person.current_voucher.voucher_status(self.person.id)
                voucher_amount = self.person.current_voucher.get_voucher_amount(self.person.id)

                # Determine voucher status and set return information accordingly
                if voucher_status in [VoucherStatus.OWN, VoucherStatus.OTHER]:
                    return_info = f"Gutschein mit {voucher_amount}M Guthaben hinzugefügt."
                elif voucher_status == VoucherStatus.ARCHIVED:
                    return_info = "Gutschein hat kein Guthaben."
                elif voucher_status == VoucherStatus.UNFINISHED:
                    return_info = "Unfertigen Gutschein hinzugefügt."

                # Retrieve all local_ids that are already saved in self.vouchers
                local_id, _ = self.person.current_voucher.get_local_voucher_id(self.person.id)
                all_local_ids = [info['local_vid'] for info in self.vouchers.values()]
                existing_vouchers = (local_id in all_local_ids)

                # If the voucher does not already exist, add it to the voucher list and voucher management
                if not existing_vouchers:
                    self.person.voucherlist[voucher_status.value].append(self.person.current_voucher)
                    self.vouchers[id(self.person.current_voucher)] = {
                        'local_vid': local_id, 'file_path': None, 'trashed': False}
                    self.save_voucher_to_disk(self.person.current_voucher)
                else:
                    # Todo (optional improvement): Avoid adding older voucher versions when a newer version exists
                    return_info = "Gutschein existiert schon."
                    self.person.current_voucher = None

            # Check if the content is a user transaction dictionary
            elif is_user_transaction_dict(file_content):
                self.person.current_voucher = None  # Reset current voucher
                # Convert dictionary to transaction object
                transaction_object = self._user_transaction.from_dict(file_content)

                # Receive transaction from user, checks if valid vouchers in transaction, and stores vouchers in voucherlist[temp]
                if self._user_transaction.receive_transaction_from_user(transaction_object, self.person,
                                                                        receive_temp=True):
                    # Todo: additional -checks if all is successful (sum of total amount before and after transaktion)
                    all_local_ids = [info['local_vid'] for info in self.vouchers.values()]
                    existing_vouchers = any(voucher.get_local_voucher_id(self.person.id)[0] in all_local_ids
                                         for voucher in self.person.voucherlist[VoucherStatus.TEMP.value])

                    # if there are existing vouchers in the transaction don't import vouchers of transaction
                    if existing_vouchers:
                        return_info = ("Transaktion konnte nicht empfangen werden, da die enthaltenen Gutscheine schon "
                                       "existieren. (Alte bereits empfangene Transaktion?)")
                    else: # avoid adding same voucher again (possible if try to load same transaction again)
                        # Iterate over a copy to avoid errors from modifying the list during iteration.
                        temp_voucher_list = self.person.voucherlist[VoucherStatus.TEMP.value][:]
                        for voucher in temp_voucher_list:
                            # Retrieve and store the local voucher ID
                            local_id, _ = voucher.get_local_voucher_id(self.person.id)

                            # Add voucher to management dictionary
                            self.vouchers[id(voucher)] = {'local_vid': local_id, 'file_path': None, 'trashed': False}
                            # Todo: Ask user if store vouchers
                            self.save_voucher_to_disk(voucher)
                        return_info = f"Transaktion mit {transaction_object.transaction_amount} Minuto erfolgreich empfangen"

                    self.person.voucherlist[VoucherStatus.TEMP.value] = []  # Clean temp list

                else:
                    return_info = "Transaktion konnte nicht empfangen werden."

            # Check if the content is a guarantor signature
            elif isinstance(file_content, list) and isinstance(file_content[0], dict) and "signature_time" in \
                    file_content[0]:
                # Try to find voucher and add guarantor signature
                self.person.current_voucher, return_info = self.person.add_received_signature_to_unfinished_voucher(
                    file_content)

                # Save updated voucher to disk
                if self.person.current_voucher is not None:
                    self.save_voucher_to_disk(self.person.current_voucher)
            else:
                return_info = "unbekanntes Format"

        else:
            return_info = "Ungültige Datei"

        voucher = self.person.current_voucher
        self.person.current_voucher = None
        return voucher ,return_info

    def open_voucher(self, file_path, trashed=False):
        """
        Opens and reads a voucher file at startup.

        Args:
            file_path (str): The path of the file to be opened.
            trashed (bool): Indicates whether the voucher is marked as trashed. Defaults to False.

        Todo:
            - Check if a new voucher has already been sent to reduce the possibility of double spending when users make mistakes.
            - Check if the voucher is already loaded (add list of all loaded local_voucher_ids) or if a new version is loaded (use old_local_ids).
        """
        file_content = read_file_content(file_path)

        # Decrypt the content if it's encrypted
        if is_encrypted_string(file_content):
            try:
                file_content = symmetric_decrypt(file_content, key=self.file_enc_key)
            except Exception as e:
                print(f"Local voucher decryption failed: {e}")

        # Validate and process the voucher content
        if is_valid_object(file_content):
            # Convert string to dictionary if necessary
            if isinstance(file_content, str):
                file_content = convert_json_string_to_dict(file_content)

            # Process the voucher if it's in the correct format
            if is_voucher_dict(file_content):
                self.person.read_voucher_from_dict(file_content)


                # Retrieve and store the local voucher ID
                local_id, old_local_ids = self.person.current_voucher.get_local_voucher_id(self.person.id)


                # Determine and set the voucher status
                voucher_status = self.person.current_voucher.voucher_status(self.person.id)
                if trashed:  # Mark the voucher as trashed if the file is in the trash folder
                    voucher_status = VoucherStatus.TRASHED

                # add voucher to managment dict
                self.vouchers[id(self.person.current_voucher)] = {'local_vid': local_id, 'file_path': file_path, 'trashed': trashed}

                # Add the voucher to the list
                self.person.voucherlist[voucher_status.value].append(self.person.current_voucher)
                self.person.current_voucher = None  # Reset the current voucher

    def delete_voucher(self, voucher):
        """
        Permanently deletes a voucher file, making recovery impossible, and removes it from the user's trashed voucher list and management list.

        Args:
            voucher: The voucher object to be deleted.
        """

        # Delete the file from the filesystem
        self._secure_file_handler.delete_file(self.vouchers[id(voucher)]['file_path'])

        # Remove the voucher from the user's trashed voucher list
        user_profile.person.voucherlist[VoucherStatus.TRASHED.value].remove(voucher)

        # Remove the voucher from management list
        self.vouchers.pop(id(voucher), None)

    def save_voucher_to_disk(self, voucher:MinutoVoucher, trash=False):
        # save vouher to disk

        voucher_stored_on_disk = (self.vouchers[id(voucher)]['file_path'] is not None)

        local_id, old_local_ids = voucher.get_local_voucher_id(self.person.id)
        if trash:
            # if voucher already in trash -> really delete voucher file
            if self.vouchers[id(voucher)]['trashed']:  # voucher._trashed:
                self.delete_voucher(voucher)
                return
            self.vouchers[id(voucher)]['trashed'] = True
            voucher_status = VoucherStatus.TRASHED.value

        else:
            voucher_status = voucher.voucher_status(self.person.id).value
            self.vouchers[id(voucher)]['trashed'] = False

        import os

        file_path = os.path.join(self.data_folder, voucher_status)
        voucher_name = f"eMinuto-{local_id}.mv"
        new_full_file_path = str(os.path.join(self.data_folder, voucher_status, voucher_name))

        old_path = None # for checking if new path
        if voucher_stored_on_disk and self.vouchers[id(voucher)]['file_path'] != new_full_file_path:
            old_path = self.vouchers[id(voucher)]['file_path']

        old_voucher_status = None
        for stat in VoucherStatus: # Search for the voucher and remember its status
            voucher_list = user_profile.person.voucherlist[stat.value]
            if voucher in voucher_list:
                old_voucher_status = stat.value
                break  # Voucher found, exit the loop

        if old_voucher_status != voucher_status:  # if new status -> Move voucher to new list
            if old_voucher_status: # if no old status (voucher creation) do nothing
                user_profile.person.voucherlist[old_voucher_status].remove(voucher)
            user_profile.person.voucherlist[voucher_status].append(voucher)

        self.vouchers[id(voucher)]['file_path'] = new_full_file_path
        self.vouchers[id(voucher)]['local_vid'] = local_id
        self._secure_file_handler.encrypt_and_save(voucher, voucher_name, key=self.file_enc_key.encode('utf-8'), subfolder=file_path)

        # todo improve and do check of new file before deletion of old file

        # delete old file
        if old_path:
            self._secure_file_handler.delete_file(old_path)

    def send_minuto(self, amount, recipient_id):
        # creates a transaction and returns an encrypted transaction file

        transaction = self.person.send_amount(amount, recipient_id)
        if not transaction.transaction_successful:
            return transaction # return failed transaction

        # save changed vouchers in transaktion to disk
        for voucher in transaction.transaction_vouchers:
            self.save_voucher_to_disk(voucher)


        # todo save transaction backup to disk (to send again, store file again for sending)
        # todo gui with transaction list
        return transaction

    def create_new_profile(self, profile_name, first_name, last_name, organization, seed, profile_password):
        # storekey and salt in object for saving to disk
        seed = " ".join(str(seed).lower().split())  # remove multiple white spaces, lower case
        self.encryption_key, self.encryption_salt = generate_symmetric_key(profile_password, b64_string=True)
        # todo test if files can be decrypted after profile recovery oder password recovery
        # derive deterministic key from seed to ensure decryption of files after profile recovery
        self.file_enc_key, _ = generate_symmetric_key(seed, salt=hash_bytes(seed), b64_string=True)
        # when password lost, seed is second password for recovery
        self.encrypted_seed_words = symmetric_encrypt(seed, second_password=seed, key=self.encryption_key.encode('utf-8'), salt=b64d(self.encryption_salt))
        self.profile_name = profile_name
        self.person_data['first_name'] = first_name
        self.person_data['last_name'] = last_name
        self.person_data['organization'] = organization
        self.person = Person(self.person_data,seed=seed)
        self._secure_file_handler = SecureFileHandler()
        self.save_profile_to_disk(second_password=seed)
        self._profile_initialized = True

    def recover_password_with_seed(self,seed, new_password):
        seed = " ".join(str(seed).lower().split()) # remove multiple white spaces, lower case
        if not self.load_profile_from_disk(seed):
            return False

        self.encryption_key, self.encryption_salt = generate_symmetric_key(new_password, b64_string=True)
        # when password lost, seed is second password for recovery
        self.encrypted_seed_words = symmetric_encrypt(seed, second_password=seed,
                                                      key=self.encryption_key.encode('utf-8'),
                                                      salt=b64d(self.encryption_salt))
        self.person = Person(self.person_data, seed=seed)
        self._secure_file_handler = SecureFileHandler(self.person.key.private_key, self.person.id)
        self.save_profile_to_disk(second_password=seed)
        return True

    def save_profile_to_disk(self, password="", second_password=None):
        # always use seed as recovery_password (needed when password is lost)
        if second_password == None:
            recovery_password = symmetric_decrypt(self.encrypted_seed_words, key=self.encryption_key.encode('utf-8'))
        else:
            recovery_password = second_password
        file_path = join_path(self.data_folder, self.profile_filename)
        self._secure_file_handler.encrypt_and_save(self, file_path, password=password, second_password=recovery_password, key=self.encryption_key.encode('utf-8'), salt=b64d(self.encryption_salt))

    def profile_logout(self):
        self.save_profile_to_disk()
        self.initialize_state()

    def load_profile_from_disk(self, password):
        filehandler = SecureFileHandler()
        try:
            loaded_profile = filehandler.decrypt_and_load(join_path(self.data_folder, self.profile_filename), password, UserProfile)
            self.__dict__.update(loaded_profile.__dict__)
            self._profile_initialized = True
            return True
        except Exception: # Exception when password is wrong
            return False

    def create_voucher(self, first_name, last_name, organization, address, gender, email, phone, service_offer, coordinates, amount, region, years_valid, is_test_voucher, description='', footnote=''):
        self.person.create_voucher_from_gui(first_name, last_name, organization, address, gender, email, phone, service_offer, coordinates, amount, region, years_valid, is_test_voucher, description, footnote)

        local_id, _ = self.person.current_voucher.get_local_voucher_id(self.person.id)
        # add to voucher management list
        self.vouchers[id(self.person.current_voucher)] = {'local_vid': local_id, 'file_path': None,
                                                          'trashed': False}
        self.save_voucher_to_disk(self.person.current_voucher) # saves file and add it to voucherlist
        voucher = self.person.current_voucher
        self.person.current_voucher = None
        return voucher

    def to_dict(self):
        """
        Converts the attributes of the class into a dictionary. This method is essential for saving to disk.
        """
        # Exclude non-serializable attributes
        exclude = ['person','vouchers']
        return {key: value for key, value in self.__dict__.items()
                if not key.startswith('_') and key not in exclude}

    def get_minuto_balance(self,type):
        # calculate total balances for gui
        if not self._profile_initialized:
            return "0,00"
        if type == VoucherStatus.OWN.value:
            value = 0
            for v in self.person.voucherlist[VoucherStatus.OWN.value]:
                value += v.get_voucher_amount(self.person.id)
            return display_balance(value)

        if type == VoucherStatus.OTHER.value:
            value = 0
            for v in self.person.voucherlist[VoucherStatus.OTHER.value]:
                value += v.get_voucher_amount(self.person.id)
            return display_balance(value)



    def profile_exists(self):
        return file_exists(self.data_folder, self.profile_filename)

    def profile_initialized(self):
        return self._profile_initialized

# Instantiate the UserProfile
user_profile = UserProfile()

