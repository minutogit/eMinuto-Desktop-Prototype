# main.py
import argparse
from src import config
from src.models.user_profile import user_profile
import src.gui.qt.qt_main as qt_main
from src.gui.qt.qt_main import app

def main():
    # Setting up argparse to accept command line arguments
    parser = argparse.ArgumentParser(description="Start the application.")
    # Adding the --test-mode argument
    parser.add_argument("--test-mode", action="store_true", help="Activate test mode")
    # Parsing the arguments
    args = parser.parse_args()

    # Checking if the --test-mode argument was used
    if args.test_mode:
        config.TEST_MODE = True
        print("Test Mode Activated")

    # Application's main logic
    qt_main.frm_main_window.show()
    if user_profile.profile_exists():
        qt_main.win['dialog_profile_login'].show()
    else:
        qt_main.win['dialog_profile_create_selection'].show()

    app.exec()

if __name__ == "__main__":
    main()
