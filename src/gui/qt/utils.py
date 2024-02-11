from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMessageBox

from src.services.utils import dprint


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
from PySide6.QtGui import QValidator, QStandardItem, Qt, QBrush, QFont, QColor
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

def is_iso8601_datetime(value):
    """Check if the string value is in ISO 8601 datetime format."""
    datetime_obj = QDateTime.fromString(value, Qt.ISODateWithMs)
    return datetime_obj.isValid()


def format_table_cell(value, color=False):
    """
    Creates a non-editable QStandardItem for display in a PyQt TableView.

    Args:
        value: The value to be displayed in the table cell. Can be of type string, float, int, or an ISO formatted datetime string.
        color: A boolean indicating if the value should be color-coded based on its value (applies to float types).

    Returns:
        A QStandardItem configured for display, with appropriate formatting based on the value type.
    """
    item = QStandardItem()  # Create a new QStandardItem.
    item.setEditable(False)  # Make the item non-editable.

    if isinstance(value, float):
        # Format float values to a string with 2 decimal places.
        display_text = "{:.2f}".format(value)
        item.setText(display_text)
        # Align float values to the right, making them easier to compare visually.
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        if color:  # Apply color and bold font for float values based on their magnitude.
            font = QFont()
            font.setBold(True)
            item.setFont(font)

            if value > 0:
                item.setForeground(QBrush(QColor(0, 150, 0))) # dark green
            elif value < 0:
                item.setForeground(QBrush(Qt.red))
            else:  # value == 0
                item.setForeground(QBrush(Qt.black))

    elif isinstance(value, str) and is_iso8601_datetime(value):
        # Convert ISO formatted datetime strings to a more readable format.
        datetime_obj = QDateTime.fromString(value, Qt.ISODateWithMs)
        display_text = datetime_obj.toString("yyyy-MM-dd HH:mm:ss")
        item.setText(display_text)
        # Align datetime values to the right.
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    else:
        # For other types, simply convert the value to a string.
        item.setText(str(value))
        # Integer values are also right-aligned for consistency.
        if isinstance(value, int):
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    return item  # Return the configured QStandardItem.