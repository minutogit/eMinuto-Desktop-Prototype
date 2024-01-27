# user_profile.py
from src.services.utils import convert_json_string_to_dict, file_exists, join_path, Serializable, read_file_content, \
    is_valid_object, dprint
from src.services.crypto_utils import generate_symmetric_key, symmetric_encrypt, symmetric_decrypt, b64d, is_encrypted_string, hash_bytes
from src.models.secure_file_handler import SecureFileHandler
from src.models.person import Person
from src.models.minuto_voucher import is_voucher_dict

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
        voucher_types = [
            "unfinished",  # list of vouchers which not ready because of missing guarantor sign etc
            "used",  # List of used vouchers after transaction without amount
            "own",  # List of own created vouchers with ammount
            "other",  # List of vouchers from other users with amount
            "temp",  # temp vouchers
            "deleted",  # deleted vouchers (to keep until full deletion)
            "corrupt"  # vouchers where the verification fails (signature etc)
        ]
        import os # todo improve without import
        for folder in voucher_types: # folders named from voucher types
            folder_path = os.path.join(self.data_folder, folder)
            os.makedirs(folder_path, exist_ok=True)

            # List all files in the directory
            for filename in os.listdir(folder_path):
                # Check if the file is a .mv file
                if filename.endswith('.mv'):

                    full_file_path = os.path.join(folder_path, filename)
                    self.open_file(full_file_path, startup=True)

    # todo extra func to open vouchers on startup
    def open_file(self,file_path, startup=False):
        # open and reads vouchers, signatures or transactions from user interaction in gui
        return_info = ""
        file_content = read_file_content(file_path)
        if is_encrypted_string(file_content):
            if startup: # on startup load local encrypted vouchers
                try:
                    file_content = symmetric_decrypt(file_content, key=self.file_enc_key)
                except:
                    pass
            else:
                file_content = self._secure_file_handler.decrypt_with_shared_secret_and_load(file_path)

        if is_valid_object(file_content):
            # if string then convert to dict
            if isinstance(file_content, str):
                file_content = convert_json_string_to_dict(file_content)


            # check if voucher
            if is_voucher_dict(file_content):
                self.person.read_voucher_from_dict(file_content)
                # if valid and ready voucher
                if self.person.current_voucher.verify_complete_voucher():
                    voucher_amount = self.person.current_voucher.get_voucher_amount(self.person.id)
                    if voucher_amount > 0:
                        # todo some checks needed is voucher already added?
                        # dont add voucher with same id and same last transaction_id
                        # special case that user owns an voucher that had been send and the new voucher_is the the update version (longer transaction list)
                        # (the last transaction hash of current voucher, will be a prev_hast transaction / with my sender in transaction list)
                        # (in real world if the user would have been used this voucher again this would be a double spend, so this can helb to reduce double spending)
                        self.person.voucherlist["temp"].append(self.person.current_voucher)
                        return_info = f"Gutschein mit {voucher_amount}M Guthaben hinzugefügt."
                    else:
                        return_info = "Gutschein hat kein Guthaben."
                        pass
                        # todo check if also the same special case above (to reduce double spend posibility by user mistake)

                else:
                    self.person.voucherlist["unfinished"].append(self.person.current_voucher)
                    if not startup: # on startup file loaded from disk (dont save them again)
                        return_info = "Unfertigen Gutschein hinzugefügt."
                        unfinished_subfolder = "unfinished"
                        voucher_path = join_path(self.data_folder, unfinished_subfolder)
                        voucher_name = f"voucher-{self.person.current_voucher.creation_date}.txt".replace(':', '_')
                        self.person.save_voucher(voucher_name, voucher_path) # todo encrypted save




            # check if guarantor signature
            elif isinstance(file_content, list) and isinstance(file_content[0], dict) and "signature_time" in \
                    file_content[0]:
                # try to find voucher and add guarantor signature
                return_info = self.person.add_received_signature_to_unfinished_voucher(file_content)

            else:
                return_info = "unbekanntes Format"



        else:
            return_info = "Ungültige Datei"

        voucher = self.person.current_voucher
        self.person.current_voucher = None
        return voucher ,return_info


    def save_file(self, voucher, encrypted=True):
        # save vouher to disk
        name = voucher.get_voucher_name()
        voucher_status = voucher.voucher_status(self.person.id)
        import os
        file_path = os.path.join(self.data_folder, voucher_status)
        os.makedirs(file_path, exist_ok=True)
        self._secure_file_handler.encrypt_and_save(voucher, f"minuto-{name}.mv", key=self.file_enc_key.encode('utf-8'), subfolder=file_path)




    def create_new_profile(self, profile_name, first_name, last_name, organization, seed, profile_password):
        # storekey and salt in object for saving to disk
        seed = " ".join(str(seed).lower().split())  # remove multiple white spaces, lower case
        self.encryption_key, self.encryption_salt = generate_symmetric_key(profile_password, b64_string=True)
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
        unfinished_subfolder = "unfinished"
        self.person.create_voucher_from_gui(first_name, last_name, organization, address, gender, email, phone, service_offer, coordinates, amount, region, years_valid, is_test_voucher, description, footnote)
        #file_path = join_path(self.data_folder, unfinished_subfolder)
        #voucher_name = f"voucher-{self.person.current_voucher.creation_date}.txt".replace(':', '_')
        #self.person.save_voucher(voucher_name, file_path)
        self.save_file(self.person.current_voucher)
        self.person.voucherlist["unfinished"].append(self.person.current_voucher)
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

