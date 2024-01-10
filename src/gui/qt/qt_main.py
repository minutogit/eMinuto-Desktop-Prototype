# qt_main.py
from PySide6.QtWidgets import QApplication, QMainWindow, \
    QMessageBox, QLineEdit
from PySide6 import QtSql
from src.services.crypto_utils import generate_seed
from src.services.utils import is_password_valid
from src.models.user_profile import user_profile


from src.gui.qt.ui_components.main_window import Ui_MainWindow
from src.gui.qt.ui_components.dialog_generate_profile import Ui_DialogGenerateProfile
#afrom ui_components.dialog_new_password import Ui_DialogNewPassword
from src.gui.qt.ui_components.dialog_enter_password import Ui_DialogEnterPassword
from src.gui.qt.ui_components.dialog_profile_create_selection import Ui_Dialog_Profile_Create_Selection
from src.gui.qt.ui_components.dialog_profile import Ui_Form_Profile


def show_message_box(title, text):
    dlg = QMessageBox()
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.exec()

def apply_global_styles(app):
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f2f2f2; 
        }
        QLineEdit, QTextBrowser, QTextEdit {
            background-color: white;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 5px;
            selection-background-color: #1abc9c;
            color: #34495e;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #3498db; 
        }
        
    """)




class Dialog_Enter_Password(QMainWindow, Ui_DialogEnterPassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.wrong_passwort_counter = 0
        self.pushButton_OK.clicked.connect(self.check_password)
        #self.lineEdit_entered_password.returnPressed.connect(self.check_password)
        self.change_existing_password = False
        self.show_seed_words = False

    def check_password(self):
        password = self.lineEdit_entered_password.text()
        if not user_profile.init_existing_profile(password):
            show_message_box("Falsches Passwort!", "Falsches Passwort eingegeben!")
            self.lineEdit_entered_password.setText("")
            return
        frm_main_window.update_values()
        self.close()



class Dialog_Profile(QMainWindow, Ui_Form_Profile):
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
        self.lineEdit_address.setText(user_profile.person_data['address'])
        self.lineEdit_email.setText(user_profile.person_data['email'])
        self.lineEdit_phone.setText(user_profile.person_data['phone'])
        self.textEdit_service_offer.setText(user_profile.person_data['service_offer'])
        self.lineEdit_coordinates.setText(user_profile.person_data['coordinates'])
        self.show()

    def save_profile(self):
        user_profile.profile_name = self.lineEdit_profile_name.text()
        user_profile.person_data['first_name'] = self.lineEdit_first_name.text()
        user_profile.person_data['last_name'] = self.lineEdit_last_name.text()
        user_profile.person_data['organization'] = self.lineEdit_organization.text()
        user_profile.person_data['address'] = self.lineEdit_address.text()
        user_profile.person_data['email'] = self.lineEdit_email.text()
        user_profile.person_data['phone'] = self.lineEdit_phone.text()
        user_profile.person_data['service_offer'] = self.textEdit_service_offer.toPlainText()
        user_profile.person_data['coordinates'] = self.lineEdit_coordinates.text()
        frm_main_window.update_values()
        user_profile.save_profile_to_disk()




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
        self.lineEdit_new_seed.setText(generate_seed())
        self.btn_new_seed_words.clicked.connect(self.generate_new_word_seed)
        self.btn_create_profile.clicked.connect(self.create_profile)

    def generate_new_word_seed(self):
        self.lineEdit_new_seed.setText(generate_seed())
        #pass

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
        if not is_password_valid(password):
            show_message_box("Fehler!", "Passwort muss mindestens 8 Zeichen haben.")
            return

        user_profile.create_new_profile(profile_name, first_name, last_name, organization, seed, password)
        frm_main_window.update_values()

        self.close()


class Frm_Mainwin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"eMinuto")
        self.actionProfile.triggered.connect(dialog_profile.init_and_show)  # menu
        self.actionClose.triggered.connect(self.close)

    def update_values(self):
        self.setWindowTitle(f"eMinuto - Profil: {user_profile.profile_name}")
        self.label_username.setText(f"{user_profile.person_data['first_name']} {user_profile.person_data['last_name']}")
        self.lineEdit_own_balance.setText(self.get_balance_own_vouchers())
        self.lineEdit_other_balance.setText(self.get_balance_other_vouchers())

    def on_enter(self):
        """Update the screen when entering."""
        self.title = self.get_title()
        self.balance_other_vouchers = str(self.get_balance_other_vouchers())
        self.balance_own_vouchers = str(self.get_balance_own_vouchers())

    def get_title(self):
        """Get the user's full name for the title."""
        name = user_profile.person_data['first_name']
        surname = user_profile.person_data['last_name']
        return f"{name} {surname}"

    def get_balance_other_vouchers(self):
        """Demo function to get balance of other vouchers."""
        return "123.45"

    def get_balance_own_vouchers(self):
        """Demo function to get balance of own vouchers."""
        return "500.00"


#
app = QApplication([])
apply_global_styles(app)

dialog_generate_profile = Dialog_Generate_Profile()
dialog_enter_password = Dialog_Enter_Password()
dialog_profile_create_selection = Dialog_Profile_Create_Selection()
dialog_profile = Dialog_Profile()


frm_main_window = Frm_Mainwin()

#
#
# db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
#
# frm_main_window = Frm_Mainwin()
# frm_main_window.show()
# #frm_main_window.profile_login()
#
# app.exec()

