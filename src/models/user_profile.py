# user_profile.py
from src.services.utils import file_exists, join_path, Serializable
from src.services.crypto_utils import generate_symmetric_key, symmetric_encrypt, symmetric_decrypt, b64d
from src.models.secure_file_handler import SecureFileHandler
from src.models.person import Person

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
            'country': 'Land',
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
        self.encryption_key = None
        self.encryption_salt = None
        self.data_folder = 'mdata'  # static folder for the app
        self.profile_filename = 'userprofile.dat'
        self.person = Person()
        self._profile_initialized = False

    def init_existing_profile(self,password):
        if not self.load_profile_from_disk(password):
            return False
        seed = symmetric_decrypt(self.encrypted_seed_words, password)
        self.person = Person(self.person_data, seed=seed)
        self.read_vouchers_from_disk()
        return True

    def read_vouchers_from_disk(self):
        unfinished_subfolder = "unfinished"
        import os
        file_path = os.path.join(self.data_folder, unfinished_subfolder)

        # List all files in the directory
        for filename in os.listdir(file_path):
            # Check if the file is a .txt file
            if filename.endswith('.txt'):
                self.person.read_voucher(filename,file_path)
                self.person.unfinished_vouchers.append(self.person.current_voucher)
                self.person.current_voucher = None


    def create_new_profile(self, profile_name, first_name, last_name, organization, seed, profile_password):
        # storekey and salt in object for saving to disk
        seed = " ".join(str(seed).lower().split())  # remove multiple white spaces, lower case
        self.encryption_key, self.encryption_salt = generate_symmetric_key(profile_password, b64_string=True)
        # when password lost, seed is second password for recovery
        self.encrypted_seed_words = symmetric_encrypt(seed, second_password=seed, key=self.encryption_key.encode('utf-8'), salt=b64d(self.encryption_salt))
        self.profile_name = profile_name
        self.person_data['first_name'] = first_name
        self.person_data['last_name'] = last_name
        self.person_data['organization'] = organization
        self.person = Person(self.person_data,seed=seed)
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
        filehandler = SecureFileHandler()
        # always use seed as recovery_password (needed when password is lost)
        if second_password == None:
            recovery_password = symmetric_decrypt(self.encrypted_seed_words, key=self.encryption_key.encode('utf-8'))
        else:
            recovery_password = second_password
        file_path = join_path(self.data_folder, self.profile_filename)
        filehandler.encrypt_and_save(self, file_path, password=password,  second_password=recovery_password,key=self.encryption_key.encode('utf-8'), salt=b64d(self.encryption_salt))

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

    def create_voucher(self, first_name, last_name, organization, address, gender, email, phone, service_offer, coordinates, amount, region, years_valid, is_test_voucher):
        unfinished_subfolder = "unfinished"
        self.person.create_voucher_from_gui(first_name, last_name, organization, address, gender, email, phone, service_offer, coordinates, amount, region, years_valid, is_test_voucher)
        file_path = join_path(self.data_folder, unfinished_subfolder)
        voucher_name = f"voucher-{self.person.current_voucher.creation_date}.txt"
        self.person.save_voucher(voucher_name, file_path)
        self.person.unfinished_vouchers.append(self.person.current_voucher)
        self.person.current_voucher = None


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

