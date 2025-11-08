@echo off
echo ====================================================
echo Tata Dealer Incoming Call Management System Setup
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo [4/6] Creating database migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo Error creating migrations
    pause
    exit /b 1
)

echo [5/6] Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo Error running migrations
    pause
    exit /b 1
)

echo [6/6] Creating sample dispositions...
python manage.py shell < create_dispositions.py

echo.
echo ====================================================
echo Setup completed successfully!
echo ====================================================
echo.
echo Next steps:
echo 1. Create admin user: python manage.py createsuperuser
echo 2. Start server: python manage.py runserver
echo 3. Test webhook: python test_webhook.py
echo.
echo Webhook URL: http://127.0.0.1:8000/api/webhook/
echo Admin Panel: http://127.0.0.1:8000/admin/
echo API: http://127.0.0.1:8000/api/calls/
echo.
pause
