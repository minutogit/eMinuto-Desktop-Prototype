# qt_main.py
from PySide6.QtCore import QSortFilterProxyModel, Qt, QSize
from PySide6.QtGui import QAction, QShowEvent, QIcon
from PySide6.QtWidgets import QApplication, QStatusBar, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtWidgets import QMainWindow, QMenu, QHeaderView

from src.gui.qt.profile_dialogs import Dialog_Generate_Profile
from src.gui.qt.ui_components.dialog_create_minuto import Ui_DialogCreateMinuto
from src.gui.qt.ui_components.dialog_profile import Ui_Form_Profile
from src.gui.qt.ui_components.dialog_profile_create_selection import Ui_Dialog_Profile_Create_Selection
from src.gui.qt.ui_components.dialog_profile_login import Ui_DialogProfileLogin
from src.gui.qt.ui_components.dialog_voucher_list import Ui_DialogVoucherList
from src.gui.qt.ui_components.form_show_raw_data import Ui_FormShowRawData
from src.gui.qt.ui_components.form_show_voucher import Ui_FormShowVoucher
from src.gui.qt.ui_components.main_window import Ui_MainWindow
from src.gui.qt.ui_components.form_send_to_guarantor import Ui_FormSendToGuarantor
from src.gui.qt.ui_components.form_sign_as_guarantor import Ui_FormSignVoucherAsGuarantor
from src.services.crypto_utils import verify_user_ID

from src.gui.qt.utils import apply_global_styles, show_message_box, show_yes_no_box
from src.models.user_profile import user_profile
from src.models.minuto_voucher import MinutoVoucher, VoucherStatus
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QAbstractItemView


def open_data_file():
    """
    Opens a file dialog to select a voucher or signature file and adds the voucher
    or signature to a voucher.
    """
    # Create a file dialog
    file_dialog = QFileDialog()

    # Set the accepted file extensions
    file_filter = "Voucher/Signature Files (*.mv *.ms);;All Files (*)"

    # Open the dialog and get the file path
    file_path, _ = file_dialog.getOpenFileName(None, "Open File", "", file_filter)

    if file_path:
        voucher, info_msg = user_profile.open_file(file_path)
        dialog_voucher_list.init_values()
        show_message_box("Info", info_msg)
        if voucher is not None:
            form_show_voucher.show_voucher(voucher)




