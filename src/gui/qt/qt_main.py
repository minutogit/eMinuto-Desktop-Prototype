# qt_main.py
import functools
import os
import sys

from PySide6.QtCore import QSortFilterProxyModel, Qt, QSize, QModelIndex, QDateTime, QTranslator, QCoreApplication
from PySide6.QtGui import QAction, QShowEvent, QIcon
from PySide6.QtWidgets import QApplication, QStatusBar, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, \
    QCheckBox, QVBoxLayout, QMessageBox
from PySide6.QtWidgets import QMainWindow, QMenu, QHeaderView

from src.gui.qt.profile_dialogs import Dialog_Generate_Profile, Dialog_Profile_Login, Dialog_Profile, \
    Dialog_Profile_Create_Selection
from src.gui.qt.ui_components.dialog_create_minuto import Ui_DialogCreateMinuto
from src.gui.qt.ui_components.dialog_voucher_list import Ui_DialogVoucherList
from src.gui.qt.ui_components.dialog_transaction_list import Ui_DialogTransactionList

from src.gui.qt.ui_components.form_show_raw_data import Ui_FormShowRawData
from src.gui.qt.ui_components.form_show_voucher import Ui_FormShowVoucher
from src.gui.qt.ui_components.form_show_transaction import Ui_FormShowTransaction
from src.gui.qt.ui_components.main_window import Ui_MainWindow
from src.gui.qt.ui_components.form_send_to_guarantor import Ui_FormSendToGuarantor
from src.gui.qt.ui_components.form_sign_as_guarantor import Ui_FormSignVoucherAsGuarantor
from src.gui.qt.ui_components.form_send_minuto import Ui_FormSendMinuto
from src.gui.qt.ui_components.dialog_forgot_password import Ui_DialogForgotPassword
from src.models.user_transaction import UserTransaction
from src.services.crypto_utils import verify_user_ID, check_word_seed

from src.gui.qt.utils import apply_global_styles, show_message_box, show_yes_no_box, DecimalFormatValidator, \
    format_table_cell
from src.models.user_profile import user_profile
from src.models.minuto_voucher import MinutoVoucher, VoucherStatus
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QAbstractItemView
from src import config


from src.services.utils import dprint, display_balance, is_iso8601_datetime, is_password_valid, get_version


def open_data_file(file_type=""):
    """
    Opens a file dialog to select a transaction, voucher or signature file and adds the voucher
    or signature to a voucher.
    """

    app = QApplication.instance()

    # Set the accepted file extensions
    if file_type == "transaction":
        file_filter = app.translate("MainWindow", "Transaction Files (*.mt);;All Files (*)")
    elif file_type == "signature":
        file_filter = app.translate("MainWindow", "Signature Files (*.ms);;All Files (*)")
    else:
        file_filter = app.translate("MainWindow", "Voucher/Signature/Transaction Files (*.mv *.ms *.mt);;All Files (*)")

    # Create and open the dialog and get the file path
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(None, app.translate("MainWindow", "Open File"), "", file_filter)

    if file_path:
        # if not a voucher then None will be returned
        voucher, transaction, info_msg = user_profile.open_file(file_path)
        win['dialog_voucher_list'].init_values()

        frm_main_window.update_values()  # update balances in main window
        show_message_box(app.translate("MainWindow", "Info"), info_msg)  # display info to user
        if voucher is not None:
            win['form_show_voucher'].show_voucher(voucher)

        if transaction is not None:
            win['dialog_transaction_list'].init_show()



class DialogForgotPassword(QMainWindow, Ui_DialogForgotPassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_save_new_password.clicked.connect(self.overwrite_old_password)

    def overwrite_old_password(self):
        seed = self.lineEdit_seed_words.text().strip()
        password = self.lineEdit_new_password.text()
        password_retyped = self.lineEdit_new_password_retyped.text()

        if not is_password_valid(password) and not config.TEST_MODE:
            show_message_box(self.tr("Error!"), self.tr("Password must be at least 8 characters long."))
            return

        if password != password_retyped:
            show_message_box(self.tr("Error"), self.tr("Passwords must match."))
            return

        if not check_word_seed(seed):
            show_message_box(self.tr("Error"), self.tr("The seed words are not correct."))
            return

        if not user_profile.recover_password_with_seed(seed, password):
            show_message_box(self.tr("Error"), self.tr("The seed words are not correct."))
            return
        else:
            self.close()
            show_message_box(self.tr("Password changed"), self.tr("Password successfully changed."))
            frm_main_window.profile_logout()
            frm_main_window.dialog_profile_login.login()


class FormSendMinuto(QMainWindow, Ui_FormSendMinuto):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Set validator for correct input format
        self.available_amount = 0 # Store max amount to send
        self.lineEdit_transfer_amount.setValidator(DecimalFormatValidator())
        self.lineEdit_recipient_id.textChanged.connect(self.check_recipient_ID)
        self.pushButton_Send_Minuto.clicked.connect(self.send_minuto)
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

    def check_recipient_ID(self):
        """
        Check the entered recipient ID and update the label with a green check or red cross based on validity.
        """
        recipient_id = self.lineEdit_recipient_id.text().strip()
        self.pushButton_Send_Minuto.setEnabled(False)
        if recipient_id == "":
            self.label_recipient_id_check.setText("")  # Clear label if input is empty
            return

        # Set label based on the validity of the recipient ID
        if verify_user_ID(recipient_id):
            if recipient_id == user_profile.person.id:
                show_message_box(self.tr("Error!"), self.tr("Do not use your own ID!"))
                return
            self.label_recipient_id_check.setText("✅")  # Green check emoji for valid ID
            self.pushButton_Send_Minuto.setEnabled(True)

        else:
            self.label_recipient_id_check.setText("❌")  # Red cross emoji for invalid ID

    def send_minuto(self):
        recipient_id = self.lineEdit_recipient_id.text()
        purpose = self.lineEdit_purpose.text()
        amount = float(self.lineEdit_transfer_amount.text().replace(",","."))

        if amount > self.available_amount:
            show_message_box(self.tr("Insufficient Balance"),
                             self.tr("You can send a maximum of %s Minuto.") % self.available_amount)
            return

        if not show_yes_no_box(self.tr("Send Minuto?"), self.tr("Do you want to send the Minuto?")):
            return

        transaction = user_profile.send_minuto(amount, purpose, recipient_id)
        if not transaction.transaction_successful:
            show_message_box(self.tr("Error"), self.tr("Transaction failed"))
            return

        suggested_filename = f"eMinuto-Transaction-to-{recipient_id[:6]}.mt"
        file_filter = self.tr("Minuto Transaction (*.mt)")

        # Open file save dialog
        filename_with_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save Transaction"),
            suggested_filename,
            file_filter
        )

        # Check if the user has entered a file name
        if filename_with_path:
            # Encrypt and save the transaction
            user_profile._secure_file_handler.encrypt_with_shared_secret_and_save(
                transaction, filename_with_path, recipient_id, user_profile.person.id)

        self.close()
        win['form_show_transaction'].show_transaction(transaction)
        frm_main_window.update_values() # Update balances in main window


    def show_init(self):
        self.setWindowTitle(self.tr("Send Minuto - Profile: %s") % user_profile.profile_name)
        self.available_amount = user_profile.person.get_amount_of_all_vouchers()
        self.lineEdit_recipient_id.setText("")
        self.lineEdit_transfer_amount.setText("")
        self.lineEdit_purpose.setText("")
        self.check_recipient_ID()
        self.show()
        self.raise_()



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
            user_profile.save_voucher_to_disk(self.voucher)  # save signed voucher
            # update gui
            self.checkBox_liability_acceptance.setEnabled(False)
            self.pushButton_sign_as_guarantor.setEnabled(False)
            self.pushButton_save_as_file.setEnabled(True)


    def save_signature_as_file(self):
        """
        Save the signature as a file, either encrypted or plain based on the user's choice.
        """
        self.guarantor_signature = user_profile.person.get_own_guarantor_signature(self.voucher)
        creator_id = self.voucher.creator_id
        creator_name = self.voucher.creator_first_name

        suggested_filename = f"eMinuto-{creator_name}_Signature-{user_profile.person.first_name}.ms"
        file_filter = self.tr("Minuto Signature (*.ms)")

        # Open file save dialog
        filename_with_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save Signature"),
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
        self.pushButton_save_as_file.setEnabled(False)

        self.checkBox_liability_acceptance.setChecked(False)
        self.checkBox_liability_acceptance.setEnabled(True)
        self.setWindowTitle(self.tr("Sign eMinuto as Guarantor - Profile: %s") % user_profile.profile_name)

        # when already own signate then change gui
        for sig in voucher.guarantor_signatures:
            if sig[0]["id"] == user_profile.person.id:
                self.checkBox_liability_acceptance.setChecked(True)
                self.checkBox_liability_acceptance.setEnabled(False)
                self.pushButton_sign_as_guarantor.setEnabled(False)
                self.pushButton_save_as_file.setEnabled(True)
                self.show()
                show_message_box(self.tr("Signature available"),
                                 self.tr("This voucher is already signed. Simply forward the signature to the creator."))
                return

        self.show()
        self.raise_()



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
                show_message_box(self.tr("Error!"), self.tr("Do not use your own ID!"))
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
            show_message_box(self.tr("Error!"), self.tr("Valid Guarantor ID is required for encryption!"))
            return

        suggested_filename = self.tr("eMinuto-%s.mv") % user_profile.person.first_name
        file_filter = self.tr("Minuto Voucher (*.mv)")

        # Open file save dialog
        filename_with_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save Voucher"),
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
        self.setWindowTitle(self.tr("Send eMinuto to Guarantor - Profile: %s") % user_profile.profile_name)
        self.show()
        self.raise_()



