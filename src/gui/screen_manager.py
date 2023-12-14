# screenmanager.py
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.menu import MDDropdownMenu

from src.services.crypto_utils import generate_seed
from src.services.utils import is_password_valid
from src.models.user_profile import UserProfile
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton


user_profile = UserProfile()
Builder.load_file('gui/gui_layout.kv')

# Definiere die verschiedenen Bildschirme
class NoProfileStartupScreen(Screen):
    pass


class UserInfoScreen(Screen):
    # Einzelne StringProperties für jedes Datenfeld
    first_name = StringProperty('')
    last_name = StringProperty('')
    organization = StringProperty('')
    address = StringProperty('')
    gender = NumericProperty(0)  # Initialisiert als 0 (Unbekannt)
    email = StringProperty('')
    phone = StringProperty('')
    service_offer = StringProperty('')
    coordinates = StringProperty('')

    # Aktuelle Eigenschaft, die bearbeitet wird
    current_edit_property = StringProperty('')

    # Dialog für die Bearbeitung
    edit_dialog = None

    def show_edit_dialog(self, property_name, title):
        """ Zeigt ein Dialogfenster zur Bearbeitung einer Eigenschaft an. """
        self.current_edit_property = property_name
        field_value = getattr(self, property_name)

        if property_name == 'service_offer':
            # Erstellen des MDTextField-Objekts
            self.service_offer_text_field = MDTextField(
                text=field_value,
                hint_text=title,
                multiline=True,
                size_hint_y=None,
                write_tab=False,
            )
            self.service_offer_text_field.bind(minimum_height=self.service_offer_text_field.setter('height'))

            content_cls = ScrollView(
                size_hint=(1, None),
                size=(dp(480), dp(120)),
                do_scroll_x=False
            )
            content_cls.add_widget(self.service_offer_text_field)
        else:
            self.service_offer_text_field = None  # Null setzen, wenn nicht im Dienstleistungsangebot
            content_cls = MDTextField(text=field_value, hint_text=title)

        self.edit_dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content_cls,
            buttons=[
                MDFlatButton(
                    text="Abbrechen",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="Speichern",
                    on_release=self.save_data
                ),
            ],
        )
        self.edit_dialog.open()

    def select_gender(self, value):
        """ Wird aufgerufen, wenn ein Geschlecht aus dem Menü ausgewählt wird. """
        self.set_gender(value)
        self.gender_menu.dismiss()

    def show_gender_edit_dialog(self):
        """ Zeigt einen speziellen Dialog zur Auswahl des Geschlechts. """
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Unbekannt",
                "on_release": lambda *args: self.select_gender('0')
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Männlich",
                "on_release": lambda *args: self.select_gender('1')
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Weiblich",
                "on_release": lambda *args: self.select_gender('2')
            },
        ]
        self.gender_menu = MDDropdownMenu(
            caller=self.ids.gender_item,
            items=menu_items,
            position="center",
            width_mult=4,
            max_height=3 * dp(48)  # Hier setzen Sie die maximale Höhe. 48dp pro Element mal 3 Elemente
        )
        self.gender_menu.open()

    def set_gender(self, value):
        """ Setzt das Geschlecht basierend auf der Auswahl und speichert es. """
        self.gender = int(value)
        user_profile.person_data['gender'] = int(value)  # Speichern als Zahl
        self.gender_menu.dismiss()

    def close_dialog(self, *args):
        """ Schließt den Dialog. """
        self.edit_dialog.dismiss()

    def save_data(self, *args):
        """ Speichert die neuen Daten und schließt den Dialog. """
        if self.current_edit_property == 'service_offer' and self.service_offer_text_field:
            new_value = self.service_offer_text_field.text
        else:
            new_value = self.edit_dialog.content_cls.text
        setattr(self, self.current_edit_property, new_value)
        user_profile.person_data[self.current_edit_property] = new_value

        # Hier können Sie zusätzliche Schritte hinzufügen, um die Änderungen dauerhaft zu speichern,
        # z.B. das Aktualisieren einer Datenbank oder das Schreiben in eine Datei

        self.close_dialog()

    def on_enter(self):
        super(UserInfoScreen, self).on_enter()
        # Aktualisieren Sie die StringProperties mit Daten aus user_profile.person_data
        self.first_name = user_profile.person_data.get('first_name', '')
        self.last_name = user_profile.person_data.get('last_name', '')
        self.organization = user_profile.person_data.get('organization', '')
        self.address = user_profile.person_data.get('address', '')
        self.gender = user_profile.person_data.get('gender', 0)
        self.email = user_profile.person_data.get('email', '')
        self.phone = user_profile.person_data.get('phone', '')
        self.service_offer = user_profile.person_data.get('service_offer', '')
        self.coordinates = user_profile.person_data.get('coordinates', '')

    def go_back_to_dashboard(self):
        # Setzt die Übergangsrichtung temporär für diesen Wechsel
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard'
        # Plant die Rücksetzung der Übergangsrichtung nach einer kurzen Verzögerung
        Clock.schedule_once(lambda dt: self.reset_transition_direction(), 0.5)

    def reset_transition_direction(self):
        # Setzt die Übergangsrichtung zurück
        self.manager.transition.direction = 'left'

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
        sm = ScreenManager(transition=SlideTransition(direction='left'))

        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(UserInfoScreen(name='user_info'))

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
