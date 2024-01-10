# main.py
from src.models.user_profile import user_profile

from PySide6.QtWidgets import QApplication
import src.gui.qt.qt_main as qt_main
from src.gui.qt.qt_main import app

def main():

    qt_main.frm_main_window.show()
    if user_profile.profile_exists():
        qt_main.dialog_profile_login.show()
    else:
        qt_main.dialog_profile_create_selection.show()

    app.exec()


if __name__ == "__main__":
    main()