class FormShowRawData(QMainWindow, Ui_FormShowRawData):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_Close.clicked.connect(self.close)

    def show_data(self, object, title_prefix=""):
        import json
        # First, convert the object to a serializable dictionary
        serializable_representation = object.to_dict()

        # Convert the dictionary to a JSON-formatted string
        json_representation = json.dumps(serializable_representation, sort_keys=False, indent=4, ensure_ascii=False)
        self.textEdit_text_data.setText(json_representation)
        self.setWindowTitle(self.tr("%sRaw Data - Profile: %s") % (title_prefix, user_profile.profile_name))
        self.show()
        self.raise_()



class FormShowVoucher(QMainWindow, Ui_FormShowVoucher):
    """
    FormShowVoucher class for displaying and managing voucher information.
    """

    def __init__(self):
        """ Initialize the FormShowVoucher window. """
        super().__init__()
        self.setupUi(self)
        self.voucher:MinutoVoucher() = None
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonRawData.clicked.connect(self.show_raw_data)
        self.pushButtonSignAsGuarantor.clicked.connect(self.sing_as_guarantor)
        self.pushButtonSendToGuarantor.clicked.connect(self.send_to_guarantor)
        self.pushButtonAddGuarantorSignature.clicked.connect(self.add_guarantor_signature)
        self.pushButtonSignAsCreator.clicked.connect(self.sign_as_creator)
        self.pushButtonTrash.clicked.connect(self.delete_voucher)
        self.pushButtonRecover.clicked.connect(self.recover_trashed_voucher)

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

    def recover_trashed_voucher(self):
        # recover back a trashed voucher
        user_profile.save_voucher_to_disk(self.voucher) # save without trash flag will restore voucher
        self.show_voucher(self.voucher) # to reload gui
        frm_main_window.update_values()  # update values in main win (calculate new amount etc)

    def delete_voucher(self):
        status = self.voucher.voucher_status(user_profile.person.id)
        amount = self.voucher.get_voucher_amount(user_profile.person.id)
        if user_profile.vouchers[id(self.voucher)]['trashed']:
            if not show_yes_no_box(self.tr("Permanently delete voucher?"),
                                   self.tr(
                                       "Are you sure you want to permanently delete the voucher? \n(Balance: %s Minuto)") % amount):
                return


        # if own voucher with amount
        elif status == VoucherStatus.OWN:
            if not show_yes_no_box(self.tr("Remove own voucher?"),
                                   self.tr(
                                       "Own voucher with %s Minuto balance. Do you really want to move it to the trash?") % amount):
                return
        # if voucher from others with amount
        elif status == VoucherStatus.OTHER:
            if not show_yes_no_box(self.tr("Remove voucher with balance?"),
                                   self.tr(
                                       "This voucher still has %s Minuto balance. Do you really want to move it to the trash?") % amount):
                return
        # if voucher from others with amount
        elif status == VoucherStatus.UNFINISHED:
            if not show_yes_no_box(self.tr("Remove unfinished voucher?"),
                            self.tr("Do you really want to move it to the trash?")):
                return
        # if voucher from others with amount
        elif status == VoucherStatus.ARCHIVED:
            if not show_yes_no_box(self.tr("Remove used voucher?"),
                            self.tr("Used vouchers are needed for fraud detection. They should not be deleted.")):
                return

        user_profile.save_voucher_to_disk(self.voucher, trash=True)
        self.close()
        # reload voucher list if open
        if not win['dialog_voucher_list'].isHidden():
            win['dialog_voucher_list'].init_show()
        frm_main_window.update_values() # update values in main win (calculate new amount etc)

    def sign_as_creator(self):
        sign = show_yes_no_box(self.tr("Sign voucher as creator"),
                               self.tr("Do you want to sign the voucher? This makes it valid and can be used for transactions."))
        if sign:
            signed, message = user_profile.person.sign_voucher_as_creator(self.voucher)

            if signed:
                user_profile.save_voucher_to_disk(self.voucher)
                user_profile.person.current_voucher = None
                self.show_voucher(self.voucher)  # to update all values
                frm_main_window.update_values()
                show_message_box(self.tr("Signature successful"),
                                 self.tr("Signature was successful. The voucher is now ready and can be used."))

            else:
                show_message_box(self.tr("Error"), self.tr("Signature failed. %s") % message)


    def sing_as_guarantor(self):
        gender_is_set = (user_profile.person.gender != 0)
        # male and female needed, so with 2 guarantors gender must be set
        if self.voucher.needed_guarantors == 2 and not gender_is_set:
            show_message_box(self.tr("Gender missing"),
                             self.tr("Please set the gender in the profile, as the voucher requires a male and female guarantor."))
            win['dialog_profile'].init_and_show()
            return

        win['form_sign_as_guarantor'].show_form(self.voucher)  # to reload gui


    def add_guarantor_signature(self):
        # to open a file with a signature to add to voucher)
        open_data_file(file_type="signature")


    def send_to_guarantor(self):
        win['form_send_to_guarantor'].show_form(self.voucher)

    def update_status(self, voucher: MinutoVoucher):
        """
        Update the UI based on the current status of the voucher,
        enabling or disabling buttons accordingly.
        """
        # Check conditions for voucher status
        own_voucher = (voucher.creator_id == user_profile.person.id)
        number_of_guarantors = len(voucher.guarantor_signatures)
        enough_guarantors = (number_of_guarantors >= 2)
        trashed_voucher = user_profile.vouchers[id(self.voucher)]['trashed']

        no_creator_signature = (voucher.creator_signature is None)

        # check if at least one male and one female guarantor exist
        guarantor_genders = {str(g_sign[0]['gender']) for g_sign in voucher.guarantor_signatures}
        both_genders_present = '1' in guarantor_genders and '2' in guarantor_genders

        # Enable or disable buttons based on voucher status
        self.pushButtonAddGuarantorSignature.hide()
        self.pushButtonSignAsGuarantor.hide()
        self.pushButtonSignAsCreator.hide()
        self.pushButtonSendToGuarantor.hide()
        self.pushButtonRecover.hide()
        if own_voucher and not enough_guarantors and not trashed_voucher:
            self.pushButtonAddGuarantorSignature.show()

        if own_voucher and not enough_guarantors and not trashed_voucher:
            self.pushButtonSendToGuarantor.show()

        if own_voucher and enough_guarantors and both_genders_present and no_creator_signature and not trashed_voucher:
            self.pushButtonSignAsCreator.show()

        if not own_voucher and not enough_guarantors and not trashed_voucher:
            self.pushButtonSignAsGuarantor.show()

        if user_profile.vouchers[id(self.voucher)]['trashed']:
            self.pushButtonRecover.show()
            self.pushButtonTrash.setText(self.tr("Permanently delete"))
            self.pushButtonRecover.setText(self.tr("Restore"))
        else:
            self.pushButtonTrash.setText(self.tr("Move to Trash"))

        voucher_stat_text = ""
        if own_voucher:
            voucher_stat_text += f"<b>{self.tr('Own voucher')}"
            if trashed_voucher:
                voucher_stat_text += f" ({self.tr('deleted')})"
            elif number_of_guarantors == 0:
                voucher_stat_text += f" ({self.tr('guarantors missing')})"
            elif '1' not in guarantor_genders:
                voucher_stat_text += f" ({self.tr('missing male guarantor')})"
            elif '2' not in guarantor_genders:
                voucher_stat_text += f" ({self.tr('missing female guarantor')})"
            elif no_creator_signature:
                voucher_stat_text += f" ({self.tr('missing creator signature')})"
            elif voucher.verify_complete_voucher():
                voucher_stat_text += f" ({self.tr('Valid')})"
            else:
                voucher_stat_text += f" ({self.tr('Invalid')})"

        else:
            voucher_stat_text += f"<b>{self.tr('Received voucher')}"
            if not enough_guarantors:
                voucher_stat_text += f" ({self.tr('Insufficient guarantors')})"
            elif no_creator_signature:
                voucher_stat_text += f" ({self.tr('missing creator signature')})"
            elif voucher.verify_complete_voucher():
                voucher_stat_text += f" ({self.tr('Valid')})"
            else:
                voucher_stat_text += f" ({self.tr('Invalid')})"
        voucher_stat_text += "</b>"

        self.labelInfoTextLeft.setText(voucher_stat_text)

        available_amount = voucher.get_voucher_amount(user_profile.person.id)
        self.labelInfoTextRight.setText("<b>%s: %s Minuto</b>" % (self.tr('Available Balance'), available_amount))

    def show_raw_data(self):
        """ Display raw data of the voucher. """
        win['form_show_raw_data'].show_data(self.voucher, self.tr("eMinuto-"))

    def init_table(self, voucher: MinutoVoucher = None):
        if voucher is None:
            voucher = self.voucher

        model = QStandardItemModel(self)
        model.setColumnCount(2)
        model.setHorizontalHeaderLabels([self.tr("Content"), self.tr("Value")])

        # Translate and display each voucher attribute
        translations = {
            'voucher_id': self.tr('Voucher ID'),
            'creator_id': self.tr('Creator ID'),
            'creator_first_name': self.tr('First Name'),
            'creator_last_name': self.tr('Last Name'),
            'creator_organization': self.tr('Organization'),
            'creator_address': self.tr('Address'),
            'creator_gender': self.tr('Gender'),
            'amount': self.tr('Amount'),
            'description': self.tr('Description'),
            'footnote': self.tr('Footnote'),
            'service_offer': self.tr('Service Offer'),
            'valid_until': self.tr('Valid Until'),
            'region': self.tr('Region'),
            'coordinates': self.tr('Coordinates'),
            'email': self.tr('Email'),
            'phone': self.tr('Phone'),
            'creation_date': self.tr('Creation Date'),
            'is_test_voucher': self.tr('Is Test Voucher'),
            'guarantor_signatures': self.tr('Number of Guarantors'),
            'creator_signature': self.tr('Creator Signature'),
            'transactions': self.tr('Transactions'),
            'needed_guarantors': self.tr('Needed Guarantors')
        }

        for attr, value in vars(voucher).items():
            translated_attr = translations.get(attr, attr)  # Translate or use original attribute name

            # Convert value to a more human-readable format if necessary
            if attr == 'creator_gender':
                value = {0: self.tr("Unknown"), 1: self.tr("Male"), 2: self.tr("Female")}.get(value, self.tr("Unknown"))
            elif attr == 'is_test_voucher':
                value = self.tr("Yes") if value else self.tr("No")
            elif isinstance(value, list):
                value = str(len(value))  # For lists, show their length
            elif attr == 'creator_signature':
                value = self.tr("Signed") if value else self.tr("Not Signed")

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

    def show_voucher(self, voucher: MinutoVoucher):
        """
        Display voucher details in a table view.
        Translates attribute names and formats values for presentation.
        """
        self.voucher = voucher
        self.init_table(voucher)
        self.update_status(voucher)
        self.setWindowTitle(self.tr("eMinuto Details - Profile: %s") % user_profile.profile_name)
        self.show()
        self.raise_()
        # close other forms and dialog which depend on voucher
        win['form_sign_as_guarantor'].close()
        win['form_send_to_guarantor'].close()

        # if ready to sign as creator show message
        if not self.pushButtonSignAsCreator.isHidden():
            show_message_box(self.tr("Complete Voucher Signature"),
                             self.tr("Sign this voucher to make it usable."))


