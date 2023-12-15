# user_info_screen.py

from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from src.models.user_profile import user_profile

class UserInfoScreen(Screen):
    """Screen class for displaying and editing user information."""

    # Properties for each data field
    first_name = StringProperty('')
    last_name = StringProperty('')
    organization = StringProperty('')
    address = StringProperty('')
    gender = NumericProperty(0)  # Initialized as 0 (Unknown)
    email = StringProperty('')
    phone = StringProperty('')
    service_offer = StringProperty('')
    coordinates = StringProperty('')

    current_edit_property = StringProperty('')

    # Dialog for editing
    edit_dialog = None

    def show_edit_dialog(self, property_name, title):
        """Shows a dialog window for editing a property."""
        self.current_edit_property = property_name
        field_value = getattr(self, property_name)

        if property_name == 'service_offer':
            # Create MDTextField object
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
            self.service_offer_text_field = None  # Reset if not service_offer
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
        """Called when a gender is selected from the menu."""
        self.set_gender(value)
        self.gender_menu.dismiss()

    def show_gender_edit_dialog(self):
        """Displays a special dialog for selecting gender."""
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "Unbekannt", "on_release": lambda *args: self.select_gender('0')},
            {"viewclass": "OneLineListItem", "text": "Männlich", "on_release": lambda *args: self.select_gender('1')},
            {"viewclass": "OneLineListItem", "text": "Weiblich", "on_release": lambda *args: self.select_gender('2')},
        ]
        self.gender_menu = MDDropdownMenu(
            caller=self.ids.gender_item,
            items=menu_items,
            position="center",
            width_mult=4,
            max_height=3 * dp(48)  # Max height set to 48dp per item times 3 items
        )
        self.gender_menu.open()

    def set_gender(self, value):
        """Sets the gender based on selection and saves it."""
        self.gender = int(value)
        user_profile.person_data['gender'] = int(value)  # Save as a number
        self.gender_menu.dismiss()

    def close_dialog(self, *args):
        """Closes the dialog."""
        self.edit_dialog.dismiss()

    def save_data(self, *args):
        """Saves the new data and closes the dialog."""
        if self.current_edit_property == 'service_offer' and self.service_offer_text_field:
            new_value = self.service_offer_text_field.text
        else:
            new_value = self.edit_dialog.content_cls.text
        setattr(self, self.current_edit_property, new_value)
        user_profile.person_data[self.current_edit_property] = new_value

        # Additional steps to persist changes can be added here,
        # such as updating a database or writing to a file

        self.close_dialog()

    def on_enter(self):
        """Updates properties with data from user_profile.person_data on entering the screen."""
        super(UserInfoScreen, self).on_enter()
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
        """Temporarily sets the transition direction for this switch."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard'
        # Schedule resetting the transition direction after a short delay
        Clock.schedule_once(lambda dt: self.reset_transition_direction(), 0.5)

    def reset_transition_direction(self):
        """Resets the transition direction."""
        self.manager.transition.direction = 'left'
