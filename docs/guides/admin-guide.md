# Admin Guide

## Overview
Administrative guide for managing the GacetaChat platform.

## Status
⚠️ **Documentation in Progress**

This section is under development. Please check back later or contribute to its development.

## System Administration

### Service Management
```bash
# Using PM2 (recommended for production)
pm2 start ecosystem.config.js
pm2 status
pm2 stop all
pm2 restart all
pm2 logs

# Manual service management
# Start backend
uvicorn fastapp:app --host 127.0.0.1 --port 8050

# Start frontend  
streamlit run streamlit_app.py --server.port 8512

# Start background processor
python download_gaceta.py
```

### Database Management
```bash
# Database backup
cp gaceta1.db gaceta1.db.backup.$(date +%Y%m%d)

# Database maintenance
python -c "from db import engine; from sqlalchemy import text; engine.execute(text('VACUUM;'))"

# View database contents
sqlite3 gaceta1.db ".tables"
sqlite3 gaceta1.db "SELECT * FROM execution_sessions LIMIT 10;"
```

### Content Management
```bash
# Check processed documents
ls -la gaceta_pdfs/

# Reprocess a specific date
python -c "from download_gaceta import check_and_download_today_pdf; check_and_download_today_pdf()"

# Clear old processed data
find gaceta_pdfs/ -name "*.pdf" -mtime +30 -delete
```

### Monitoring and Logs
```bash
# Check service health
curl http://localhost:8050/health
curl http://localhost:8512/health

# View logs
tail -f download.log
pm2 logs

# System resources
htop
df -h
```

### User Management
Access the admin interface at `http://localhost:8512/3_Admin` to:
- Manage user accounts
- Configure prompts and templates
- Monitor system usage
- Review processing logs

### Security
- Change default API keys in production
- Configure firewall rules for ports 8050 and 8512
- Set up SSL certificates for HTTPS
- Regular security updates

## Backup and Recovery
```bash
# Full backup
tar -czf gacetachat-backup-$(date +%Y%m%d).tar.gz \
  gaceta1.db gaceta_pdfs/ .env

# Restore from backup
tar -xzf gacetachat-backup-YYYYMMDD.tar.gz
```

## Contributing
See [Contributing Guide](../development/contributing.md) for how to help improve this documentation.