class FormShowTransaction(QMainWindow, Ui_FormShowTransaction):
    """
    FormShowVoucher class for displaying and managing voucher information.
    """

    def __init__(self):
        """ Initialize the FormShowVoucher window. """
        super().__init__()
        self.setupUi(self)
        self.voucher:MinutoVoucher() = None
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonRawData.clicked.connect(self.show_raw_data)
        self.pushButtonSaveTransactionFile.clicked.connect(self.save_transaction)
        self.apply_stylesheet_to_buttons()
        self.transaction: UserTransaction = None

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


    def show_raw_data(self):
        """ Display raw data of the voucher. """
        win['form_show_raw_data'].show_data(self.transaction, "Transaktions-")

    def init_table(self, transaction: UserTransaction = None):
        if transaction is None:
            transaction = self.transaction

        model = QStandardItemModel(self)
        model.setColumnCount(2)
        model.setHorizontalHeaderLabels([self.tr("Content"), self.tr("Value")])

        # Translate and display each transaction attribute
        translations = {
            'transaction_id': self.tr('Transaction ID'),
            'transaction_sender_id': self.tr('Sender ID'),
            'transaction_recipient_id': self.tr('Recipient ID'),
            'transaction_amount': self.tr('Amount'),
            'transaction_purpose': self.tr('Purpose'),
            'transaction_vouchers': self.tr('Number of Vouchers'),
            'transaction_successful': self.tr('Valid Transaction'),
            'transaction_failure_reason': self.tr('Transaction Failure Reason'),
            'transaction_start_timestamp': self.tr('Start Timestamp'),
            'transaction_end_timestamp': self.tr('End Timestamp')
        }


        for attr, value in vars(transaction).items():
            translated_attr = translations.get(attr, attr)  # Translate or use original attribute name

            # Convert value to a more human-readable format if necessary
            if attr == 'transaction_successful':
                value = self.tr("Yes") if value else self.tr("No")

            # show number of vouchers
            elif attr == 'transaction_vouchers':
                value = len(value)

            elif attr == 'transaction_failure_reason' and transaction.transaction_successful:
                continue  # don't display failure reason if successful transaction

            label_item = QStandardItem(translated_attr)
            value_item = QStandardItem(str(value))
            model.appendRow([label_item, value_item])

        self.tableView_transaction.setModel(model)
        self.tableView_transaction.verticalHeader().setVisible(False)
        self.tableView_transaction.horizontalHeader().setVisible(True)
        self.tableView_transaction.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_transaction.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableView_transaction.setWordWrap(True)
        self.tableView_transaction.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableView_transaction.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def save_transaction(self):
        # Saves the transaction to file (for sending again to recipient)
        recipient_id = self.transaction.transaction_recipient_id

        if not show_yes_no_box(self.tr("Save Minuto Transaction File?"),
                               self.tr("Do you want to save the Minuto transaction file to be able to send it again to the recipient?")):
            return

        if self.transaction.transaction_recipient_id == user_profile.person.id:
            show_message_box(self.tr("Error"), self.tr("Received transaction cannot be sent."))
            return

        suggested_filename = f"eMinuto-Transaction-to-{recipient_id[:6]}.mt"
        file_filter = self.tr("Minuto Transaction (*.mt)")

        # Open file save dialog
        filename_with_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save Transaction"),
            suggested_filename,
            file_filter
        )

        # Check if the user has entered a file name
        if filename_with_path:
            # Encrypt and save the transaction
            user_profile._secure_file_handler.encrypt_with_shared_secret_and_save(
                self.transaction, filename_with_path, recipient_id, user_profile.person.id)

    def show_transaction(self, transaction: UserTransaction):
        """
        Display transaction details in a table view.
        Translates attribute names and formats values for presentation.
        """
        self.transaction = transaction
        self.pushButtonSaveTransactionFile.hide()
        if transaction.transaction_recipient_id != user_profile.person.id:
            self.pushButtonSaveTransactionFile.show()
        self.init_table(transaction)
        self.setWindowTitle(self.tr("Transaction Details - Profile: %s") % user_profile.profile_name)

        self.show()
        self.raise_()


