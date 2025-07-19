@echo off
echo ========================================
echo Voice Assistant Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Create virtual environment (optional but recommended)
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Warning: Could not create virtual environment
    echo Continuing with system Python...
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install PyAudio first (special handling for Windows)
echo Installing PyAudio (this may take a moment)...
pip install pipwin
pipwin install pyaudio
if errorlevel 1 (
    echo Warning: pipwin method failed, trying direct pip install...
    pip install pyaudio
)
echo.

REM Install other requirements
echo Installing other requirements...
pip install -r requirements.txt
echo.

REM Check .env file
if exist .env (
    echo .env file found
    findstr /C:"your_openai_api_key_here" .env >nul
    if not errorlevel 1 (
        echo.
        echo WARNING: Please edit .env file and add your actual OpenAI API key
        echo The file currently contains placeholder text.
        echo.
    )
) else (
    echo WARNING: .env file not found
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: python test_components.py (to test everything)
echo 3. Run: python voice_assistant.py (to start the assistant)
echo.
echo Press any key to exit...
pause >nul
