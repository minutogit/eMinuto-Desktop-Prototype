# profile_dialogs.py
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal

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

