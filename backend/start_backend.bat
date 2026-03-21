@echo off
REM Skin Disease Recognition - Backend Startup Script
REM This script starts the Flask backend server

echo ========================================
echo Starting Skin Disease Backend Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Creating from .env.example...
    copy .env.example .env
    echo.
    echo [ACTION REQUIRED] Please edit .env and add your SERP_API_KEY
    echo Get your key from: https://serpapi.com/
    echo.
)

REM Start the Flask server
echo [INFO] Starting Flask server...
echo [INFO] Backend will run on: http://localhost:5000
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python app_simple.py

pause
