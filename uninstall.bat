@echo off
reg delete "HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v "Shell" /f
echo.
echo Uninstalled successfully.
set /p DUMMY="Press Enter to close..."