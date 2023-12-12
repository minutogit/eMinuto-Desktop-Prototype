# screenmanager.py
from src.services.crypto_utils import generate_seed
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


# for hot reload
from kivymd.app import MDApp
#from kivymd.tools.hotreload.app import MDApp


Builder.load_file('gui/gui_layout.kv')

# Definiere die verschiedenen Bildschirme
class NoProfileStartupScreen(Screen):
    pass

class GenerateNewUserIdScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.on_enter = self.init_seed

    def init_seed(self):
        self.generate_seed()

    def generate_seed(self):
        seed = generate_seed()
        self.ids.seed_field.text = seed



# Hauptanwendung
class MyApp(MDApp):
    #DEBUG = 1 # activate hot reload
    #KV_FILES = ["gui/gui_layout.kv"]
    def build(self, first=False):
        self.theme_cls.primary_palette = "Blue"  # Setze das Farbschema

        # Erstelle den Screen Manager
        sm = ScreenManager()

        sm.add_widget(NoProfileStartupScreen(name='no_profile_startup'))
        sm.add_widget(GenerateNewUserIdScreen(name='generate_new_user_id'))

        sm.current = 'no_profile_startup'
        print(generate_seed())
        return sm

if __name__ == '__main__':
    MyApp().run()
