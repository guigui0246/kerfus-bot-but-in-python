@echo off

where python > nul 2>&1
if %errorlevel% equ 0 (
    echo Python is installed.
) else (
    echo Python is not installed.
    echo Installing Python.
    call python_install.bat
    echo Python installed.
)

python -m ensurepip --upgrade

pip install discord
pip install datetime
pip install asyncio
pip install typing
