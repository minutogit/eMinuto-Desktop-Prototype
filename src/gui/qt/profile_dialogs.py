# profile_dialogs.py
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal


from src.gui.qt.ui_components.dialog_profile import Ui_Form_Profile
from src.gui.qt.ui_components.dialog_profile_create_selection import Ui_Dialog_Profile_Create_Selection
from src.gui.qt.ui_components.dialog_profile_login import Ui_DialogProfileLogin
from src.gui.qt.ui_components.dialog_generate_profile import Ui_DialogGenerateProfile
from src.gui.qt.utils import show_message_box
from src.models.user_profile import user_profile
from src.services.crypto_utils import generate_seed
from src.services.utils import is_password_valid
from src import config


class Dialog_Generate_Profile(QMainWindow, Ui_DialogGenerateProfile):
    profileCreated = Signal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.lineEdit_new_seed.setText(generate_seed())
        self.btn_new_seed_words.clicked.connect(self.generate_new_word_seed)
        self.btn_create_profile.clicked.connect(self.create_profile)

    def generate_new_word_seed(self):
        self.lineEdit_new_seed.setText(generate_seed())

    def create_profile(self):
        seed = self.lineEdit_new_seed_confirmed.text().strip()
        retyped_seed = self.lineEdit_new_seed_confirmed.text().strip()
        profile_name = self.lineEdit_profile_name.text().strip()
        password = self.lineEdit_password.text()
        password_confirmed = self.lineEdit_password_confirmed.text()
        organization = self.lineEdit_organization.text().strip()
        first_name = self.lineEdit_first_name.text().strip()
        last_name = self.lineEdit_last_name.text().strip()

        #check conditions
        if not seed == retyped_seed.strip():
            show_message_box("Fehler!", "Schlüsselwörter stimmen nicht überein. Bitte prüfen!")
            return
        if profile_name.replace(" ","") == "":
            show_message_box("Fehler!", "Bitte Profilnamen eingeben.")
            return
        if password != password_confirmed:
            show_message_box("Fehler!", "Passwörter stimmen nicht überein.")
            return
        if not is_password_valid(password) and not config.TEST_MODE:
            show_message_box("Fehler!", "Passwort muss mindestens 8 Zeichen haben.")
            return

        user_profile.create_new_profile(profile_name, first_name, last_name, organization, seed, password)
        self.profileCreated.emit() # emit signal
        self.close()

class Dialog_Profile_Login(QMainWindow, Ui_DialogProfileLogin):
    profileLogin = Signal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_OK.clicked.connect(self.check_password)
        self.lineEdit_entered_password.returnPressed.connect(self.check_password)

        self.lineEdit_entered_password.textChanged.connect(self.on_password_text_changed)

    def on_password_text_changed(self, text):
        # Setzt das Label nur zurück, wenn der Benutzer etwas eingibt
        if text:
            self.label_status.setText("")

    def check_password(self):
        password = self.lineEdit_entered_password.text()
        if not user_profile.init_existing_profile(password):
            self.label_status.setText("Passwort falsch")
            self.lineEdit_entered_password.clear()
            self.lineEdit_entered_password.setFocus()
            return
        self.lineEdit_entered_password.clear()
        #frm_main_window.profile_login()
        self.profileLogin.emit()  # emit signal
        self.close()

    def login(self):
        self.lineEdit_entered_password.setFocus()
        self.show()


class Dialog_Profile(QMainWindow, Ui_Form_Profile):
    frm_main_window_update_values = Signal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.save_profile)
        self.pushButton_close.clicked.connect(self.close)

    def init_and_show(self):
        self.lineEdit_profile_name.setText(user_profile.profile_name)
        self.lineEdit_first_name.setText(user_profile.person_data['first_name'])
        self.lineEdit_last_name.setText(user_profile.person_data['last_name'])
        self.lineEdit_organization.setText(user_profile.person_data['organization'])
        self.comboBox_gender.setCurrentIndex(user_profile.person_data['gender'])
        self.lineEdit_street.setText(user_profile.person_data['street'])
        self.lineEdit_zip_code.setText(user_profile.person_data['zip_code'])
        self.lineEdit_city.setText(user_profile.person_data['city'])
        self.lineEdit_state_or_region.setText(user_profile.person_data['state_or_region'])
        self.lineEdit_country.setText(user_profile.person_data['country'])
        self.lineEdit_email.setText(user_profile.person_data['email'])
        self.lineEdit_phone.setText(user_profile.person_data['phone'])
        self.textEdit_service_offer.setText(user_profile.person_data['service_offer'])
        self.lineEdit_coordinates.setText(user_profile.person_data['coordinates'])
        self.show()
        self.raise_()

    def save_profile(self):
        user_profile.profile_name = self.lineEdit_profile_name.text()
        user_profile.person_data['first_name'] = self.lineEdit_first_name.text()
        user_profile.person_data['last_name'] = self.lineEdit_last_name.text()
        user_profile.person_data['organization'] = self.lineEdit_organization.text()
        user_profile.person_data['street'] = self.lineEdit_street.text()
        user_profile.person_data['zip_code'] = self.lineEdit_zip_code.text()
        user_profile.person_data['city'] = self.lineEdit_city.text()
        user_profile.person_data['state_or_region'] = self.lineEdit_state_or_region.text()
        user_profile.person_data['country'] = self.lineEdit_country.text()
        user_profile.person_data['gender'] = self.comboBox_gender.currentIndex()
        user_profile.person_data['email'] = self.lineEdit_email.text()
        user_profile.person_data['phone'] = self.lineEdit_phone.text()
        user_profile.person_data['service_offer'] = self.textEdit_service_offer.toPlainText()
        user_profile.person_data['coordinates'] = self.lineEdit_coordinates.text()
        user_profile.person.set_person_data(user_profile.person_data)  # update person from person_data in profile
        #frm_main_window.update_values()
        self.frm_main_window_update_values.emit()
        user_profile.save_profile_to_disk()


class Dialog_Profile_Create_Selection(QMainWindow, Ui_Dialog_Profile_Create_Selection):
    frm_main_window_generate_profile = Signal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kein Profil gefunden")

        self.pushButton_create_new_profile.clicked.connect(self.generate_new_profile)
        self.pushButton_restore_exisitin_profile.clicked.connect(self.restore_profile)

    def generate_new_profile(self):
        self.close()
        #frm_main_window.dialog_generate_profile.show()
        self.frm_main_window_generate_profile.emit()

    def restore_profile(self):
        self.close()