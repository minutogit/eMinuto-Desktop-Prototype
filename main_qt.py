# main.py
from PySide6.QtWidgets import QApplication
import src.gui.qt.qt_main as qt_main


def main():
    app = QApplication([])

    frm_main_window = qt_main.Frm_Mainwin()
    frm_main_window.show()
    #frm_main_window.profile_login()

    # Starten der Qt-Anwendung
    app.exec()


if __name__ == "__main__":
    main()
