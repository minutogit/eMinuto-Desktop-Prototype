import os
import subprocess


def update_qm_files():
    """
    Checks all .ts files in the current directory and creates or updates the corresponding
    .qm files if they do not exist or are older than the .ts files.
    """
    # Get the list of all .ts files in the current directory
    ts_files = [f for f in os.listdir('.') if f.endswith('.ts')]

    for ts_file in ts_files:
        qm_file = ts_file.replace('.ts', '.qm')

        # Check if the QM file exists and if it needs to be updated
        ts_mtime = os.path.getmtime(ts_file)
        if not os.path.exists(qm_file):
            # Run lrelease to create the QM file
            subprocess.run(['lrelease', ts_file, '-qm', qm_file])
        elif os.path.getmtime(qm_file) < ts_mtime:
            # Run lrelease to update the QM file
            subprocess.run(['lrelease', ts_file, '-qm', qm_file])


if __name__ == "__main__":
    """
    This script must be run in the directory containing the .ts files.
    It checks if .qm files are present or if the .ts files are newer than the .qm files.
    If a .qm file is missing or needs to be updated, it will be created or updated using lrelease.
    Run this script to generate or update the .qm files.
    """
    update_qm_files()
