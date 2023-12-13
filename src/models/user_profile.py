# user_profile.py
from src.services.utils import file_exists

class UserProfile:
    def __init__(self):
        # A dictionary to store all personal data
        self.person_data = {
            'name': None,
            'address': None,
            'gender': None,
            'email': None,
            'phone': None,
            'service_offer': None,
            'coordinates': None,
            'seed': None
        }

        # Additional attributes of UserProfile
        self.balance = 0
        self.transaction_pin = None
        self.seed_words = None
        self.data_folder = 'mdata' # static folder for app
        self.profile_filename = 'userprofile.dat'

    @staticmethod
    def check_file_exists(data_folder, profile_filename):
        return file_exists(data_folder, profile_filename)



