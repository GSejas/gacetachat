# 🔥 ROBO-ACTIVIST NON-DOCKER DEPLOYMENT GUIDE 🔥

## 🎯 SINCE DOCKER ISN'T AVAILABLE - NATIVE DEPLOYMENT

### 1. **IMMEDIATE DEPENDENCY FIX**
```bash
# Install missing critical dependencies
pip install schedule pytest-watch tox mkdocs mkdocs-material

# OR use our comprehensive requirements
pip install -r requirements.txt
```

### 2. **ENVIRONMENT SETUP** 
```bash
# Copy environment template
copy .env.template .env

# Edit .env with your actual values (CRITICAL: Add your OPENAI_API_KEY!)
```

### 3. **DATABASE INITIALIZATION**
```bash
# Initialize database schema
python -c "from models import Base; from db import engine; Base.metadata.create_all(engine)"
```

### 4. **PRODUCTION STARTUP OPTIONS**

#### Option A: All-in-One Startup (RECOMMENDED)
```bash
python startup.py
```

#### Option B: Manual Service Management
```bash
# Terminal 1: Backend
uvicorn fastapp:app --host 127.0.0.1 --port 8050

# Terminal 2: Frontend  
streamlit run streamlit_app.py --server.port 8512

# Terminal 3: PDF Processor (Optional)
python download_gaceta.py
```

#### Option C: PM2 Process Manager (Linux/Mac)
```bash
# Install PM2
npm install -g pm2

# Start all services
pm2 start ecosystem.config.js

# Monitor
pm2 status
pm2 logs
```

### 5. **WINDOWS SERVICE DEPLOYMENT**
```powershell
# Create Windows batch files for service management

# start-backend.bat
@echo off
cd /d "C:\path\to\gacetachat"
call venv\Scripts\activate
uvicorn fastapp:app --host 127.0.0.1 --port 8050

# start-frontend.bat  
@echo off
cd /d "C:\path\to\gacetachat"
call venv\Scripts\activate
streamlit run streamlit_app.py --server.port 8512
```

### 6. **CLOUD DEPLOYMENT (No Docker)**

#### Heroku
```bash
# Add Procfile
echo "web: python startup.py" > Procfile

# Deploy
git add .
git commit -m "Deploy democratic transparency platform"
heroku create gacetachat-demo
git push heroku main
```

#### Railway/Render
```bash
# Add start command in platform: python startup.py
# Set environment variables in platform dashboard
```

#### DigitalOcean App Platform
```yaml
# .do/app.yaml
name: gacetachat
services:
- name: web
  source_dir: /
  github:
    repo: your-username/gacetachat
    branch: main
  run_command: python startup.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
```

### 7. **PRODUCTION CHECKLIST**
- [ ] ✅ Set real OPENAI_API_KEY in .env
- [ ] ✅ Install all dependencies from requirements.txt  
- [ ] ✅ Initialize database schema
- [ ] ✅ Test startup.py locally
- [ ] ✅ Configure firewall (ports 8050, 8512)
- [ ] ✅ Set up reverse proxy (nginx/apache) if needed
- [ ] ✅ Configure domain/SSL if public
- [ ] ✅ Set up monitoring/logs
- [ ] ✅ Backup strategy for SQLite database
