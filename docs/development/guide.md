# Development Guide

## Overview
Comprehensive guide for developers working on the GacetaChat project.

## Status
⚠️ **Documentation in Progress**

This section is under development. Please check back later or contribute to its development.

## Development Environment Setup

### Prerequisites
- Python 3.10+
- Node.js 16+ (for PM2)
- Git
- OpenAI API Key

### Quick Setup
```bash
# Clone repository
git clone https://github.com/gacetachat/gacetachat.git
cd gacetachat

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run development servers
uvicorn fastapp:app --host 127.0.0.1 --port 8050 --reload  # Backend
streamlit run streamlit_app.py --server.port 8512          # Frontend
```

## Development Workflow

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints where possible
- Write comprehensive docstrings
- Maintain test coverage above 80%

### Testing with Tox
```bash
# Run all tests
tox

# Run specific test environments
tox -e py310          # Python 3.10 tests
tox -e lint           # Code linting
tox -e format         # Code formatting
tox -e smoke-test     # Quick smoke tests
tox -e docs           # Documentation build
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature description"

# Push and create pull request
git push origin feature/your-feature-name
```

## Architecture Overview

### System Components
- **Frontend**: Streamlit app (port 8512)
- **Backend**: FastAPI app (port 8050)
- **Processor**: Background PDF processing
- **Database**: SQLite with SQLAlchemy ORM
- **Vector Store**: FAISS for semantic search

### Key Directories
```
├── fastapp.py              # FastAPI backend
├── streamlit_app.py        # Streamlit frontend
├── download_gaceta.py      # Background processor
├── models.py               # Database models
├── crud.py                 # Database operations
├── qa.py                   # Question-answering logic
├── faiss_helper.py         # Vector search
├── mpages/                 # Streamlit pages
├── services/               # Business logic
└── test/                   # Test files
```

## Database Development

### Models
- Use SQLAlchemy for ORM
- Define relationships clearly
- Add proper indexes for performance
- Include validation and constraints

### Migrations
```python
# Example model change
class ExecutionSession(Base):
    __tablename__ = 'execution_sessions'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    state = Column(Enum(ExecutionState), default=ExecutionState.PENDING)
    # Add new fields here
```

## Frontend Development

### Streamlit Best Practices
- Use session state for data persistence
- Implement proper error handling
- Design responsive layouts
- Add loading indicators for slow operations

### Multi-page Structure
```python
# mpages/1_Home.py
import streamlit as st

def main():
    st.title("Home Page")
    # Page content here

if __name__ == "__main__":
    main()
```

## Backend Development

### FastAPI Patterns
```python
# fastapp.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/api/data")
def get_data(db: Session = Depends(get_db)):
    return {"data": "example"}
```

### Error Handling
```python
from fastapi import HTTPException

@app.get("/api/data/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

## Testing

### Unit Tests
```python
# test/test_crud.py
import pytest
from crud import get_execution_session_by_date

def test_get_execution_session_by_date(db_session):
    # Test implementation
    session = get_execution_session_by_date(db_session, test_date)
    assert session is not None
```

### Integration Tests
```python
# test/test_integration.py
from fastapi.testclient import TestClient
from fastapp import app

client = TestClient(app)

def test_api_endpoint():
    response = client.get("/api/data")
    assert response.status_code == 200
```

## Deployment

### Local Development
```bash
# Start all services with PM2
pm2 start ecosystem.config.js

# Monitor services
pm2 monit

# View logs
pm2 logs
```

### Production Deployment
- Use environment variables for configuration
- Set up proper logging and monitoring
- Configure backup strategies
- Implement health checks

## Performance Optimization

### Database
- Use proper indexes
- Optimize query patterns
- Implement connection pooling
- Monitor slow queries

### Vector Search
- Optimize FAISS index parameters
- Implement result caching
- Batch similar operations
- Monitor search performance

## Security

### API Security
- Implement authentication where needed
- Use HTTPS in production
- Validate all inputs
- Implement rate limiting

### Data Protection
- Encrypt sensitive data
- Implement proper access controls
- Regular security audits
- Backup encryption

## Contributing
See [Contributing Guide](contributing.md) for detailed contribution guidelines.

## Troubleshooting
See [Troubleshooting Guide](../operations/troubleshooting.md) for common issues and solutions.
