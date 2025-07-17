# Installation Guide

This guide will help you set up GacetaChat on your local machine or server.

## Prerequisites

Before installing GacetaChat, ensure you have the following:

### System Requirements

- **Operating System**: Linux, macOS, or Windows 10/11
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: At least 2GB free space
- **Network**: Stable internet connection for API calls

### Required Accounts & API Keys

1. **OpenAI Account**
   - Sign up at [platform.openai.com](https://platform.openai.com)
   - Generate an API key
   - Ensure you have credits for API usage

2. **Twitter Developer Account** (Optional)
   - Apply at [developer.twitter.com](https://developer.twitter.com)
   - Create a new app
   - Generate API keys and tokens

## Installation Methods

### Method 1: Quick Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/gacetachat/gacetachat.git
cd gacetachat

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python -c "from models import *; from db import engine; Base.metadata.create_all(bind=engine)"

# Start the application
python start.py
```

### Method 2: Docker Installation

```bash
# Clone the repository
git clone https://github.com/gacetachat/gacetachat.git
cd gacetachat

# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Method 3: Manual Installation

#### Step 1: Clone Repository
```bash
git clone https://github.com/gacetachat/gacetachat.git
cd gacetachat
```

#### Step 2: Python Environment
```bash
# Check Python version
python --version

# Create virtual environment
python -m venv gaceta_env

# Activate environment
# Windows:
gaceta_env\Scripts\activate
# macOS/Linux:
source gaceta_env/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

#### Step 4: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

#### Step 5: Database Setup
```bash
# Initialize database
python setup_database.py

# Run migrations (if any)
python migrate_database.py

# Verify setup
python verify_installation.py
```

## Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL_NAME=gpt-4o
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.3

# Application Settings
APP_SECRET_API_KEY=your-secret-api-key-here
ENVIRONMENT=development
DEBUG=true

# Database Configuration
DATABASE_URL=sqlite:///gaceta.db

# Twitter Integration (Optional)
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET_KEY=your-twitter-api-secret
TWITTER_CONSUMER_API_KEY=your-consumer-key
TWITTER_CONSUMER_API_SECRET_KEY=your-consumer-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-token-secret

# File Storage
GACETA_PDFS_DIR=gaceta_pdfs
FAISS_INDEX_DIR=faiss_indexes

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/gaceta.log
```

### Optional Configuration

```env
# Performance Settings
WORKER_PROCESSES=2
WORKER_THREADS=4
MAX_CONCURRENT_REQUESTS=10

# Cache Settings
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# Monitoring
SENTRY_DSN=your-sentry-dsn
ENABLE_METRICS=true
```

## Service Configuration

### Method 1: PM2 (Production)

```bash
# Install PM2 globally
npm install -g pm2

# Start services
pm2 start ecosystem.config.js

# Check status
pm2 status

# View logs
pm2 logs

# Stop services
pm2 stop all
```

### Method 2: Manual Service Start

```bash
# Terminal 1: Start FastAPI backend
uvicorn fastapp:app --host 127.0.0.1 --port 8050 --reload

# Terminal 2: Start Streamlit frontend
streamlit run app.py --server.port 8512

# Terminal 3: Start background processor
python download_gaceta.py
```

### Method 3: Docker Services

```bash
# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs for specific service
docker-compose logs -f streamlit

# Restart specific service
docker-compose restart fastapi
```

## Verification

### Health Checks

1. **Backend API**
   ```bash
   curl http://localhost:8050/health
   ```

2. **Frontend**
   ```bash
   curl http://localhost:8512
   ```

3. **Database Connection**
   ```bash
   python -c "from db import Session; print('Database OK' if Session() else 'Database Error')"
   ```

### Test Installation

```bash
# Run basic tests
python test_installation.py

# Test API endpoints
python test_api.py

# Test PDF processing
python test_pdf_processing.py
```

## Troubleshooting

### Common Issues

#### 1. **Python Version Conflicts**
```bash
# Check Python version
python --version

# Use specific Python version
python3.9 -m venv venv
```

#### 2. **Permission Errors**
```bash
# Windows: Run as Administrator
# macOS/Linux: Use sudo for system-wide installation
sudo pip install -r requirements.txt
```

#### 3. **Missing Dependencies**
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# macOS with Homebrew
brew install python@3.9
```

#### 4. **Port Conflicts**
```bash
# Check if ports are in use
netstat -an | grep 8050
netstat -an | grep 8512

# Use different ports
uvicorn fastapp:app --port 8051
streamlit run app.py --server.port 8513
```

#### 5. **Database Issues**
```bash
# Reset database
rm gaceta.db
python setup_database.py

# Check database permissions
ls -la gaceta.db
```

### Log Files

Check these locations for error logs:

- **Application Logs**: `logs/gaceta.log`
- **PM2 Logs**: `~/.pm2/logs/`
- **Docker Logs**: `docker-compose logs`

### Getting Help

If you encounter issues:

1. Check the [FAQ](../reference/faq.md)
2. Review [Common Issues](../operations/troubleshooting.md)
3. Search [GitHub Issues](https://github.com/gacetachat/gacetachat/issues)
4. Create a new issue with:
   - System information
   - Error messages
   - Steps to reproduce

## Next Steps

After successful installation:

1. **Configure your first prompts**: See [Configuration Guide](configuration.md)
2. **Test the system**: Follow [Quick Start Guide](quick-start.md)
3. **Set up monitoring**: Review [Operations Guide](../operations/monitoring.md)
4. **Learn to demo**: Check [Demo Guide](../guides/demo-guide.md)

!!! success "Installation Complete"
    Your GacetaChat installation is ready! Visit `http://localhost:8512` to access the application.
