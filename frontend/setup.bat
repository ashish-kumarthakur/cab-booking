@echo off
REM Cab Booking Frontend Setup Script for Windows

echo Setting up Cab Booking Frontend...

REM Install dependencies
echo Installing dependencies...
call npm install

REM Create .env.local file if it doesn't exist
if not exist .env.local (
    echo Creating .env.local file from .env.example...
    copy .env.example .env.local
    echo Please edit .env.local file with your configuration
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env.local file with your configuration
echo 2. Run: npm run dev

pause


