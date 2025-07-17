# Development Setup Guide

This guide walks you through setting up a complete development environment for GacetaChat.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher (3.10 recommended)
- **Git**: Latest version
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: 20GB free space

### Required Software
- **Python 3.10+**: [Download from python.org](https://www.python.org/downloads/)
- **Git**: [Download from git-scm.com](https://git-scm.com/downloads)
- **VS Code**: [Download from code.visualstudio.com](https://code.visualstudio.com/) (recommended)
- **Docker**: [Download from docker.com](https://www.docker.com/products/docker-desktop) (optional)

## Initial Setup

### 1. Clone the Repository
```bash
git clone https://github.com/gacetachat/gacetachat.git
cd gacetachat
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configuration
# Required variables:
# - OPENAI_API_KEY=your-openai-api-key
# - SECRET_KEY=your-secret-key
# - DATABASE_URL=sqlite:///gaceta.db
```

### 5. Database Setup
```bash
# Initialize database
python -c "from db import init_db; init_db()"

# Run migrations (if any)
python manage.py migrate
```

### 6. Download Sample Data
```bash
# Download sample PDFs for testing
python download_gaceta.py --date 2024-07-15
```

## Development Workflow

### Running the Application

#### Option 1: Streamlit App (Recommended for Development)
```bash
streamlit run streamlit_app.py
```

#### Option 2: Flask App
```bash
python app.py
```

#### Option 3: FastAPI App
```bash
uvicorn fastapp:app --reload
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test/test_integration.py

# Run tests with verbose output
pytest -v
```

### Code Quality
```bash
# Format code with black
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

## Development Tools

### IDE Setup (VS Code)

#### Recommended Extensions
- Python (Microsoft)
- Pylance (Microsoft)
- Python Docstring Generator
- GitLens
- Docker (Microsoft)
- Jupyter

#### VS Code Settings
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Git Workflow

#### Branch Naming Convention
- `feature/description`: New features
- `bugfix/description`: Bug fixes
- `hotfix/description`: Critical fixes
- `refactor/description`: Code refactoring
- `docs/description`: Documentation updates

#### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(auth): add OAuth2 authentication
fix(pdf): resolve text extraction issue
docs(api): update API documentation
```

### Development Scripts

#### Setup Script
```bash
#!/bin/bash
# setup.sh - Complete development setup

echo "Setting up GacetaChat development environment..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Initialize database
python -c "from db import init_db; init_db()"

# Download sample data
python download_gaceta.py --date 2024-07-15

echo "Setup complete! Run 'streamlit run streamlit_app.py' to start."
```

#### Test Script
```bash
#!/bin/bash
# test.sh - Run all tests and quality checks

echo "Running code quality checks..."

# Format code
black .
isort .

# Lint code
flake8 .

# Type checking
mypy .

# Run tests
pytest --cov=. --cov-report=html

echo "All checks complete!"
```

## Database Development

### Database Schema
```sql
-- Example schema for development
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    date_published DATE,
    processed_at TIMESTAMP,
    status TEXT DEFAULT 'pending'
);

CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER,
    content TEXT NOT NULL,
    page_number INTEGER,
    chunk_index INTEGER,
    embedding_vector BLOB,
    FOREIGN KEY (document_id) REFERENCES documents (id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Database Migrations
```python
# migrations/001_initial_schema.py
def upgrade():
    """Create initial database schema"""
    # Migration code here
    pass

def downgrade():
    """Rollback initial schema"""
    # Rollback code here
    pass
```

## API Development

### API Documentation
```python
# Example API endpoint documentation
@app.route('/api/search', methods=['POST'])
def search_documents():
    """
    Search documents using natural language query
    
    Request:
        {
            "query": "string",
            "limit": "integer (optional, default: 10)",
            "filters": "object (optional)"
        }
    
    Response:
        {
            "results": [
                {
                    "document_id": "string",
                    "content": "string",
                    "score": "float",
                    "metadata": "object"
                }
            ],
            "total": "integer",
            "query_time": "float"
        }
    """
    pass
```

### API Testing
```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from fastapp import app

client = TestClient(app)

def test_search_endpoint():
    response = client.post("/api/search", json={
        "query": "test query",
        "limit": 5
    })
    assert response.status_code == 200
    assert "results" in response.json()
```

## Frontend Development

### Streamlit Components
```python
# Custom Streamlit components
import streamlit as st

def render_search_interface():
    """Render the search interface"""
    st.title("GacetaChat - Document Search")
    
    # Query input
    query = st.text_input("Enter your question:")
    
    # Search options
    col1, col2 = st.columns(2)
    with col1:
        limit = st.slider("Number of results", 1, 20, 10)
    with col2:
        date_filter = st.date_input("Filter by date")
    
    # Search button
    if st.button("Search"):
        results = search_documents(query, limit, date_filter)
        display_results(results)

def display_results(results):
    """Display search results"""
    for result in results:
        with st.expander(f"Document {result['id']}"):
            st.write(result['content'])
            st.write(f"Score: {result['score']:.3f}")
```

## Performance Profiling

### Profiling Tools
```python
# profile.py
import cProfile
import pstats
from pstats import SortKey

def profile_function(func, *args, **kwargs):
    """Profile a function and print stats"""
    pr = cProfile.Profile()
    pr.enable()
    
    result = func(*args, **kwargs)
    
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(20)
    
    return result
```

### Memory Profiling
```python
# memory_profiler.py
from memory_profiler import profile

@profile
def process_large_document(document_path):
    """Process a large document and monitor memory usage"""
    # Function implementation
    pass
```

## Debugging

### Logging Configuration
```python
# logging_config.py
import logging
import sys

def setup_logging(level=logging.INFO):
    """Setup logging configuration for development"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set third-party library log levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
```

### Debug Mode
```python
# debug.py
import os
from flask import Flask

app = Flask(__name__)

# Enable debug mode for development
if os.environ.get('FLASK_ENV') == 'development':
    app.debug = True
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True
```

## Docker Development

### Development Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements-dev.txt

# Copy source code
COPY . .

# Set environment variables
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Start development server
CMD ["python", "app.py"]
```

### Docker Compose for Development
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
      - "8501:8501"  # Streamlit
    volumes:
      - .:/app
      - ./gaceta_pdfs:/app/gaceta_pdfs
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=sqlite:///gaceta.db
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  docs:
    image: squidfunk/mkdocs-material
    ports:
      - "8000:8000"
    volumes:
      - .:/docs
    command: serve --dev-addr 0.0.0.0:8000
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Or add to .env file
echo "PYTHONPATH=$(pwd)" >> .env
```

#### 2. Database Connection Issues
```bash
# Check database file permissions
ls -la gaceta.db

# Recreate database
rm gaceta.db
python -c "from db import init_db; init_db()"
```

#### 3. Dependency Conflicts
```bash
# Create fresh virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. OpenAI API Issues
```bash
# Test API key
python -c "
import openai
openai.api_key = 'your-api-key'
print(openai.models.list())
"
```

### Debug Commands
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check environment variables
printenv | grep GACETA

# Test database connection
python -c "
from db import get_db_connection
conn = get_db_connection()
print('Database connection successful')
conn.close()
"
```

## Contributing

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

### Code Review Process
- All code must pass automated tests
- Code must follow established style guidelines
- Documentation must be updated for new features
- Performance impact should be considered

### Release Process
1. Update version number
2. Update CHANGELOG.md
3. Create release branch
4. Deploy to staging
5. Run integration tests
6. Deploy to production
7. Tag release

## Resources

### Documentation
- [Python Official Documentation](https://docs.python.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Learning Resources
- [Real Python](https://realpython.com/)
- [Python Package Index](https://pypi.org/)
- [GitHub Guides](https://guides.github.com/)

### Community
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)
- [Reddit r/Python](https://www.reddit.com/r/Python/)
- [Python Discord](https://pythondiscord.com/)

This setup guide should get you up and running with GacetaChat development. For additional help, please refer to the project documentation or reach out to the development team.
