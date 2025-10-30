@echo off
echo ============================================================
echo   STARTING FRONTEND SERVER
echo ============================================================
echo.

cd /d "%~dp0frontend"

echo Starting React development server...
echo Browser will open automatically at http://localhost:3000
echo.
npm start

pause
