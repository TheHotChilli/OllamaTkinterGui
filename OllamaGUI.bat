@echo off

REM set your python path
set "PYTHON_PATH=C:\Program Files\Python311\pythonw.exe"

REM check if path exists
if not exist "%PYTHON_PATH%" (
    echo Python Installation nicht gefunden.
    exit /b 1
)

REM start gui
@REM python ./ChatApp.py
start "" "%PYTHON_PATH%" "%~dp0\ChatApp.py"