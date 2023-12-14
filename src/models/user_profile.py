# user_profile.py
from src.services.utils import file_exists, join_path, Serializable
from src.services.crypto_utils import generate_symmetric_key, symmetric_encrypt, symmetric_decrypt
from src.models.SecureFileHandler import SecureFileHandler
from src.models.person import Person

class UserProfile(Serializable):
    def __init__(self):
        # A dictionary to store all personal data
        self.person_data = {
            'first_name': None,
            'last_name': None,
            'organization': None,
            'address': None,
            'gender': 0,
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
        self.person = None # _ to exclude storage on disk

    def init_existing_profile(self,password):
        if not self.load_profile_from_disk(password):
            return False
        seed = symmetric_decrypt(self.encrypted_seed_words, password)
        self.person = Person(
            f"{self.person_data['first_name']} {self.person_data['last_name']}",
            self.person_data['address'],
            self.person_data['gender'],
            self.person_data['email'],
            self.person_data['phone'],
            self.person_data['service_offer'],
            self.person_data['coordinates'],
            seed=seed
        )
        return True

    def create_new_profile(self, first_name, last_name, organization, seed, profile_password):
        key, salt = generate_symmetric_key(profile_password)
        self.encrypted_seed_words = symmetric_encrypt(seed, key=key, salt=salt)
        self.person_data['first_name'] = first_name
        self.person_data['last_name'] = last_name
        self.person_data['organization'] = organization
        self.person = Person(
            f"{self.person_data['first_name']} {self.person_data['last_name']}",
            "",
            self.person_data['gender'],
            "",
            "",
            "",
            "",
            seed=seed
        )
        self.save_profile_to_disk(profile_password)

    def save_profile_to_disk(self, password):
        filehandler = SecureFileHandler()
        filehandler.encrypt_and_save(self, password, join_path(self.data_folder, self.profile_filename))

    def load_profile_from_disk(self, password):
        filehandler = SecureFileHandler()
        try:
            loaded_profile = filehandler.decrypt_and_load(join_path(self.data_folder, self.profile_filename), password, UserProfile)
            self.__dict__.update(loaded_profile.__dict__)
            return True
        except Exception: # Exception when password is wrong
            return False

    def to_dict(self):
        """
        Converts the attributes of the class into a dictionary. This method is essential for saving to disk.
        """
        # Exclude non-serializable attributes
        exclude = ['person']
        return {key: value for key, value in self.__dict__.items()
                if not key.startswith('_') and key not in exclude}

    def profile_exists(self):
        return file_exists(self.data_folder, self.profile_filename)



