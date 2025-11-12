#!/usr/bin/env python3
"""
🔥 ROBO-ACTIVIST STARTUP ORCHESTRATOR 🔥
Unified startup script for democratic transparency platform
Handles service initialization, health checks, and graceful startup
"""

import asyncio
import logging
import multiprocessing
import os
import signal
import sys
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='🚀 %(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GacetaChat-Startup")

def check_environment():
    """Validate critical environment variables and dependencies"""
    logger.info("🔍 ENVIRONMENT VALIDATION STARTING...")
    
    required_env = [
        "OPENAI_API_KEY"
    ]
    
    missing = []
    for env_var in required_env:
        if not os.getenv(env_var):
            missing.append(env_var)
    
    if missing:
        logger.error(f"❌ MISSING ENVIRONMENT VARIABLES: {missing}")
        logger.error("💡 Copy .env.example to .env and configure!")
        sys.exit(1)
    
    # Check critical files
    critical_files = [
        "fastapp.py",
        "streamlit_app.py", 
        "download_gaceta.py",
        "models.py",
        "db.py"
    ]
    
    for file in critical_files:
        if not Path(file).exists():
            logger.error(f"❌ MISSING CRITICAL FILE: {file}")
            sys.exit(1)
    
    logger.info("✅ ENVIRONMENT VALIDATION PASSED!")

def start_backend():
    """Start FastAPI backend server"""
    logger.info("🔧 STARTING FASTAPI BACKEND...")
    os.system("python -m uvicorn fastapp:app --host 0.0.0.0 --port 8050")

def start_frontend():
    """Start Streamlit frontend server"""
    logger.info("🎨 STARTING STREAMLIT FRONTEND...")
    os.system("streamlit run streamlit_app.py --server.port 8512 --server.address 0.0.0.0")

def start_pdf_processor():
    """Start PDF processing daemon"""
    logger.info("📄 STARTING PDF PROCESSOR...")
    os.system("python download_gaceta.py")

def main():
    """Main startup orchestrator"""
    logger.info("🔥 ROBO-ACTIVIST DEMOCRATIC TRANSPARENCY PLATFORM STARTING 🔥")
    
    # Environment validation
    check_environment()
    
    # Initialize database
    logger.info("🗄️ INITIALIZING DATABASE...")
    try:
        from models import Base
        from db import engine
        Base.metadata.create_all(engine)
        logger.info("✅ DATABASE INITIALIZED")
    except Exception as e:
        logger.error(f"❌ DATABASE INITIALIZATION FAILED: {e}")
        sys.exit(1)
    
    # Determine startup mode
    mode = os.getenv("STARTUP_MODE", "all")
    
    if mode == "backend":
        start_backend()
    elif mode == "frontend":
        start_frontend()
    elif mode == "processor":
        start_pdf_processor()
    else:
        # Start all services in parallel
        logger.info("🚀 STARTING ALL SERVICES IN PARALLEL...")
        
        processes = []
        
        # Backend process
        backend_process = multiprocessing.Process(target=start_backend)
        backend_process.start()
        processes.append(backend_process)
        
        time.sleep(3)  # Let backend start first
        
        # Frontend process  
        frontend_process = multiprocessing.Process(target=start_frontend)
        frontend_process.start()
        processes.append(frontend_process)
        
        # PDF processor (optional in container)
        if os.getenv("ENABLE_PDF_PROCESSOR", "true").lower() == "true":
            pdf_process = multiprocessing.Process(target=start_pdf_processor)
            pdf_process.start()
            processes.append(pdf_process)
        
        logger.info("🎯 ALL SERVICES STARTED! Democratic transparency is ONLINE!")
        logger.info("🌐 Frontend: http://localhost:8512")
        logger.info("⚡ Backend: http://localhost:8050")
        
        # Wait for processes
        try:
            for process in processes:
                process.join()
        except KeyboardInterrupt:
            logger.info("🛑 SHUTTING DOWN GRACEFULLY...")
            for process in processes:
                process.terminate()
                process.join()

if __name__ == "__main__":
    main()
