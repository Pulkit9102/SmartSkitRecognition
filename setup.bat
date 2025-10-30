@echo off
REM Complete Setup Script for Skin Disease Recognition System

echo ================================================================
echo  Skin Disease Recognition System - Complete Setup
echo ================================================================
echo.

echo This script will help you set up the entire project.
echo.
echo Steps:
echo   1. Set up backend (Python)
echo   2. Set up frontend (React)
echo   3. Create sample dataset structure
echo.
pause

REM ===== BACKEND SETUP =====
echo.
echo ================================================================
echo  STEP 1: Backend Setup
echo ================================================================
echo.

cd backend

echo [1/4] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    echo Please ensure Python 3.8+ is installed
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo [INFO] .env file created. Please add your SERP_API_KEY later.
)

echo.
echo [SUCCESS] Backend setup complete!
echo.

cd ..

REM ===== FRONTEND SETUP =====
echo.
echo ================================================================
echo  STEP 2: Frontend Setup
echo ================================================================
echo.

cd frontend

echo [1/2] Installing Node dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Please ensure Node.js 14+ is installed
    pause
    exit /b 1
)

echo [2/2] Creating .env file...
if not exist ".env" (
    copy .env.example .env
)

echo.
echo [SUCCESS] Frontend setup complete!
echo.

cd ..

REM ===== DATASET SETUP =====
echo.
echo ================================================================
echo  STEP 3: Dataset Setup
echo ================================================================
echo.

cd model

echo Would you like to create sample dataset structure? (y/n)
set /p create_dataset="Enter choice: "

if /i "%create_dataset%"=="y" (
    echo Creating sample dataset structure...
    python create_sample_dataset.py
)

cd ..

REM ===== FINAL INSTRUCTIONS =====
echo.
echo ================================================================
echo  Setup Complete!
echo ================================================================
echo.
echo Next steps:
echo.
echo 1. Get SerpAPI Key (optional but recommended):
echo    - Visit: https://serpapi.com/
echo    - Sign up for free account
echo    - Copy your API key
echo    - Edit backend\.env and add: SERP_API_KEY=your_key_here
echo.
echo 2. Add training images:
echo    - Place images in dataset\train\[disease_name]\
echo    - Place images in dataset\validation\[disease_name]\
echo    - Minimum 50 images per disease
echo.
echo 3. Train the model:
echo    - cd model
echo    - python train_model.py
echo.
echo 4. Start the application:
echo    - Terminal 1: cd backend ^&^& start_backend.bat
echo    - Terminal 2: cd frontend ^&^& start_frontend.bat
echo.
echo ================================================================
echo  Documentation
echo ================================================================
echo.
echo - README.md           - Complete guide
echo - QUICKSTART.md       - Quick setup guide
echo - SETUP_CHECKLIST.md  - Step-by-step checklist
echo - PROJECT_SUMMARY.md  - Project overview
echo.
echo ================================================================
echo.

pause
