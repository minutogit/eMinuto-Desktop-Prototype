# qt_main.py
from PySide6.QtWidgets import QApplication, QMainWindow, \
    QMessageBox, QLineEdit

from PySide6 import QtSql
from src.services.crypto_utils import generate_seed
from src.services.utils import is_password_valid
from src.models.user_profile import user_profile


from PySide6.QtGui import QTextDocument, QAction
from PySide6.QtWidgets import QMainWindow, QMenu, QHeaderView
from PySide6.QtCore import QSortFilterProxyModel, Qt



from src.gui.qt.ui_components.main_window import Ui_MainWindow
from src.gui.qt.ui_components.dialog_generate_profile import Ui_DialogGenerateProfile
from src.gui.qt.ui_components.dialog_profile_login import Ui_DialogProfileLogin
from src.gui.qt.ui_components.dialog_profile_create_selection import Ui_Dialog_Profile_Create_Selection
from src.gui.qt.ui_components.dialog_profile import Ui_Form_Profile
from src.gui.qt.ui_components.dialog_create_minuto import Ui_DialogCreateMinuto
from src.gui.qt.ui_components.dialog_voucher_list import Ui_DialogVoucherList
from src.gui.qt.ui_components.form_show_voucher import Ui_FormShowVoucher
from src.gui.qt.ui_components.form_show_raw_data import Ui_FormShowRawData



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


from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QAbstractItemView

class FormShowRawData(QMainWindow, Ui_FormShowRawData):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_Close.clicked.connect(self.close)

    def show_data(self, object):
        import json
        # Convert the object's dictionary to a JSON-formatted string
        json_representation = json.dumps(object.__dict__, sort_keys=False, indent=4, ensure_ascii=False)
        self.textEdit_text_data.setText(json_representation)
        self.show()


class FormShowVoucher(QMainWindow, Ui_FormShowVoucher):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.voucher = None
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonRawData.clicked.connect(self.show_raw_data)

    def show_raw_data(self):
        form_show_raw_data.show_data(self.voucher)

    def show_voucher(self, voucher):
        self.voucher = voucher
        model = QStandardItemModel(self)
        model.setColumnCount(2)
        model.setHorizontalHeaderLabels(["Inhalt", "Wert"])

        # Set the model to the table and adjust table properties
        self.tableView_voucher.setModel(model)
        self.tableView_voucher.verticalHeader().setVisible(False)
        self.tableView_voucher.horizontalHeader().setVisible(True)
        self.tableView_voucher.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_voucher.setSelectionMode(QAbstractItemView.NoSelection)

        # Add voucher details as rows
        voucher_details = [
            ("Gutschein-ID", voucher.voucher_id),
            ("Ersteller-ID", voucher.creator_id),
            ("Vorname des Erstellers", voucher.creator_first_name),
            ("Nachname des Erstellers", voucher.creator_last_name),
            ("Organisation des Erstellers", voucher.creator_organization),
            ("Adresse des Erstellers", voucher.creator_address),
            ("Geschlecht des Erstellers", voucher.creator_gender),
            ("Betrag", voucher.amount),
            ("Beschreibung", voucher.description),
            ("Fußnote", voucher.footnote),
            ("Serviceangebot", voucher.service_offer),
            ("Gültig bis", voucher.validit_until),
            ("Region", voucher.region),
            ("Koordinaten", voucher.coordinates),
            ("E-Mail", voucher.email),
            ("Telefon", voucher.phone),
            ("Erstellungsdatum", voucher.creation_date),
            ("Ist Testgutschein", "Ja" if voucher.is_test_voucher else "Nein"),
            ("Garantenunterschriften", len(voucher.guarantor_signatures)),
            ("Unterschrift des Erstellers", "Unterschrieben" if voucher.creator_signature else "Nicht unterschrieben"),
            ("Transaktionen", len(voucher.transactions))
        ]

        for label, value in voucher_details:
            label_item = self.create_non_editable_item(label)
            value_item = self.create_non_editable_item(str(value))
            model.appendRow([label_item, value_item])

        self.tableView_voucher.setWordWrap(True)
        self.tableView_voucher.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableView_voucher.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.show()

    def create_non_editable_item(self, text):
        item = QStandardItem(str(text))
        item.setEditable(False)
        return item





