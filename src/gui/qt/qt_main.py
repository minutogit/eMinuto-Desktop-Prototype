# qt_main.py
from PySide6.QtWidgets import QApplication, QMainWindow, \
    QMessageBox
from PySide6 import QtSql

from src.gui.qt.ui_components.main_window import Ui_MainWindow
from src.gui.qt.ui_components.dialog_generate_profile import Ui_DialogGenerateProfile
#afrom ui_components.dialog_new_password import Ui_DialogNewPassword
from src.gui.qt.ui_components.dialog_enter_password import Ui_DialogEnterPassword


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
        self.pushButton_OK.clicked.connect(self.check_password)
        self.lineEdit_entered_password.returnPressed.connect(self.check_password)
        self.change_existing_password = False
        self.show_seed_words = False


class Dialog_Generate_Profile(QMainWindow, Ui_DialogGenerateProfile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.textBrowser_new_seed.setText(crypt.generate_word_seed())
        self.btn_new_seed_words.clicked.connect(self.generate_new_word_seed)
        self.btn_create_profile.clicked.connect(self.create_profile)

    def generate_new_word_seed(self):
        # seed = crypt.generate_word_seed(self)
        pass

    def create_profile(self):
        seed = self.textBrowser_new_seed.toPlainText()
        retyped_seed = self.textEdit_new_seed_confirmed.toPlainText()
        profile_name = str(self.lineEdit_profile_name.text())
        # ignore spaces when compare



class Frm_Mainwin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# app = QApplication()
#
#
# #dialog_generate_profile = Dialog_Generate_Profile()
# #dialog_enter_password = Dialog_Enter_Password()
#
#
# db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
#
# frm_main_window = Frm_Mainwin()
# frm_main_window.show()
# #frm_main_window.profile_login()
#
# app.exec()

