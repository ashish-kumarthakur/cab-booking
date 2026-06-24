@echo off
REM Cab Booking Backend Setup Script for Windows

echo Setting up Cab Booking Backend...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please edit .env file with your configuration
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Set up PostgreSQL database with PostGIS
echo 3. Start Redis server
echo 4. Run: uvicorn app.main:app --reload

pause


