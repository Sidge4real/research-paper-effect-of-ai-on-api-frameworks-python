@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

:: Create and activate virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call .\venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Start the servers in separate windows
echo Starting servers...
start "Django Server" cmd /c "call .\venv\Scripts\activate && python wsgi.py"
start "Flask Server" cmd /c "call .\venv\Scripts\activate && python flask_app.py"
start "FastAPI Server" cmd /c "call .\venv\Scripts\activate && uvicorn fastapi_app:app --host 0.0.0.0 --port 8001 --workers 4"

:: Function to check if a server is responding
echo Waiting for servers to be ready...

:check_servers
timeout /t 5 /nobreak >nul

:: Check Django server
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo Waiting for Django server...
    goto check_servers
)

:: Check Flask server
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo Waiting for Flask server...
    goto check_servers
)

:: Check FastAPI server
curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% neq 0 (
    echo Waiting for FastAPI server...
    goto check_servers
)

echo All servers are ready!

:: Run the benchmark
echo Running benchmark...
python test.py

:: Keep the window open
pause