import sys
import subprocess
import os

def build_executable():
    """
    Erstellt eine ausführbare Datei für das Projekt mit PyInstaller unter Verwendung der main.spec-Datei.
    """

    # Pfad zur main.spec-Datei
    spec_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.spec")

    # Build-Befehl
    build_command = ["pyinstaller", spec_path]

    print("Erstelle eine ausführbare Datei unter Verwendung der main.spec-Datei...")
    subprocess.run(build_command)

if __name__ == "__main__":
    build_executable()
