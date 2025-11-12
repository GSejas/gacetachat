@echo off
REM 🔥 ROBO-ACTIVIST WINDOWS DEPLOYMENT SCRIPT 🔥
REM One-click deployment for democratic transparency platform

echo 🔥 ROBO-ACTIVIST DEPLOYMENT STARTING 🔥
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo 💡 Please create venv first: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo 📋 Copying template...
    copy .env.template .env
    echo.
    echo 🚨 CRITICAL: Edit .env file and add your OPENAI_API_KEY!
    echo 📝 Opening .env file for editing...
    notepad .env
    echo.
    echo ⏸️  Press any key after saving your API key...
    pause
)

REM Initialize database
echo 🗄️ Initializing database...
python -c "from models import Base; from db import engine; Base.metadata.create_all(engine); print('✅ Database initialized')"

REM Check if initialization succeeded
if %errorlevel% neq 0 (
    echo ❌ Database initialization failed!
    echo 💡 Check your environment configuration
    pause
    exit /b 1
)

echo.
echo 🎯 DEPLOYMENT COMPLETE! Starting services...
echo.
echo 🌐 The platform will start on:
echo    Frontend: http://localhost:8512
echo    Backend:  http://localhost:8050
echo.
echo 🛑 Press Ctrl+C to stop all services
echo.

REM Start the application
python startup.py

echo.
echo 👋 Services stopped. Thanks for using GacetaChat!
pause
