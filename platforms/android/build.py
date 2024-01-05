import sys
import subprocess
import os

def build_apk(build_type='debug'):
    """
    Builds the APK for the project using buildozer.
    :param build_type: 'debug' or 'release' to specify the type of build.
    """

    # Navigate to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Build command
    if build_type == 'release':
        print("Building Release APK...")
        subprocess.run(["buildozer", "-v", "android", "release"])
    else:
        print("Building Debug APK...")
        subprocess.run(["buildozer", "-v", "android", "debug"])

if __name__ == "__main__":
    build_type = sys.argv[1] if len(sys.argv) > 1 else 'debug'
    build_apk(build_type)