class FormSignAsGuarantor(QMainWindow, Ui_FormSignVoucherAsGuarantor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.voucher = None
        self.guarantor_signature = None
        self.checkBox_liability_acceptance.stateChanged.connect(self.liability_acceptance)
        self.pushButton_sign_as_guarantor.clicked.connect(self.sign_as_guarantor)
        self.pushButton_save_as_file.clicked.connect(self.save_signature_as_file)

        self.apply_stylesheet_to_buttons()

    def apply_stylesheet_to_buttons(self):
        """ Apply custom stylesheet to buttons in the form. """
        button_stylesheet = """
                    QPushButton {
                        /* Stylesheet for normal button states */
                    }
                    QPushButton:disabled {
                        background-color: #d3d3d3;
                        color: #a0a0a0;
                    }
                """
        for button in self.findChildren(QPushButton):
            button.setStyleSheet(button_stylesheet)

    def liability_acceptance(self):
        # when checkbox for liability acceptance is checked / unchecked
        liability_accepted = self.checkBox_liability_acceptance.isChecked()
        self.pushButton_sign_as_guarantor.setEnabled(liability_accepted)

    def sign_as_guarantor(self):
        # if sign successful
        if user_profile.person.sign_voucher_as_guarantor(self.voucher):
            self.guarantor_signature = user_profile.person.get_own_guarantor_signature(self.voucher)
            self.checkBox_liability_acceptance.setEnabled(False)
            self.pushButton_sign_as_guarantor.setEnabled(False)
            self.pushButton_save_as_file.setEnabled(True)

    def save_signature_as_file(self):
        """
        Save the signature as a file, either encrypted or plain based on the user's choice.
        """

        creator_id = self.voucher.creator_id

        suggested_filename = f"Gutschein-Unterschrift_{user_profile.person.id[:4]}-{creator_id[:4]}.ms"
        file_filter = "Minuto Unterschrift (*.ms)"

        # Open file save dialog
        filename_with_path, _ = QFileDialog.getSaveFileName(
            self,
            "Unterschrift speichern",
            suggested_filename,
            file_filter
        )

         # Check if the user has entered a file name
        if filename_with_path:
            user_profile._secure_file_handler.encrypt_with_shared_secret_and_save(
                self.guarantor_signature, filename_with_path, creator_id, user_profile.person.id)



    def show_form(self, voucher):
        self.voucher = voucher
        self.guarantor_signature = None
        self.pushButton_sign_as_guarantor.setEnabled(False)
        self.pushButton_save_as_file.setEnabled(False)
        self.pushButton_send_as_email.setEnabled(False)
        self.checkBox_liability_acceptance.setChecked(False)
        self.show()



class FormSendToGuarantor(QMainWindow, Ui_FormSendToGuarantor):
    """
    A window form to send a voucher for signing to a guarantor or save the voucher as a file for obtaining a signature.
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.voucher = None
        self.pushButton_copy_user_ID.clicked.connect(self.copyUserIDToClipboard)
        self.pushButton_save_as_file.clicked.connect(self.save_voucher_as_file)
        self.lineEdit_guarantor_ID.textChanged.connect(self.check_guarantor_ID)

    def copyUserIDToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.lineEdit_user_ID.text())

    def check_guarantor_ID(self):
        """
        Check the entered guarantor ID and update the label with a green check or red cross based on validity.
        """
        guarantor_id = self.lineEdit_guarantor_ID.text().strip()
        if guarantor_id == "":
            self.label_guarantor_id_check.setText("")  # Clear label if input is empty
            return

        # Set label based on the validity of the guarantor ID
        if verify_user_ID(guarantor_id):
            if guarantor_id == user_profile.person.id:
                show_message_box("Fehler!", "Nicht die eigene ID verwenden!")
                return
            self.label_guarantor_id_check.setText("✅")  # Green check emoji for valid ID

        else:
            self.label_guarantor_id_check.setText("❌")  # Red cross emoji for invalid ID

    def save_voucher_as_file(self):
        """
        Save the voucher as a file, either encrypted or plain based on the user's choice.
        """

        # Set the suggested file name and extension based on encryption choice
        encrypt_data = self.checkBox_encrypt_voucher.isChecked()
        if verify_user_ID(self.lineEdit_guarantor_ID.text().strip()):
            guarantor_id = self.lineEdit_guarantor_ID.text().strip()
        elif encrypt_data:
            show_message_box("Fehler!", "Gültige ID des Bürgen wird für Verschlüsselung benötigt!")
            return

        suggested_filename = f"Gutschein-unfertig_{user_profile.person.id[:8]}.mv"
        file_filter = "Minuto Voucher (*.mv)"

        # Open file save dialog
        filename_with_path, _ = QFileDialog.getSaveFileName(
            self,
            "Voucher speichern",
            suggested_filename,
            file_filter
        )

        # Check if the user has entered a file name
        if filename_with_path:
            if encrypt_data:
                # Encrypt and save the voucher
                user_profile._secure_file_handler.encrypt_with_shared_secret_and_save(
                    self.voucher, filename_with_path, guarantor_id, user_profile.person.id)
            else:
                # Save the voucher unencrypted
                user_profile.person.save_voucher(filename=filename_with_path, voucher=self.voucher)


    def show_form(self, voucher):
        self.voucher = voucher
        self.lineEdit_user_ID.setText(user_profile.person.id)
        self.show()






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
    """
    FormShowVoucher class for displaying and managing voucher information.
    """

    def __init__(self):
        """ Initialize the FormShowVoucher window. """
        super().__init__()
        self.setupUi(self)
        self.voucher = None
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonRawData.clicked.connect(self.show_raw_data)
        self.pushButtonSignAsGuarantor.clicked.connect(self.sing_as_guarantor)
        self.pushButtonSendToGuarantor.clicked.connect(self.send_to_guarantor)
        self.pushButtonSignAsCreator.clicked.connect(self.sign_as_creator)

        self.apply_stylesheet_to_buttons()

    def apply_stylesheet_to_buttons(self):
        """ Apply custom stylesheet to buttons in the form. """
        button_stylesheet = """
                QPushButton {
                    /* Stylesheet for normal button states */
                }
                QPushButton:disabled {
                    background-color: #d3d3d3;
                    color: #a0a0a0;
                }
            """
        for button in self.findChildren(QPushButton):
            button.setStyleSheet(button_stylesheet)

    def sign_as_creator(self):
        sign = show_yes_no_box("Gutschein selbst unterschreiben", "Soll der Gutschein unterschrieben werden? Damit ist er gültig und kann für Transaktionen verwenden werden.")
        if sign:
            signed, message = user_profile.person.sign_voucher_as_creator(self.voucher)

            if signed:
                user_profile.save_file(self.voucher)
                user_profile.person.current_voucher = None
                show_message_box("Unterschrift erfolgreich", "Unterschrift war erfolgreich. Der Gutschein ist nun fertig und kann verwendet werden.")
                self.update_status(self.voucher)
            else:
                show_message_box("Fehler", f"Unterschrift fehlgeschlagen. {message}")


    def sing_as_guarantor(self):
        # check if gender is set
        sign_voucher = (user_profile.person.gender != 0)
        if not sign_voucher:
            sign_voucher = show_yes_no_box("Geschlecht fehlt", "Im Profil muss das Geschlecht angegeben werden. Dennoch unterschreiben? (nicht empfohlen)")
        if sign_voucher:
            form_sing_as_guarantor.show_form(self.voucher)

    def send_to_guarantor(self):
        form_send_to_guarantor.show_form(self.voucher)

    def update_status(self, voucher: MinutoVoucher):
        """
        Update the UI based on the current status of the voucher,
        enabling or disabling buttons accordingly.
        """
        # Check conditions for voucher status
        own_voucher = (voucher.creator_id == user_profile.person.id)
        number_of_guarantors =  len(voucher.guarantor_signatures)
        enough_guarantors = (number_of_guarantors >= 2)

        no_creator_signature = (voucher.creator_signature is None)

        # check if at least one male and one female guarantor exist
        guarantor_genders = {str(g_sign[0]['gender']) for g_sign in voucher.guarantor_signatures}
        both_genders_present = '1' in guarantor_genders and '2' in guarantor_genders

        # Enable or disable buttons based on voucher status
        self.pushButtonSendToGuarantor.setEnabled(own_voucher and not enough_guarantors)
        self.pushButtonSignAsCreator.setEnabled(own_voucher and enough_guarantors and both_genders_present and no_creator_signature)
        self.pushButtonSignAsGuarantor.setEnabled(not own_voucher and not enough_guarantors)

        voucher_status = ""
        if own_voucher:
            voucher_status += "<b>Eigener Gutschein"
            if number_of_guarantors == 0:
                voucher_status += " (Bürgen fehlen)"
            elif not '1' in guarantor_genders:
                voucher_status += " (männlicher Bürge fehlt)"
            elif not '2' in guarantor_genders:
                voucher_status += " (weiblicher Bürge fehlt)"
            elif no_creator_signature is None:
                voucher_status += " (Eigene Unterschrift fehlt)"
            elif voucher.verify_complete_voucher():
                voucher_status += " (Gültig)"
            else:
                voucher_status += " (Ungültig!)"

        else:
            voucher_status += "<b>Erhaltener Gutschein"
            if not enough_guarantors:
                voucher_status += " (Nicht genug Bürgen)"
            elif no_creator_signature is None:
                voucher_status += " (Ersteller Unterschrift fehlt)"
            elif voucher.verify_complete_voucher():
                voucher_status += " (Gültig)"
            else:
                voucher_status += " (Ungültig!)"
        voucher_status += "</b>"

        self.labelInfoTextLeft.setText(voucher_status)

        available_amount = voucher.get_voucher_amount(user_profile.person.id)
        self.labelInfoTextRight.setText(f"<b>Verfügbarer Betrag:  {available_amount} Minuto</b>")

    def show_raw_data(self):
        """ Display raw data of the voucher. """
        form_show_raw_data.show_data(self.voucher)

    def show_voucher(self, voucher: MinutoVoucher):
        """
        Display voucher details in a table view.
        Translates attribute names and formats values for presentation.
        """
        self.voucher = voucher
        model = QStandardItemModel(self)
        model.setColumnCount(2)
        model.setHorizontalHeaderLabels(["Inhalt", "Wert"])

        # Translate and display each voucher attribute
        translations = {
            'voucher_id': 'Gutschein-ID',
            'temp_voucher_id': 'Temporäre Gutschein-ID',
            'creator_id': 'Ersteller-ID',
            'creator_first_name': 'Vorname',
            'creator_last_name': 'Nachname',
            'creator_organization': 'Organisation',
            'creator_address': 'Adresse',
            'creator_gender': 'Geschlecht',
            'amount': 'Betrag',
            'description': 'Beschreibung',
            'footnote': 'Fußnote',
            'service_offer': 'Serviceangebot',
            'valid_until': 'Gültig bis',
            'region': 'Region',
            'coordinates': 'Koordinaten',
            'email': 'E-Mail',
            'phone': 'Telefon',
            'creation_date': 'Erstellungsdatum',
            'is_test_voucher': 'Ist Testgutschein',
            'guarantor_signatures': 'Anzahl Bürgen',
            'creator_signature': 'Unterschrift des Erstellers',
            'transactions': 'Transaktionen'
        }

        for attr, value in vars(voucher).items():
            translated_attr = translations.get(attr, attr)  # Translate or use original attribute name

            # Convert value to a more human-readable format if necessary
            if attr == 'creator_gender':
                value = {0: "Unbekannt", 1: "Männlich", 2: "Weiblich"}.get(value, "Unbekannt")
            elif attr == 'is_test_voucher':
                value = "Ja" if value else "Nein"
            elif isinstance(value, list):
                value = str(len(value))  # For lists, show their length
            elif attr == 'creator_signature':
                value = "Unterschrieben" if value else "Nicht unterschrieben"

            label_item = QStandardItem(translated_attr)
            value_item = QStandardItem(str(value))
            model.appendRow([label_item, value_item])

        self.tableView_voucher.setModel(model)
        self.tableView_voucher.verticalHeader().setVisible(False)
        self.tableView_voucher.horizontalHeader().setVisible(True)
        self.tableView_voucher.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_voucher.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableView_voucher.setWordWrap(True)
        self.tableView_voucher.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableView_voucher.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.update_status(voucher)
        self.show()

    def create_non_editable_item(self, text):
        """ Create a non-editable table item with the provided text. """
        item = QStandardItem(str(text))
        item.setEditable(False)
        return item


class Dialog_Create_Minuto(QMainWindow, Ui_DialogCreateMinuto):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialized = False  # Flag to track initialization
        self.lineEdit_amount.textChanged.connect(self.update_voucher_description)
        self.pushButton_CreateVoucher.clicked.connect(self.create_minuto)
        self.init_values()

    def showEvent(self, event: QShowEvent):
        """Called when the dialog is shown."""
        if not self.initialized:
            self.init_values()
            self.initialized = True
        super().showEvent(event)

    def create_minuto(self):
        # Extrahiere die Werte aus den GUI-Elementen
        amount = int(self.lineEdit_amount.text())
        region = self.lineEdit_region.text()
        years_valid = int(self.spinBox_years_valid.text())

        first_name = self.lineEdit_creator_first_name.text()
        last_name = self.lineEdit_creator_last_name.text()
        organization = self.lineEdit_creator_organization.text()
        address = self.lineEdit_creator_address.text()
        email = self.lineEdit_email.text()
        phone = self.lineEdit_phone.text()
        service_offer = self.textEdit_service_offer.toPlainText()
        coordinates = self.lineEdit_coordinates.text()
        is_test_vocher = self.checkBox_is_test_voucher.isChecked()

        gender = self.comboBox_creator_gender.currentIndex() # 0 unknown, 1 male, 2 female
        footnote = self.label_footnote.text()
        description = self.label_voucher_description.text()
        voucher = user_profile.create_voucher(first_name, last_name, organization, address, gender, email, phone, service_offer,
                                    coordinates, amount, region, years_valid, is_test_vocher, description, footnote)
        form_show_voucher.show_voucher(voucher)
        self.initialized = False # to load values from profile on next show
        self.close()


    def init_values(self):
        address = (f"{user_profile.person_data['street']} {user_profile.person_data['zip_code']} "
                   f"{user_profile.person_data['city']} {user_profile.person_data['state_or_region']} "
                   f"{user_profile.person_data['country']}")
        self.lineEdit_amount.setText("1000")
        self.lineEdit_region.setText(user_profile.person_data['zip_code'])
        self.comboBox_creator_gender.setCurrentIndex(int(user_profile.person_data['gender']))
        self.lineEdit_coordinates.setText(user_profile.person_data['coordinates'])
        self.update_voucher_description(self.lineEdit_amount.text())
        self.lineEdit_creator_organization.setText(user_profile.person_data['organization'])
        self.lineEdit_creator_first_name.setText(user_profile.person_data['first_name'])
        self.lineEdit_creator_last_name.setText(user_profile.person_data['last_name'])
        self.lineEdit_creator_address.setText(address)
        self.lineEdit_email.setText(user_profile.person_data['email'])
        self.lineEdit_phone.setText(user_profile.person_data['phone'])
        self.textEdit_service_offer.setText(user_profile.person_data['service_offer'])
        self.label_footnote.setText("Gutschein-Nutzung nur für Mitspieler/innen.")

    def update_voucher_description(self, amount):
        """Update the voucher description based on the amount."""
        if amount:
            self.label_voucher_description.setText(
                f"Gutschein für Waren oder Dienstleistungen im Wert von {amount} Minuten qualitativer Leistung.")
        else:
            self.label_voucher_description.setText("Gutschein für Waren oder Dienstleistungen")


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
        self.pushButton_open_voucher_or_signature.clicked.connect(open_data_file)

    def init_show(self):
        self.init_values()
        self.show()

    def init_values(self):
        # Accumulate all vouchers from all categories
        self.all_vouchers = []
        for status in VoucherStatus:
            self.all_vouchers += user_profile.person.voucherlist[status.value]

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
            self.create_non_editable_item(voucher.valid_until),
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
        user_profile.person.set_person_data(user_profile.person_data) # update person from person_data in profile
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
        frm_main_window.dialog_generate_profile.show()

    def restore_profile(self):
        self.close()



class Frm_Mainwin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dialog_generate_profile = Dialog_Generate_Profile()
        self.dialog_generate_profile.profileCreated.connect(self.onProfileCreated)

        self.setWindowTitle(f"eMinuto")
        self.actionCreateProfile.triggered.connect(self.dialog_generate_profile.show)
        self.actionEditProfile.triggered.connect(dialog_profile.init_and_show)
        self.actionCreateMinuto.triggered.connect(dialog_create_minuto.show)
        self.actionProfileLogin.triggered.connect(dialog_profile_login.login)
        self.actionProfileLogout.triggered.connect(self.profile_logout)
        self.actionVoucherList.triggered.connect(dialog_voucher_list.init_show)
        self.actionOpenFile.triggered.connect(open_data_file)

        self.actionClose.triggered.connect(self.close)
        self.set_gui_depending_profile_status()

        self.pushButton_copy_user_ID.clicked.connect(self.copyUserIDToClipboard)

    def copyUserIDToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(user_profile.person.id)

    def onProfileCreated(self):
        self.profile_logout()
        dialog_profile_login.show()

    def update_values(self):
        self.setWindowTitle(f"eMinuto - Profil: {user_profile.profile_name}")
        self.label_user_id.setText(f"{user_profile.person.id[:16]}...")
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

form_sing_as_guarantor = FormSignAsGuarantor()
form_send_to_guarantor = FormSendToGuarantor()
form_show_raw_data = FormShowRawData()
dialog_profile_login = Dialog_Profile_Login()
dialog_profile_create_selection = Dialog_Profile_Create_Selection()
dialog_profile = Dialog_Profile()
dialog_create_minuto = Dialog_Create_Minuto()
dialog_voucher_list = DialogVoucherList()
form_show_voucher = FormShowVoucher()


frm_main_window = Frm_Mainwin()

