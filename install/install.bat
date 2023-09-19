@echo off

where python > nul 2>&1
if %errorlevel% equ 0 (
    echo Python is installed.
) else (
    echo Python is not installed.
    echo Installing Python.
    call python_install.bat
    where python > nul 2>&1
    if %errorlevel% equ 0 (
        echo Python installed.
    ) else (
        echo Failed to install Python
        exit -1
    )
)

python -m ensurepip --upgrade

pip install discord
pip install datetime
pip install asyncio
pip install typing