class Dialog_Create_Minuto(QMainWindow, Ui_DialogCreateMinuto):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialized = False  # Flag to track initialization
        self.lineEdit_amount.textChanged.connect(self.update_voucher_description)
        self.pushButton_CreateVoucher.clicked.connect(self.create_minuto)
        self.init_values()

    # initialized flag is need to prevent reset to init_values when windows was closed
    # so form data does not get lost on window close
    def showEvent(self, event: QShowEvent):
        """Called when the dialog is shown."""
        if not self.initialized:
            self.init_values()
            self.initialized = True
        super().showEvent(event)
        self.raise_()

    def create_minuto(self):
        # Extract values from the GUI elements
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
        is_test_voucher = self.checkBox_is_test_voucher.isChecked()

        gender = self.comboBox_creator_gender.currentIndex()  # 0 unknown, 1 male, 2 female
        footnote = self.label_footnote.text()
        description = self.label_voucher_description.text()
        voucher = user_profile.create_voucher(first_name, last_name, organization, address, gender, email, phone, service_offer,
                                    coordinates, amount, region, years_valid, is_test_voucher, description, footnote)
        # Reload voucher list if open
        if not win['dialog_voucher_list'].isHidden():
            win['dialog_voucher_list'].init_show()
        win['form_show_voucher'].show_voucher(voucher)
        self.initialized = False  # to load values from profile on next show
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
        self.label_footnote.setText(self.tr("Voucher usage only for players."))
        self.setWindowTitle(self.tr("Create eMinuto - Profile: %s") % user_profile.profile_name)

    def update_voucher_description(self, amount):
        """Update the voucher description based on the amount."""
        if amount:
            self.label_voucher_description.setText(
                self.tr("Voucher for goods or services worth %s minutes of quality work.") % amount)
        else:
            self.label_voucher_description.setText(self.tr("Voucher for goods or services"))



