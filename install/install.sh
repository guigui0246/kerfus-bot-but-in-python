#!/bin/bash

if which python3 > /dev/null 2>&1; then
    echo "Python is installed."
else
    echo "Python is not installed."
    echo "Installing Python."
    bash ./python_install.sh
    echo "Python installed."
fi

python -m ensurepip --upgrade

pip install discord
pip install datetime
pip install asyncio
pip install typing
