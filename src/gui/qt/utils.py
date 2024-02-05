from PySide6.QtWidgets import QMessageBox

def show_message_box(title, text):
    dlg = QMessageBox()
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.exec()

def show_yes_no_box(title, text):
    dlg = QMessageBox()
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    dlg.setDefaultButton(QMessageBox.No)
    dlg.setIcon(QMessageBox.Question)
    result = dlg.exec()

    if result == QMessageBox.Yes:
        return True
    else:
        return False

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


# utils.py
from PySide6.QtGui import QValidator
import re


class DecimalFormatValidator(QValidator):
    """
    A singleton validator class for validating and correcting decimal input.
    Allows up to five digits before the decimal point and two digits after it.
    Accepts both dot (.) and comma (,) as decimal separators.
    """
    instance = None

    def __new__(cls):
        """Ensure only one instance of DecimalFormatValidator is created (singleton pattern)."""
        if cls.instance is None:
            cls.instance = super(DecimalFormatValidator, cls).__new__(cls)
        return cls.instance

    def validate(self, input_str, pos):
        """
        Validate the input string based on the defined decimal format.

        :param input_str: The string input to validate.
        :param pos: The position of the cursor.
        :return: Tuple of validation state (Acceptable, Intermediate, or Invalid), input string, and cursor position.
        """
        pattern = r'^\d{0,5}([.,]\d{0,2})?$'
        if re.match(pattern, input_str):
            return QValidator.Acceptable, input_str, pos
        else:
            return QValidator.Invalid, input_str, pos

    def fixup(self, input_str):
        """
        Correct the input string by replacing commas with dots.

        :param input_str: The string input to correct.
        :return: The corrected string.
        """
        return input_str.replace(',', '.')
