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

:: Wait for servers to start
echo Waiting for servers to initialize (10 seconds)...
timeout /t 10 /nobreak

:: Run the benchmark
echo Running benchmark...
python test.py

:: Keep the window open
pause