class Dialog_Create_Minuto(QMainWindow, Ui_DialogCreateMinuto):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_amount.textChanged.connect(self.update_voucher_description)
        self.pushButton_CreateVoucher.clicked.connect(self.create_minuto)

    def create_minuto(self):
        # Extrahiere die Werte aus den GUI-Elementen
        amount = int(self.lineEdit_amount.text())
        region = self.lineEdit_region.text()
        years_valid = int(self.spinBox_years_valid.text())

        # Extrahiere Informationen aus anderen GUI-Elementen
        first_name = self.lineEdit_creator_first_name.text()
        last_name = self.lineEdit_creator_last_name.text()
        organization = self.lineEdit_creator_organization.text()
        address = self.lineEdit_creator_address.text()
        email = self.lineEdit_email.text()
        phone = self.lineEdit_phone.text()
        service_offer = self.textEdit_service_offer.toPlainText()
        coordinates = self.lineEdit_coordinates.text()
        is_test_vocher = self.checkBox_is_test_voucher.isChecked()

        # Geschlechtswert von QComboBox ermitteln
        gender = self.comboBox_creator_gender.currentIndex() # 0 unknown, 1 male, 2 female

        # Erstelle den Voucher
        user_profile.create_voucher(first_name, last_name, organization, address, gender, email, phone, service_offer,
                                    coordinates, amount, region, years_valid, is_test_vocher)

    def init_values(self):
        self.lineEdit_amount.setText("1000")
        self.update_voucher_description(self.lineEdit_amount.text())
        self.lineEdit_creator_organization.setText(user_profile.person_data['organization'])
        self.lineEdit_creator_first_name.setText(user_profile.person_data['first_name'])
        self.lineEdit_creator_last_name.setText(user_profile.person_data['last_name'])
        self.lineEdit_creator_address.setText(user_profile.person_data['address'])
        self.lineEdit_email.setText(user_profile.person_data['email'])
        self.lineEdit_phone.setText(user_profile.person_data['phone'])
        self.textEdit_service_offer.setText(user_profile.person_data['service_offer'])
        self.label_coordinates.setText(user_profile.person_data['coordinates'])

    def update_voucher_description(self, amount):
        """Update the voucher description based on the amount."""
        if amount:
            self.label_voucher_description.setText(
                f"Gutschein für Waren oder Dienstleistungen im Wert von {amount} Minuten qualitativer Leistung.")
        else:
            self.label_voucher_description.setText("Gutschein für Waren oder Dienstleistungen")

    def init_and_show(self):
        self.init_values()
        self.show()


class DialogVoucherList(QMainWindow, Ui_DialogVoucherList):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.all_vouchers = None
        self.headers = [
            "Gutschein-ID", "Ersteller", "Organisation", "Adresse", "Geschlecht",
            "Betrag", "Beschreibung", "Fußnote", "Dienstleistungsangebot",
            "Gültigkeit bis", "Region", "Koordinaten", "E-Mail", "Telefon",
            "Erstellungsdatum", "Testgutschein", "Garantenunterschriften",
            "Unterschrift des Erstellers", "Transaktionen"
        ]
        self.voucher_mapping = {}
        self.isTableViewConnected = False
        self.tableView_vouchers.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_vouchers.horizontalHeader().customContextMenuRequested.connect(self.openContextMenu)

    def init_show(self):
        self.init_values()
        self.show()

    def init_values(self):
        self.all_vouchers = user_profile.person.unfinished_vouchers

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(self.headers)

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(model)
        self.proxyModel.setDynamicSortFilter(True)
        self.tableView_vouchers.setModel(self.proxyModel)
        self.tableView_vouchers.setSortingEnabled(True)

        for i, voucher in enumerate(self.all_vouchers):
            self.add_voucher_to_model(model, voucher)
            self.voucher_mapping[i] = voucher

        self.tableView_vouchers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_vouchers.customContextMenuRequested.connect(self.openContextMenu)
        if not self.isTableViewConnected:
            self.tableView_vouchers.doubleClicked.connect(self.on_table_view_clicked)
            self.isTableViewConnected = True

    def add_voucher_to_model(self, model, voucher):
        gender_text = {0: "Unbekannt", 1: "Männlich", 2: "Weiblich"}.get(voucher.creator_gender, "Unbekannt")
        test_voucher_text = "Ja" if voucher.is_test_voucher else "Nein"
        creator_signature_text = "Ja" if voucher.creator_signature else "Nein"
        row = [
            self.create_non_editable_item(voucher.voucher_id),
            self.create_non_editable_item(f"{voucher.creator_first_name} {voucher.creator_last_name}"),
            self.create_non_editable_item(voucher.creator_organization),
            self.create_non_editable_item(voucher.creator_address),
            self.create_non_editable_item(gender_text),
            self.create_non_editable_item(str(voucher.amount)),
            self.create_non_editable_item(voucher.description),
            self.create_non_editable_item(voucher.footnote),
            self.create_non_editable_item(voucher.service_offer),
            self.create_non_editable_item(voucher.validit_until),
            self.create_non_editable_item(voucher.region),
            self.create_non_editable_item(voucher.coordinates),
            self.create_non_editable_item(voucher.email),
            self.create_non_editable_item(voucher.phone),
            self.create_non_editable_item(voucher.creation_date),
            self.create_non_editable_item(test_voucher_text),
            self.create_non_editable_item(str(len(voucher.guarantor_signatures))),
            self.create_non_editable_item(creator_signature_text),
            self.create_non_editable_item(str(len(voucher.transactions)))
        ]
        model.appendRow(row)

    def create_non_editable_item(self, text):
        item = QStandardItem(str(text))
        item.setEditable(False)
        return item

    def openContextMenu(self, position):
        menu = QMenu()
        for i, header in enumerate(self.headers):
            action = QAction(header, menu)
            action.setCheckable(True)
            action.setChecked(not self.tableView_vouchers.isColumnHidden(i))
            action.setData(i)
            action.toggled.connect(self.toggleColumnVisibility)
            menu.addAction(action)
        menu.exec_(self.tableView_vouchers.viewport().mapToGlobal(position))

    def toggleColumnVisibility(self, visible):
        column = self.sender().data()
        if visible:
            self.tableView_vouchers.showColumn(column)
        else:
            self.tableView_vouchers.hideColumn(column)

    def on_table_view_clicked(self, index):
        mapped_index = self.proxyModel.mapToSource(index)
        row = mapped_index.row()
        voucher = self.voucher_mapping[row]
        form_show_voucher.show_voucher(voucher)




