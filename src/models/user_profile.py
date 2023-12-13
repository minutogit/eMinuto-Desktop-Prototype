# user_profile.py
from src.services.utils import file_exists, join_path, Serializable
from src.services.crypto_utils import generate_symmetric_key, symmetric_encrypt, symmetric_decrypt
from src.models.SecureFileHandler import SecureFileHandler

class UserProfile(Serializable):
    def __init__(self):
        # A dictionary to store all personal data
        self.person_data = {
            'first_name': None,
            'last_name': None,
            'organization': None,
            'address': None,
            'gender': None,
            'email': None,
            'phone': None,
            'service_offer': None,
            'coordinates': None
        }

        # Additional attributes of UserProfile
        self.balance = 0
        self.transaction_pin = None
        self.encrypted_seed_words = None
        self.data_folder = 'mdata' # static folder for app
        self.profile_filename = 'userprofile.dat'
        self._person = None

    def create_new_profile(self, first_name, last_name, organization, seed, profile_password):
        key, salt = generate_symmetric_key(profile_password)
        self.encrypted_seed_words = symmetric_encrypt(seed, key=key, salt=salt)
        self.person_data['first_name'] = first_name
        self.person_data['last_name'] = last_name
        self.person_data['organization'] = organization
        self.save_profile_to_disk(profile_password)


    def save_profile_to_disk(self, password):
        filehandler = SecureFileHandler()
        filehandler.encrypt_and_save(self, password, join_path(self.data_folder, self.profile_filename))

    @staticmethod
    def check_file_exists(data_folder, profile_filename):
        return file_exists(data_folder, profile_filename)



