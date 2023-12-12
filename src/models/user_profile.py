# user_profile.py

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
        self.data_folder = 'data'
        self.profile_filename = 'userprofile.dat'





