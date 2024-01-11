# run this script to convert all *.ui in this folder to py
# pyside6-uic wurde nicht in der venv gefunde obwohl installiert. wenn pip3 install pyside6 dann ist es unter den bins dabei.
# workaround: normal im system installieren und absouten pfad der anwendung nehmen: /home/basti/.local/bin/pyside6-uic

import os
import time
import warnings


def convert_ui_to_py():
    print("Convert ui to py\n")
    dirname = os.path.dirname(__file__)

    directory = os.listdir(dirname)
    counter = 0
    skipped_counter = 0
    for file in directory:
        if not file.endswith(".ui"):
            continue
        if len(file.split(".")) > 2:
            warnings.warn(file + ' not converted. Filename contains a dot!')
            #continue

        py_file_name = file.split(".")[0] + '.py'
        cmd_command = ('/home/basti/.local/bin/pyside6-uic ' + file + ' -o ' + py_file_name)

        if os.path.isfile(py_file_name): # file exists -> check if ui updated (modified date)
            if os.path.getmtime(file) <= os.path.getmtime(py_file_name): # ui is not updated, older modified date
                skipped_counter += 1
                continue # don't convert

        print(f"Convert {file} to {py_file_name} !!!\n")
        os.system(cmd_command)
        counter += 1
    print(f"{counter} files converted.  ({skipped_counter} unchanged files skipped)")

convert_ui_to_py()