# screenmanager.py
from src.services.crypto_utils import generate_seed
from src.services.utils import is_password_valid, file_exists
from src.models.user_profile import UserProfile
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


# for hot reload
from kivymd.app import MDApp
#from kivymd.tools.hotreload.app import MDApp


Builder.load_file('gui/gui_layout.kv')

# Definiere die verschiedenen Bildschirme
class NoProfileStartupScreen(Screen):
    pass

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

    def generate_new_user_profile(self, seed, profile_password):
        print(f"generate_new_user_profile\nseed: -{seed}-\npassword: -{profile_password}-")
        pass



# Hauptanwendung
class MyApp(MDApp):
    #DEBUG = 1 # activate hot reload
    #KV_FILES = ["gui/gui_layout.kv"]
    def build(self, first=False):
        self.theme_cls.primary_palette = "Blue"  # Setze das Farbschema

        # Erstelle den Screen Manager
        sm = ScreenManager()

        sm.add_widget(NoProfileStartupScreen(name='no_profile_startup'))
        sm.add_widget(GenerateNewUserProfileScreen(name='generate_new_user_profile'))

        sm.current = 'no_profile_startup'
        return sm

if __name__ == '__main__':
    MyApp().run()
