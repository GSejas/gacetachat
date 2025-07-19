# Troubleshooting Guide

## Overview
Common issues and solutions for the GacetaChat platform.

## Status
⚠️ **Documentation in Progress**

This section is under development. Please check back later or contribute to its development.

## Common Issues

### Service Startup Problems

#### Frontend won't start
```bash
# Check if backend is running first
curl http://localhost:8050/health

# Start backend if needed
uvicorn fastapp:app --host 127.0.0.1 --port 8050

# Then start frontend
streamlit run streamlit_app.py --server.port 8512
```

#### Database connection errors
```bash
# Check database file exists
ls -la gaceta1.db

# Recreate database if needed
python -c "from models import *; from db import engine; Base.metadata.create_all(bind=engine)"
```

### PDF Processing Issues

#### PDF download failures
- Check government website availability
- Verify network connectivity
- Check `download_gaceta.py` logs

#### FAISS index errors
- Verify FAISS CPU installation: `pip install faiss-cpu`
- Check available disk space for indexes
- Verify `gaceta_pdfs/{date}/` directory structure

### API and Integration Issues

#### OpenAI API errors
- Verify `OPENAI_API_KEY` in environment
- Check API quota and usage
- Review rate limiting settings

#### Twitter integration problems
- Verify Twitter API credentials
- Check OAuth callback URL configuration
- Review Twitter API rate limits

## Debugging Commands

### System Health Check
```bash
# Run smoke tests
tox -e smoke-test

# Check service status
ps aux | grep -E "(streamlit|uvicorn|download_gaceta)"

# Check logs
tail -f download.log
```

### Performance Debugging
```bash
# Run performance tests
tox -e performance

# Check memory usage
ps aux --sort=-%mem | head

# Check disk usage
df -h
du -sh gaceta_pdfs/
```

## Getting Help
- Check the [FAQ](../reference/faq.md)
- Review [Documentation Issues](../reference/documentation-issues-analysis.md)
- Open an issue on GitHub

## Contributing
See [Contributing Guide](../development/contributing.md) for how to help improve this documentation.