class CustomSortFilterProxyModel(QSortFilterProxyModel):
    """
    A custom filter proxy model to filter table rows based on text.
    It supports filtering with a logical "AND" between words and a logical "OR" across visible columns.
    This model allows rows to be shown if each word in the filter text is found in any of the visible columns.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the CustomSortFilterProxyModel with empty lists for visible_columns and filter_words.
        """
        super().__init__(*args, **kwargs)
        self.visible_columns = []  # List of indexes of columns that are visible
        self.filter_words = []  # List of words to filter by


    def set_visible_columns(self, columns):
        """
        Sets the visible columns in the table view.

        :param columns: A list of column indexes that are visible.
        """
        self.visible_columns = columns
        self.invalidateFilter()  # Important to reapply the filter

    def set_filter_text(self, text):
        """
        Sets the filter text, splitting it into words for the filter.

        :param text: The text string to filter by.
        """
        self.filter_words = [word.lower() for word in text.split() if word]
        self.invalidateFilter()  # Important to reapply the filter

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Reimplementation of the filterAcceptsRow method to apply a custom filter.
        The row is accepted if each word in the filter text is found in any of the visible columns.

        :param source_row: The row number in the model.
        :param source_parent: The parent index in the model.
        :return: True if the row should be included; otherwise False.
        """
        if not self.filter_words:
            return True  # No filter set, accept all rows

        # Check each column for each word
        for word in self.filter_words:
            word_found_in_any_column = False
            for col in self.visible_columns:
                cell_text = str(self.sourceModel().index(source_row, col, source_parent).data()).lower()
                if word in cell_text:
                    word_found_in_any_column = True
                    break  # Word found in this column, no need to check further

            if not word_found_in_any_column:
                return False  # Word not found in any of the visible columns

        # All words were found in at least one of the visible columns
        return True

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        """
        Reimplementation of the lessThan method to handle numerical sorting based on the Qt.UserRole.

        :param left: The QModelIndex of the left item.
        :param right: The QModelIndex of the right item.
        :return: True if the left item is less than the right item; otherwise False.
        """
        leftData = self.sourceModel().data(left, Qt.UserRole)
        rightData = self.sourceModel().data(right, Qt.UserRole)

        # If both leftData and rightData are of type float or int, compare them as numbers
        if isinstance(leftData, (float, int)) and isinstance(rightData, (float, int)):
            return leftData < rightData

        # Otherwise, fall back to the default implementation for other types (e.g., string comparison)
        return super().lessThan(left, right)


class DialogVoucherList(QMainWindow, Ui_DialogVoucherList):
    """
    A main window class that handles the display and filtering of vouchers in a table view.
    It allows for dynamic filtering based on text input and visible table columns.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.all_vouchers = None

        # Define table headers
        self.headers = [
            self.tr("Voucher ID"), self.tr("Amount"), self.tr("Amount (Available)"), self.tr("Valid Until"), self.tr("Creator"),
            self.tr("Organization"), self.tr("Address"), self.tr("Gender"), self.tr("Service Offer"),
            self.tr("Region"), self.tr("Coordinates"), self.tr("Email"), self.tr("Phone"),
            self.tr("Creation Date"), self.tr("Test Voucher"), self.tr("Guarantors"),
            self.tr("Creator's Signature"), self.tr("Transactions")
        ]
        self.voucher_mapping = {}
        self.isTableViewConnected = False

        # Setup context menu for table headers
        # context menü
        self.tableView_vouchers.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_vouchers.horizontalHeader().customContextMenuRequested.connect(self.openContextMenu)
        self.pushButton_open_voucher_or_signature.clicked.connect(open_data_file)

        # Initialize the base model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.headers)

        self.base_proxy_model = CustomSortFilterProxyModel()
        self.base_proxy_model.setSourceModel(self.model)
        self.base_proxy_model.setDynamicSortFilter(True)

        # Set the top proxy model for the TableView
        self.tableView_vouchers.setModel(self.base_proxy_model)
        self.tableView_vouchers.setSortingEnabled(True)

        self.add_filter()
        self.lineEditFilter.textChanged.connect(self.apply_filter)

    def get_visible_columns(self):
        """
        Returns a list of indexes of columns that are currently visible in the table view.
        """
        visible_columns = []
        for i in range(self.model.columnCount()):
            if not self.tableView_vouchers.isColumnHidden(i):
                visible_columns.append(i)
        return visible_columns

    def apply_filter(self):
        """
        Applies the filter based on the text in the filter input and the visible columns.
        """
        filter_text = self.lineEditFilter.text().lower()
        visible_columns = self.get_visible_columns()

        # Set the visible columns and filter text in the proxy model
        self.base_proxy_model.set_visible_columns(visible_columns)
        self.base_proxy_model.set_filter_text(filter_text)

        # Set the proxy model as the model for the TableView
        self.tableView_vouchers.setModel(self.base_proxy_model)

        # Refresh the view
        self.init_values()

    def add_filter(self):
        """
        Adds filters to select which vouchers to display.
        Initializes checkboxes for each voucher status, with the ability to exclude certain statuses
        and set default checked statuses.
        """
        # Translation dictionary for voucher statuses
        status_translation = {
            VoucherStatus.UNFINISHED.value: self.tr("Unfinished"),
            VoucherStatus.ARCHIVED.value: self.tr("Archived"),
            VoucherStatus.OWN.value: self.tr("Own"),
            VoucherStatus.OTHER.value: self.tr("Other"),
            VoucherStatus.TRASHED.value: self.tr("Trashed"),
            VoucherStatus.CORRUPT.value: self.tr("Corrupt")
        }

        # Statuses to be excluded from display
        exclude_status = {VoucherStatus.TEMP.value}

        # Statuses to be checked by default
        default_checked = {VoucherStatus.OWN.value, VoucherStatus.OTHER.value, VoucherStatus.UNFINISHED.value}

        self.status_text_to_enum = {status.value: status for status in VoucherStatus if
                                    status.value not in exclude_status}
        self.translated_text_to_enum = {v: k for k, v in status_translation.items()}  # Reverse mapping

        # Add CheckBox items for each VoucherStatus
        for status in VoucherStatus:
            if status.value in exclude_status:
                continue  # Skip statuses that should not be displayed

            translated_status = status_translation.get(status.value, status.value.replace('_', ' ').capitalize())
            item = QStandardItem(translated_status)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)

            # Set the checkbox to checked if it's in the default_checked set
            check_state = Qt.CheckState.Checked if status.value in default_checked else Qt.CheckState.Unchecked
            item.setData(check_state, Qt.ItemDataRole.CheckStateRole)

            self.statusComboBox.model().appendRow(item)

        # Connect the itemChanged signal for all items
        self.statusComboBox.model().itemChanged.connect(self.init_values)

    def init_values(self):
        """
        Initializes the values in the table view based on the selected filters.
        """
        self.setWindowTitle(f"eMinuto-Liste - Profil: {user_profile.profile_name}")

        self.model.removeRows(0, self.model.rowCount())

        # Fetch vouchers based on the selected status
        self.all_vouchers = []
        for index in range(self.statusComboBox.model().rowCount()):
            item = self.statusComboBox.model().item(index)
            translated_status_text = item.text()

            # Get the English key from the translation dictionary
            english_status_key = self.translated_text_to_enum.get(translated_status_text)

            # Get the VoucherStatus Enum object from the English key
            status_enum = self.status_text_to_enum.get(english_status_key)

            if status_enum and item.checkState() == Qt.CheckState.Checked:
                self.all_vouchers += user_profile.person.voucherlist[status_enum.value]

        for i, voucher in enumerate(self.all_vouchers):
            self.add_voucher_to_model(self.model, voucher)
            self.voucher_mapping[i] = voucher

        self.tableView_vouchers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_vouchers.customContextMenuRequested.connect(self.openContextMenu)
        if not self.isTableViewConnected:
            self.tableView_vouchers.doubleClicked.connect(self.on_table_view_clicked)
            self.isTableViewConnected = True

    def add_voucher_to_model(self, model, voucher):
        """
        Adds a voucher to the table model.
        :param model: The table model to which the voucher will be added.
        :param voucher: The voucher object to add.
        """
        gender_text = {0: self.tr("Unknown"), 1: self.tr("Male"),2: self.tr("Female")}.get(voucher.creator_gender, self.tr("Unknown"))
        test_voucher_text = self.tr("Yes") if voucher.is_test_voucher else self.tr("No")
        creator_signature_text = self.tr("Yes") if voucher.creator_signature else self.tr("No")

        available_balance = format_table_cell(
            (voucher.get_voucher_amount(user_profile.person.id))
        )

        row = [
            format_table_cell(voucher.voucher_id),
            format_table_cell(float(voucher.amount)),
            available_balance,
            format_table_cell(voucher.valid_until),
            format_table_cell(f"{voucher.creator_first_name} {voucher.creator_last_name}"),
            format_table_cell(voucher.creator_organization),
            format_table_cell(voucher.creator_address),
            format_table_cell(gender_text),
            format_table_cell(voucher.service_offer),
            format_table_cell(voucher.region),
            format_table_cell(voucher.coordinates),
            format_table_cell(voucher.email),
            format_table_cell(voucher.phone),
            format_table_cell(voucher.creation_date),
            format_table_cell(test_voucher_text),
            format_table_cell(str(len(voucher.guarantor_signatures))),
            format_table_cell(creator_signature_text),
            format_table_cell(str(len(voucher.transactions)))
        ]
        model.appendRow(row)


    def openContextMenu(self, position):
        """
        Opens a context menu at the header position if the click is a right-click.
        :param position: The position where the context menu will be opened.
        """
        # Überprüfen, ob der Klick ein Rechtsklick war
        if QApplication.mouseButtons() == Qt.RightButton:
            menu = QMenu()
            for i, header in enumerate(self.headers):
                action = QAction(header, menu)
                action.setCheckable(True)
                action.setChecked(not self.tableView_vouchers.isColumnHidden(i))
                action.setData(i)
                action.toggled.connect(self.toggleColumnVisibility)
                menu.addAction(action)
            menu.exec_(self.tableView_vouchers.horizontalHeader().viewport().mapToGlobal(position))

    def toggleColumnVisibility(self, visible):
        """
        Toggles the visibility of a column.
        :param visible: A boolean indicating the desired visibility state.
        """
        column = self.sender().data()
        if visible:
            self.tableView_vouchers.showColumn(column)
        else:
            self.tableView_vouchers.hideColumn(column)

    def on_table_view_clicked(self, index):
        """
        Handles a double-click event on the table view.
        :param index: The index of the clicked table cell.
        """
        mapped_index = self.base_proxy_model.mapToSource(index)
        row = mapped_index.row()
        voucher = self.voucher_mapping[row]
        win['form_show_voucher'].show_voucher(voucher)

    def init_show(self):
        """
        Initializes and shows the main window.
        """
        self.init_values()
        self.show()
        self.raise_()


