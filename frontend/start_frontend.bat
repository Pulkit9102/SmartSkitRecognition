@echo off
REM Skin Disease Recognition - Frontend Startup Script
REM This script starts the React development server

echo ========================================
echo Starting Skin Disease Frontend
echo ========================================
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
    echo [ERROR] Dependencies not installed!
    echo Please run: npm install
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo [INFO] Creating .env from .env.example...
    copy .env.example .env
    echo.
)

REM Start the development server
echo [INFO] Starting React development server...
echo [INFO] Frontend will open at: http://localhost:3000
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

npm start

pause
