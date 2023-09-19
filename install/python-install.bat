@echo off

setlocal enabledelayedexpansion

:: Set the Python version to install
set PYTHON_VERSION=3.9.7

:: Set the installation directory (adjust this path as needed)
set INSTALL_DIR=C:\Python

:: URL for downloading the Python installer
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

:: Download and install Python
echo Downloading Python %PYTHON_VERSION%...
curl -o python_installer.exe %PYTHON_URL%
if errorlevel 1 (
    echo Failed to download Python installer.
    exit /b 1
)

echo Installing Python %PYTHON_VERSION%...
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if errorlevel 1 (
    echo Failed to install Python.
    exit /b 1
)

:: Cleanup
del python_installer.exe

:: Display installation success message
echo Python %PYTHON_VERSION% has been installed to %INSTALL_DIR%
exit /b 0
