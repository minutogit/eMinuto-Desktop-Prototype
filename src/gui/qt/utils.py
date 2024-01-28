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