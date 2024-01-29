# user_profile.py
from src.services.utils import convert_json_string_to_dict, file_exists, join_path, Serializable, read_file_content, \
    is_valid_object, dprint
from src.services.crypto_utils import generate_symmetric_key, symmetric_encrypt, symmetric_decrypt, b64d, is_encrypted_string, hash_bytes
from src.models.secure_file_handler import SecureFileHandler
from src.models.person import Person
from src.models.minuto_voucher import is_voucher_dict, VoucherStatus

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
                    self.open_voucher(full_file_path)

    def open_file(self, file_path):
        # open and reads vouchers, signatures or transactions from user interaction in gui
        return_info = ""
        file_content = read_file_content(file_path)
        if is_encrypted_string(file_content):

            try:
                # first try to encrypt received files from other users with shared secret
                file_content = self._secure_file_handler.decrypt_with_shared_secret_and_load(file_path)
            except:
                try:
                    # if decryption from other user fails, try to decrypt with own file key
                    file_content = symmetric_decrypt(file_content, key=self.file_enc_key)
                except:
                    print("decryption fails")
                    return None, "Entschlüsselung fehlgeschlagen"

        if is_valid_object(file_content):
            # if string then convert to dict
            if isinstance(file_content, str):
                file_content = convert_json_string_to_dict(file_content)

            # check if voucher
            if is_voucher_dict(file_content):
                self.person.read_voucher_from_dict(file_content)
                # todo avoid adding duplicates - add func in person to check if voucher already loaded
                voucher_status = self.person.current_voucher.voucher_status(self.person.id)
                dprint(voucher_status)
                self.person.voucherlist[voucher_status.value].append(self.person.current_voucher)
                voucher_amount = self.person.current_voucher.get_voucher_amount(self.person.id)

                if voucher_status in [VoucherStatus.OWN, VoucherStatus.OTHER]:
                    return_info = f"Gutschein mit {voucher_amount}M Guthaben hinzugefügt."
                elif voucher_status == VoucherStatus.USED:
                    return_info = "Gutschein hat kein Guthaben."
                elif voucher_status == VoucherStatus.UNFINISHED:
                    return_info = "Unfertigen Gutschein hinzugefügt."

                self.save_file(self.person.current_voucher)

            # check if guarantor signature
            elif isinstance(file_content, list) and isinstance(file_content[0], dict) and "signature_time" in \
                    file_content[0]:
                # try to find voucher and add guarantor signature
                self.person.current_voucher, return_info = self.person.add_received_signature_to_unfinished_voucher(file_content)
                # save updated voucher to disk
                if self.person.current_voucher is not None:
                    self.save_file(self.person.current_voucher)
            else:
                return_info = "unbekanntes Format"

        else:
            return_info = "Ungültige Datei"

        voucher = self.person.current_voucher
        self.person.current_voucher = None
        return voucher ,return_info


    def open_voucher(self,file_path):
        # open and reads vouchers on startup
        # todo for later: Check if a new voucher has already been sent to reduce the possibility of double spending when users make mistakes.
        file_content = read_file_content(file_path)
        if is_encrypted_string(file_content):
            try:
                file_content = symmetric_decrypt(file_content, key=self.file_enc_key)
            except:
                print(f"local voucher decryption failed. ")

        if is_valid_object(file_content):
            # if string then convert to dict
            if isinstance(file_content, str):
                file_content = convert_json_string_to_dict(file_content)

            # check if voucher format
            if is_voucher_dict(file_content):
                # todo check if not the correct file name format (save new file with correct name and delete old file)
                # todo just check and save the voucher again (an let the save function do correct the file name)
                # todo check if voucher already loaded (add list off all loaded local_voucher_ids) or new version (use old_local_ids) loaded
                self.person.read_voucher_from_dict(file_content)
                self.person.current_voucher._file_path = str(file_path) # store current file location
                local_id, old_local_ids = self.person.current_voucher.get_local_voucher_id(self.person.id)
                self.person.current_voucher._local_voucher_id = local_id # store local_id
                voucher_status = self.person.current_voucher.voucher_status(self.person.id)
                self.person.voucherlist[voucher_status.value].append(self.person.current_voucher)
                self.person.current_voucher = None


    def save_file(self, voucher, encrypted=True):
        # save vouher to disk
        voucher_stored_on_disk = (voucher._file_path is not None)
        #dprint("voucher_stored_on_disk", voucher_stored_on_disk)
        local_id, old_local_ids = voucher.get_local_voucher_id(self.person.id)
        voucher_status = voucher.voucher_status(self.person.id)
        import os

        file_path = os.path.join(self.data_folder, voucher_status.value)
        voucher_name = f"eMinuto-{local_id}.mv"
        new_full_file_path = str(os.path.join(self.data_folder, voucher_status.value, voucher_name))
        old_path = None
        if voucher_stored_on_disk and voucher._file_path != new_full_file_path:
            dprint(f"voucher hat neuen pfad/namen {voucher._file_path} -> {new_full_file_path}")
            old_path = voucher._file_path

        voucher._file_path = new_full_file_path
        voucher._local_voucher_id = local_id
        #os.makedirs(file_path, exist_ok=True)
        self._secure_file_handler.encrypt_and_save(voucher, voucher_name, key=self.file_enc_key.encode('utf-8'), subfolder=file_path)

        # todo improve and do chek of new file before deletion of old file

        # delete old file
        if old_path:
            self._secure_file_handler.delete_file(old_path)


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
        self.save_file(self.person.current_voucher)
        self.person.voucherlist[VoucherStatus.UNFINISHED.value].append(self.person.current_voucher)
        voucher = self.person.current_voucher
        self.person.current_voucher = None
        return voucher

    def to_dict(self):
        """
        Converts the attributes of the class into a dictionary. This method is essential for saving to disk.
        """
        # Exclude non-serializable attributes
        exclude = ['person']
        return {key: value for key, value in self.__dict__.items()
                if not key.startswith('_') and key not in exclude}

    def get_own_minuto_balance(self):
        if not self._profile_initialized:
            return "0,00"

        return "123,00" # todo

    def get_other_minuto_balance(self):
        if not self._profile_initialized:
            return "0,00"

        return "123,00" # todo


    def profile_exists(self):
        return file_exists(self.data_folder, self.profile_filename)

    def profile_initialized(self):
        return self._profile_initialized

# Instantiate the UserProfile
user_profile = UserProfile()