class Dialog_Profile_Login(QMainWindow, Ui_DialogProfileLogin):
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
        frm_main_window.profile_login()
        self.close()

    def login(self):
        self.lineEdit_entered_password.setFocus()
        self.show()


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
        self.actionEditProfile.triggered.connect(dialog_profile.init_and_show)
        self.actionCreateMinuto.triggered.connect(dialog_create_minuto.init_and_show)
        self.actionProfileLogin.triggered.connect(dialog_profile_login.login)
        self.actionProfileLogout.triggered.connect(self.profile_logout)
        self.actionVoucherList.triggered.connect(dialog_voucher_list.init_show)

        self.actionClose.triggered.connect(self.close)
        self.set_gui_depending_profile_status()

    def update_values(self):
        self.setWindowTitle(f"eMinuto - Profil: {user_profile.profile_name}")
        self.label_username.setText(f"{user_profile.person_data['first_name']} {user_profile.person_data['last_name']}")
        self.lineEdit_own_balance.setText(user_profile.get_own_minuto_balance())
        self.lineEdit_other_balance.setText(user_profile.get_other_minuto_balance())


    def profile_login(self):
        self.update_values()
        self.set_gui_depending_profile_status()
        self.show_status_message("Erfolgreich eingeloggt.")

    def profile_logout(self):
        user_profile.profile_logout()
        self.update_values()
        self.set_gui_depending_profile_status()
        self.show_status_message("Erfolgreich ausgeloggt.")

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

    def set_gui_depending_profile_status(self):
        """changes the gui depending on whether the profile exists and is active or inactive."""

        profile_exists = user_profile.profile_exists()
        profile_initialized = user_profile.profile_initialized()

        profile_name = user_profile.profile_name
        window_title = f"eMinuto"


        def hide(object): #helper
            object.setVisible(False)

        def show(object):
            object.setVisible(True)

        def disable(object):
            object.setEnabled(False)

        def enable(object):
            object.setEnabled(True)


        #changings of GUI
        if profile_initialized:
            show(self.actionEditProfile)
            show(self.actionProfileLogout)
            show(self.actionCreateMinuto)
            show(self.actionVoucherList)
            enable(self.lineEdit_own_balance)
            enable(self.lineEdit_other_balance)

            hide(self.actionProfileLogin)
            hide(self.actionCreateProfile)


        if profile_exists and not profile_initialized:
            show(self.actionProfileLogin)

            hide(self.actionEditProfile)
            hide(self.actionProfileLogout)
            hide(self.actionCreateProfile)
            hide(self.actionCreateMinuto)
            hide(self.actionVoucherList)


            # disable(self.menuMinuto) does not work
            disable(self.lineEdit_own_balance)
            disable(self.lineEdit_other_balance)


        if not profile_exists:
            show(self.actionCreateProfile)

            hide(self.actionEditProfile)
            hide(self.actionProfileLogout)
            hide(self.actionProfileLogin)
            hide(self.actionCreateMinuto)
            hide(self.actionVoucherList)

            # disable(self.menuMinuto) does not work
            disable(self.lineEdit_own_balance)
            disable(self.lineEdit_other_balance)

    def show_status_message(self, message):
        self.statusBar().showMessage(message, 5000)  # 5 seconds timeout


#
app = QApplication([])
apply_global_styles(app)

form_show_raw_data = FormShowRawData()
dialog_generate_profile = Dialog_Generate_Profile()
dialog_profile_login = Dialog_Profile_Login()
dialog_profile_create_selection = Dialog_Profile_Create_Selection()
dialog_profile = Dialog_Profile()
dialog_create_minuto = Dialog_Create_Minuto()
dialog_voucher_list = DialogVoucherList()
form_show_voucher = FormShowVoucher()


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

