import os
import subprocess

def generate_translation_file_from_ui(output_ts_file, directory, additional_files=None):
    """
    Generates a Qt translation file (.ts) from .ui files and additional Python source files.

    :param output_ts_file: The name of the output .ts file.
    :param directory: The directory containing the .ui files to include.
    :param additional_files: A list of additional Python files to include (optional).
    """
    # Create a list of all .ui files in the specified directory
    ui_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.ui')]

    # Add any additional files provided
    if additional_files:
        ui_files.extend(additional_files)

    # Ensure all file paths are relative and exist
    ui_files = [os.path.relpath(file) for file in ui_files if os.path.exists(file)]

    # Print debug information
    print("Files to be included in translation:")
    for file in ui_files:
        print(f"  {file}")

    # Create the lupdate command
    command = ['pyside6-lupdate'] + ui_files + ['-ts', output_ts_file]

    # Run the lupdate command
    try:
        subprocess.run(command, check=True)
        print(f"Successfully created {output_ts_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating the translation file: {e}")

if __name__ == "__main__":
    # Define the directory containing the UI files
    ui_directory = 'src/gui/qt/ui_components'

    # Define any additional files to be included
    additional_files = [
        'src/gui/qt/qt_main.py',
        'src/gui/qt/profile_dialogs.py'
    ]

    # Ensure the output directory exists
    output_directory = 'src/gui/qt/translation'
    os.makedirs(output_directory, exist_ok=True)

    # Define the output translation file
    output_ts_file = os.path.join(output_directory, 'de_DE.ts')

    # Generate the translation file
    generate_translation_file_from_ui(output_ts_file, ui_directory, additional_files)