class DialogTransactionList(QMainWindow, Ui_DialogTransactionList):
    """
    A main window class that handles the display and filtering of transactions in a table view.
    It allows for dynamic filtering based on text input and visible table columns.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # This method needs to be defined elsewhere, typically setup by Qt Designer UI files.
        self.headers = []
        self.column_translations = {
            'id': self.tr("Transaction ID"),
            'sender': self.tr("Sender"),
            'recipient': self.tr("Recipient"),
            'amount': self.tr("Amount"),
            'purpose': self.tr("Purpose"),
            'time': self.tr("Time")
        }
        self.transaction_mapping = {}
        self.isTableViewConnected = False
        
        # Setup context menu for table headers
        self.tableView_transactions.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_transactions.horizontalHeader().customContextMenuRequested.connect(self.openContextMenu)

        # Initialize the base model
        self.model = QStandardItemModel()
        #self.model.setHorizontalHeaderLabels(self.headers)

        self.base_proxy_model = CustomSortFilterProxyModel()  # This needs to be defined
        self.base_proxy_model.setSourceModel(self.model)
        self.base_proxy_model.setDynamicSortFilter(True)

        # Set the top proxy model for the TableView
        self.tableView_transactions.setModel(self.base_proxy_model)
        self.tableView_transactions.setSortingEnabled(True)

        self.add_filter()
        self.lineEditFilter.textChanged.connect(self.apply_filter)

        self.init_values()  # Populate the table with transactions

    def get_visible_columns(self):
        """
        Returns a list of indexes of columns that are currently visible in the table view.
        """
        visible_columns = []
        for i in range(self.model.columnCount()):
            if not self.tableView_transactions.isColumnHidden(i):
                visible_columns.append(i)
        return visible_columns

    def apply_filter(self):
        """
        Applies the filter based on the text in the filter input and the visible columns.
        """
        filter_text = self.lineEditFilter.text().lower()
        self.base_proxy_model.set_filter_text(filter_text)
        self.base_proxy_model.set_visible_columns(self.get_visible_columns())
        self.tableView_transactions.setModel(self.base_proxy_model)

    def add_filter(self):
        """
        Adjusted to handle transaction filtering for incoming and outgoing transactions.
        """
        # Simplify for the example; in real implementation, you would dynamically create these based on actual data
        self.statusComboBox.addItem(self.tr("All Transactions"))
        self.statusComboBox.addItem(self.tr("Incoming"))
        self.statusComboBox.addItem(self.tr("Outgoing"))

        # Connect comboBox changes to filter application or data reloading
        self.statusComboBox.currentIndexChanged.connect(self.init_values)

    def init_values(self):
        """
        Initializes the values in the table view based on the selected filter and transactions.
        This implementation uses the index of the selection in the statusComboBox to determine
        the filter to be applied, making it independent of the actual text, which is useful for localization.
        """
        self.setWindowTitle(self.tr("Transaction - Profile: %s") % user_profile.profile_name)

        self.model.clear()  # Clear existing items from the table model.

        # Determine the current filter based on the index of the selection in the statusComboBox.
        current_filter_index = self.statusComboBox.currentIndex()

        filtered_transactions = []
        for transaction_id, transaction_details in user_profile.transactions.items():
            if current_filter_index == 0:  # Index 0 corresponds to "All Transactions".
                filtered_transactions.append((transaction_id, transaction_details))
            elif current_filter_index == 1:  # Index 1 corresponds to "Incoming Transactions".
                if transaction_details['recipient'] == user_profile.person.id:
                    filtered_transactions.append((transaction_id, transaction_details))
            elif current_filter_index == 2:  # Index 2 corresponds to "Outgoing Transactions".
                if transaction_details['sender'] == user_profile.person.id:
                    filtered_transactions.append((transaction_id, transaction_details))

        # If there are any transactions to display, set up the table headers based on the keys of the first transaction
        # and exclude 'transaction_object' from being displayed.
        if filtered_transactions:
            first_transaction = filtered_transactions[0][1]
            headers_keys = [key for key in first_transaction.keys() if key != 'transaction_object']
            self.headers = [self.column_translations.get(key, key) for key in headers_keys]
            self.model.setHorizontalHeaderLabels(self.headers)

        # Clearing the transaction mapping to ensure it's in sync with the currently displayed transactions.
        self.transaction_mapping.clear()

        # Populate the table with filtered transactions.
        for transaction_id, transaction_details in filtered_transactions:
            self.add_transaction_to_model(self.model, transaction_details)
            # Update the transaction mapping for each transaction using its row index.
            self.transaction_mapping[
                self.model.indexFromItem(self.model.item(self.model.rowCount() - 1, 0)).row()] = transaction_id

        # Apply the filter settings.
        self.apply_filter()

        # Set the updated model to the tableView_transactions.
        self.tableView_transactions.setModel(self.base_proxy_model)
        self.tableView_transactions.setSortingEnabled(True)

        # Connect signals for handling table view interactions, ensuring they are only connected once.
        if not self.isTableViewConnected:
            self.tableView_transactions.doubleClicked.connect(self.on_table_view_clicked)
            self.isTableViewConnected = True

    def add_transaction_to_model(self, model, transaction):
        """
        Adds a transaction to the table model.
        :param model: The table model to which the transaction will be added.
        :param transaction: The transaction object to add.
        """
        amount = float(transaction['amount'])
        if transaction['recipient'] != user_profile.person.id:
            amount *= -1
        row = [
            format_table_cell(transaction['id']),
            format_table_cell(transaction['sender']),
            format_table_cell(transaction['recipient']),
            format_table_cell(amount, color=True),
            format_table_cell(transaction['purpose']),
            format_table_cell(transaction['time']),
        ]
        model.appendRow(row)


    def openContextMenu(self, position):
        """
        Opens a context menu at the header position if the click is a right-click.
        :param position: The position where the context menu will be opened.
        """
        # Überprüfen, ob der Klick ein Rechtsklick war
        if QApplication.mouseButtons() == Qt.RightButton:
            menu = QMenu()
            for i, header in enumerate(self.headers):
                action = QAction(header, menu)
                action.setCheckable(True)
                action.setChecked(not self.tableView_transactions.isColumnHidden(i))
                action.setData(i)
                action.toggled.connect(self.toggleColumnVisibility)
                menu.addAction(action)
            menu.exec_(self.tableView_transactions.horizontalHeader().viewport().mapToGlobal(position))

    def toggleColumnVisibility(self, visible):
        """
        Toggles the visibility of a column.
        :param visible: A boolean indicating the desired visibility state.
        """
        column = self.sender().data()
        if visible:
            self.tableView_transactions.showColumn(column)
        else:
            self.tableView_transactions.hideColumn(column)

    def on_table_view_clicked(self, index):
        source_index = self.base_proxy_model.mapToSource(index)
        if source_index.isValid():
            row = source_index.row()
            # Using the transaction_mapping to get the transaction_id
            transaction_id = self.transaction_mapping.get(row)
            if transaction_id:
                # Access the transaction details directly from user_profile.transactions
                transaction = user_profile.transactions.get(transaction_id)
                transaction = transaction['transaction_object']
                if transaction:
                    win['form_show_transaction'].show_transaction(transaction)

    def init_show(self):
        """
        Initializes and shows the main window.
        """
        self.init_values()
        self.show()
        self.raise_()


TRANSLATION_DIR = 'src/gui/qt/translation'
MAIN_DIR = '.'  # Main directory where the program is run
DEFAULT_LANG = 'English'
QM_FILE_NAME = 'current_lang.qm'

# Mapping for language codes to full language names in their respective languages
LANGUAGE_NAMES = {
    "de_DE": "Deutsch",
    "fr_FR": "Français",
    "es_ES": "Español",
    # Add more language mappings as needed
}


class Frm_Mainwin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialize language menu
        self.create_language_menu()

        # Load profile windows - connect signals
        self.dialog_generate_profile = Dialog_Generate_Profile()
        self.dialog_generate_profile.profileCreated.connect(self.onProfileCreated)
        self.dialog_profile_login = Dialog_Profile_Login()
        self.dialog_profile_login.profileLogin.connect(self.profile_login)
        self.dialog_profile_login.overwritePassword.connect(self.forgot_password)
        self.dialog_profile = Dialog_Profile()
        self.dialog_profile.frm_main_window_update_values.connect(self.update_values)
        self.dialog_profile_create_selection = Dialog_Profile_Create_Selection()
        self.dialog_profile_create_selection.frm_main_window_generate_profile.connect(self.dialog_generate_profile.show)

        self.setWindowTitle(f"eMinuto v{get_version()}")

        # Menu actions
        self.actionCreateProfile.triggered.connect(self.dialog_generate_profile.show)
        self.actionEditProfile.triggered.connect(self.dialog_profile.init_and_show)
        self.actionCreateMinuto.triggered.connect(win['dialog_create_minuto'].show)
        self.actionProfileLogin.triggered.connect(self.dialog_profile_login.login)
        self.actionProfileLogout.triggered.connect(self.profile_logout)
        self.actionVoucherList.triggered.connect(win['dialog_voucher_list'].init_show)
        self.actionTransactions.triggered.connect(win['dialog_transaction_list'].init_show)
        self.actionOpenFile.triggered.connect(open_data_file)

        self.actionClose.triggered.connect(self.close)
        self.set_gui_depending_profile_status()

        # Buttons
        self.pushButton_copy_user_ID.clicked.connect(self.copyUserIDToClipboard)
        self.pushButton_send_minuto.clicked.connect(self.sendMinuto)
        self.pushButton_receive_minuto.clicked.connect(self.receiveMinutoTransaction)
        self.pushButton_show_transactions.clicked.connect(win['dialog_transaction_list'].init_show)
        self.pushButton_show_vouchers.clicked.connect(win['dialog_voucher_list'].init_show)

    def show(self):
        super().show()
        if user_profile.profile_exists():
            self.dialog_profile_login.show()
        else:
            self.dialog_profile_create_selection.show()

    def create_language_menu(self):
        language_menu = self.menuLanguage
        language_menu.clear()  # Clear existing actions to avoid duplication
        qm_files = [f for f in os.listdir(TRANSLATION_DIR) if f.endswith('.qm')]

        # Add default English language option
        default_action = QAction(DEFAULT_LANG, self, checkable=True)
        default_action.triggered.connect(functools.partial(self.change_language, DEFAULT_LANG))
        language_menu.addAction(default_action)

        current_language = None
        if os.path.exists(os.path.join(MAIN_DIR, 'mdata')):
            for file in os.listdir(os.path.join(MAIN_DIR, 'mdata')):
                if file.endswith('.qm'):
                    current_language = file.replace('.qm', '')

        if current_language is None:
            default_action.setChecked(True)

        for qm_file in qm_files:
            lang_code = qm_file.replace('.qm', '')
            full_language_name = LANGUAGE_NAMES.get(lang_code, lang_code)
            action = QAction(full_language_name, self, checkable=True)
            action.triggered.connect(functools.partial(self.change_language, lang_code))
            language_menu.addAction(action)
            if current_language and lang_code == current_language:
                action.setChecked(True)

    def change_language(self, lang_code, checked=True):
        qm_file_path = os.path.join(TRANSLATION_DIR, f"{lang_code}.qm")
        dest_qm_dir = os.path.join(MAIN_DIR, 'mdata')
        os.makedirs(dest_qm_dir, exist_ok=True)

        # Remove all existing .qm files in the mdata directory
        for file in os.listdir(dest_qm_dir):
            if file.endswith('.qm'):
                os.remove(os.path.join(dest_qm_dir, file))

        dest_qm_file = os.path.join(dest_qm_dir, f"{lang_code}.qm")

        if lang_code == DEFAULT_LANG:
            if os.path.exists(dest_qm_file):
                os.remove(dest_qm_file)
        else:
            if os.path.exists(qm_file_path):
                # Copy file content without shutil
                with open(qm_file_path, 'rb') as src_file:
                    with open(dest_qm_file, 'wb') as dst_file:
                        dst_file.write(src_file.read())

        show_message_box(self.tr("Notice"), self.tr("Please restart the application to apply the new language settings."))


    def closeEvent(self, event):
        # Close all windows on close of main win
        for window in win.values():
            window.close()

        # Beenden der Anwendung
        QApplication.instance().quit()

        super().closeEvent(event)

    def forgot_password(self):
        win['dialog_forgot_password'].show()

    def sendMinuto(self):
        win['form_send_minuto'].show_init()

    def receiveMinutoTransaction(self):
        open_data_file(file_type="transaction")

    def copyUserIDToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(user_profile.person.id)

    def onProfileCreated(self):
        self.profile_logout()
        self.dialog_profile_login.show()

    def update_values(self):
        self.setWindowTitle(
            self.tr("eMinuto v%s - Profile: %s - ID: %s") % (get_version(), user_profile.profile_name, user_profile.person.id[:8]))
        self.set_vouchers_balances()
        self.lineEdit_user_id.setText(f"{user_profile.person.id}")
        self.lineEdit_user_id.setCursorPosition(0)
        self.label_username.setText(f"{user_profile.person_data['first_name']} {user_profile.person_data['last_name']}")

    def profile_login(self):
        self.update_values()
        self.set_gui_depending_profile_status()
        self.show_status_message(self.tr("Successfully logged in."))

    def profile_logout(self):
        user_profile.profile_logout()
        self.update_values()
        self.set_gui_depending_profile_status()
        self.show_status_message(self.tr("Successfully logged out."))

    def on_enter(self):
        """Update the screen when entering."""
        self.title = self.get_title()
        self.set_vouchers_balances()

    def get_title(self):
        """Get the user's full name for the title."""
        name = user_profile.person_data['first_name']
        surname = user_profile.person_data['last_name']
        return f"{name} {surname}"

    def set_vouchers_balances(self):
        """Demo function set balance of vouchers."""
        self.lineEdit_own_balance.setText(user_profile.get_minuto_balance(VoucherStatus.OWN.value))
        self.lineEdit_other_balance.setText(user_profile.get_minuto_balance(VoucherStatus.OTHER.value))

    def set_gui_depending_profile_status(self):
        """Changes the GUI depending on whether the profile exists and is active or inactive."""

        profile_exists = user_profile.profile_exists()
        profile_initialized = user_profile.profile_initialized()

        def hide(object):  # helper
            object.setVisible(False)

        def show(object):
            object.setVisible(True)

        def disable(object):
            object.setEnabled(False)

        def enable(object):
            object.setEnabled(True)

        # Changings of GUI
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
            self.lineEdit_user_id.setText("")
            self.lineEdit_own_balance.setText("0")
            self.lineEdit_other_balance.setText("0")
            show(self.actionProfileLogin)

            hide(self.actionEditProfile)
            hide(self.actionProfileLogout)
            hide(self.actionCreateProfile)
            hide(self.actionCreateMinuto)
            hide(self.actionVoucherList)

            disable(self.lineEdit_own_balance)
            disable(self.lineEdit_other_balance)

        if not profile_exists:
            show(self.actionCreateProfile)

            hide(self.actionEditProfile)
            hide(self.actionProfileLogout)
            hide(self.actionProfileLogin)
            hide(self.actionCreateMinuto)
            hide(self.actionVoucherList)

            disable(self.lineEdit_own_balance)
            disable(self.lineEdit_other_balance)

    def show_status_message(self, message):
        self.statusBar().showMessage(message, 5000)  # 5 seconds timeout


app = QApplication([])
apply_global_styles(app)

# Load translation file if available
translator = QTranslator()
qm_file = None
if os.path.exists(os.path.join(MAIN_DIR, 'mdata')):
    for file in os.listdir(os.path.join(MAIN_DIR, 'mdata')):
        if file.endswith('.qm'):
            qm_file = os.path.join(MAIN_DIR, 'mdata', file)
            break

if qm_file and translator.load(qm_file):
    app.installTranslator(translator)



# Dictionary of all windows
win = {
    'form_send_minuto': FormSendMinuto(),
    'form_sign_as_guarantor': FormSignAsGuarantor(),
    'form_send_to_guarantor': FormSendToGuarantor(),
    'form_show_raw_data': FormShowRawData(),
    'dialog_create_minuto': Dialog_Create_Minuto(),
    'dialog_voucher_list': DialogVoucherList(),
    'dialog_transaction_list': DialogTransactionList(),
    'dialog_forgot_password': DialogForgotPassword(),
    'form_show_voucher': FormShowVoucher(),
    'form_show_transaction': FormShowTransaction()
}

frm_main_window = Frm_Mainwin()
frm_main_window.show()

sys.exit(app.exec())
