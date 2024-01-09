# qt_main.py
from PySide6.QtWidgets import QApplication, QMainWindow, \
    QMessageBox
from PySide6 import QtSql
from src.services.crypto_utils import generate_seed
from src.services.utils import is_password_valid
from src.models.user_profile import user_profile


from src.gui.qt.ui_components.main_window import Ui_MainWindow
from src.gui.qt.ui_components.dialog_generate_profile import Ui_DialogGenerateProfile
#afrom ui_components.dialog_new_password import Ui_DialogNewPassword
from src.gui.qt.ui_components.dialog_enter_password import Ui_DialogEnterPassword
from src.gui.qt.ui_components.dialog_profile_create_selection import Ui_Dialog_Profile_Create_Selection


def show_message_box(title, text):
    dlg = QMessageBox()
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.exec()


class Dialog_Enter_Password(QMainWindow, Ui_DialogEnterPassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.wrong_passwort_counter = 0
        #self.pushButton_OK.clicked.connect(self.check_password)
        #self.lineEdit_entered_password.returnPressed.connect(self.check_password)
        self.change_existing_password = False
        self.show_seed_words = False


class Dialog_Profile_Create_Selection(QMainWindow, Ui_Dialog_Profile_Create_Selection):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kein Profil gefunden")

        self.pushButton_create_new_profile.clicked.connect(self.generate_new_profile)
        self.pushButton_restore_exisitin_profile.clicked.connect(self.restore_profile)

    def generate_new_profile(self):
        self.close()
        dialog_generate_profile.show()

    def restore_profile(self):
        self.close()
        #dialog_restore_profile.restore_old_profile()
        pass

class Dialog_Generate_Profile(QMainWindow, Ui_DialogGenerateProfile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser_new_seed.setText(generate_seed())
        self.btn_new_seed_words.clicked.connect(self.generate_new_word_seed)
        self.btn_create_profile.clicked.connect(self.create_profile)

    def generate_new_word_seed(self):
        self.textBrowser_new_seed.setText(generate_seed())
        #pass

    def create_profile(self):
        seed = self.textBrowser_new_seed.toPlainText().strip()
        retyped_seed = self.textEdit_new_seed_confirmed.toPlainText().strip()
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
        if not is_password_valid(password):
            show_message_box("Fehler!", "Passwort muss mindestens 8 Zeichen haben.")

        user_profile.create_new_profile(first_name, last_name, organization, seed, password)
        self.close()


class Frm_Mainwin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# app = QApplication()
#
#
app = QApplication([])
dialog_generate_profile = Dialog_Generate_Profile()
dialog_enter_password = Dialog_Enter_Password()
dialog_profile_create_selection = Dialog_Profile_Create_Selection()

#
#
# db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
#
# frm_main_window = Frm_Mainwin()
# frm_main_window.show()
# #frm_main_window.profile_login()
#
# app.exec()

