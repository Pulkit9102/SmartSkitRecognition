@echo off
echo ============================================================
echo   STARTING BACKEND SERVER
echo ============================================================
echo.

cd /d "%~dp0backend"
call venv\Scripts\activate.bat

echo Starting Flask API...
python app_simple.py

pause
