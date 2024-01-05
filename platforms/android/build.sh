#!/bin/bash

# Relative path to the venv's activate script
VENV_ACTIVATE_PATH="../../venv/bin/activate"

# Navigate to the script directory
cd "$(dirname "$0")"
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Die virtuelle Umgebung ist aktiv."
else
    echo "Die virtuelle Umgebung ist nicht aktiv."
fi
pip list | wc -l
# Activate the virtual environment
source "$VENV_ACTIVATE_PATH"

if [ -n "$VIRTUAL_ENV" ]; then
    echo "Die virtuelle Umgebung ist aktiv."
else
    echo "Die virtuelle Umgebung ist nicht aktiv."
fi

pip list | wc -l

# Check the passed argument
if [ "$1" == "release" ]; then
    echo "Building Release APK..."
    #buildozer -v android release
else
    echo "Building Debug APK..."
    #buildozer -v android debug
fi

