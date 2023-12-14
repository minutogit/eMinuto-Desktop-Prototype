# screenmanager.py
from src.services.crypto_utils import generate_seed
from src.services.utils import is_password_valid, file_exists
from src.models.user_profile import UserProfile
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.color_definitions import colors


user_profile = UserProfile()
Builder.load_file('gui/gui_layout.kv')

# Definiere die verschiedenen Bildschirme
class NoProfileStartupScreen(Screen):
    pass

class DashboardScreen(Screen):
    # propertys for automatic update of values
    title = StringProperty('')
    balance_other_vouchers = StringProperty('')
    balance_own_vouchers = StringProperty('')

    def on_enter(self):
        self.title = self.get_title()
        self.balance_other_vouchers = str(self.get_balance_other_vouchers())
        self.balance_own_vouchers = str(self.get_balance_own_vouchers())

    def __init__(self, **kw):
        super().__init__(**kw)

    def get_title(self):
        name = user_profile.person_data['first_name']
        surname = user_profile.person_data['last_name']
        return f"{name} {surname}"

    def get_balance_other_vouchers(self):
        return "123.45"

    def get_balance_own_vouchers(self):
        return "500.00"


class ProfileLoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def load_existing_profile(self, password):
        return user_profile.init_existing_profile(password)


class GenerateNewUserProfileScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.on_enter = self.init_seed

    def init_seed(self):
        self.generate_seed()

    def generate_seed(self):
        seed = generate_seed()
        self.ids.seed_field.text = seed

    def is_password_valid(self,password):
        return is_password_valid(password)

    def generate_new_user_profile(self, first_name, last_name, organization, seed, profile_password):
        print(f"generate_new_user_profile\nseed: -{seed}-\npassword: -{profile_password}-")
        user_profile.create_new_profile(first_name, last_name, organization, seed, profile_password)




# Hauptanwendung
from kivymd.app import MDApp
class MyApp(MDApp):
    def build(self, first=False):
        # Erstelle den Screen Manager
        sm = ScreenManager()

        sm.add_widget(DashboardScreen(name='dashboard'))

        if user_profile.profile_exists():
            sm.add_widget(ProfileLoginScreen(name='profile_login'))
            sm.current = 'profile_login'
        else:
            sm.add_widget(NoProfileStartupScreen(name='no_profile_startup'))
            sm.add_widget(GenerateNewUserProfileScreen(name='generate_new_user_profile'))
            sm.current = 'no_profile_startup'

        return sm

if __name__ == '__main__':
    MyApp().run()
