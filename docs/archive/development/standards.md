# Development Standards & Guidelines

## 📋 Code Standards

### Python Code Style

We follow **PEP 8** with some modifications:

#### Naming Conventions
```python
# Classes: PascalCase
class PDFProcessor:
    pass

# Functions/variables: snake_case
def process_latest_pdf():
    user_id = 123
    
# Constants: UPPER_SNAKE_CASE
OPENAI_MODEL_NAME = "gpt-4o"
MAX_TOKENS = 2000

# Private methods: Leading underscore
def _internal_helper():
    pass
```

#### File Organization
```python
# Import order:
# 1. Standard library
import os
import datetime
from typing import List, Optional

# 2. Third-party packages
import streamlit as st
import sqlalchemy
from langchain import OpenAI

# 3. Local imports
from models import User, Prompt
from config import config
```

#### Error Handling
```python
# Always use specific exception types
try:
    result = process_pdf(file_path)
except FileNotFoundError:
    logger.error(f"PDF file not found: {file_path}")
    return None
except Exception as e:
    logger.error(f"Unexpected error processing PDF: {e}")
    raise
```

### Database Standards

#### Model Design
```python
# Always include timestamps
class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Use descriptive table names
class ExecutionSession(BaseModel):
    __tablename__ = "execution_sessions"
    
# Always define relationships properly
class Prompt(BaseModel):
    content_template = relationship("ContentTemplate", back_populates="prompts")
```

#### Query Patterns
```python
# Always use context managers
def get_user_prompts(user_id: int):
    with Session() as session:
        return session.query(Prompt).filter_by(user_id=user_id).all()

# Use descriptive query methods
def get_active_execution_sessions(date: str):
    return session.query(ExecutionSession)\
        .filter(ExecutionSession.date == date)\
        .filter(ExecutionSession.status == ExecutionState.ACTIVE)\
        .order_by(ExecutionSession.created_at.desc())\
        .all()
```

## 🏗️ Architecture Patterns

### Repository Pattern
```python
# Abstract base repository
class BaseRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, id: int):
        return self.session.query(self.model).filter_by(id=id).first()
    
    def create(self, **kwargs):
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance

# Specific implementations
class PromptRepository(BaseRepository):
    model = Prompt
    
    def get_by_alias(self, alias: str):
        return self.session.query(Prompt).filter_by(alias=alias).first()
```

### Service Layer Pattern
```python
# Business logic in services
class PromptExecutionService:
    def __init__(self, prompt_repo: PromptRepository, llm_service: LLMService):
        self.prompt_repo = prompt_repo
        self.llm_service = llm_service
    
    def execute_prompt(self, prompt_id: int, context: dict):
        prompt = self.prompt_repo.get_by_id(prompt_id)
        if not prompt:
            raise PromptNotFoundError(f"Prompt {prompt_id} not found")
        
        return self.llm_service.generate_response(prompt.text, context)
```

### Configuration Management
```python
# Environment-based configuration
class Config:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///gaceta.db")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
    
    def validate(self):
        if not self.openai_api_key:
            raise ConfigurationError("OPENAI_API_KEY is required")
```

## 🧪 Testing Standards

### Unit Tests
```python
# Test file naming: test_<module_name>.py
# tests/test_pdf_processor.py

import pytest
from unittest.mock import Mock, patch
from pdf_processor import PDFProcessor

class TestPDFProcessor:
    def setup_method(self):
        self.processor = PDFProcessor()
    
    def test_process_valid_pdf(self):
        # Given
        mock_pdf_path = "test.pdf"
        
        # When
        result = self.processor.process_pdf(mock_pdf_path)
        
        # Then
        assert result is not None
        assert isinstance(result, dict)
    
    @patch('pdf_processor.PyPDFLoader')
    def test_process_invalid_pdf(self, mock_loader):
        # Given
        mock_loader.side_effect = FileNotFoundError()
        
        # When/Then
        with pytest.raises(FileNotFoundError):
            self.processor.process_pdf("invalid.pdf")
```

### Integration Tests
```python
# tests/test_integration.py
class TestPromptExecution:
    def test_end_to_end_prompt_execution(self, db_session):
        # Given
        prompt = create_test_prompt(db_session)
        pdf_content = load_test_pdf()
        
        # When
        result = execute_prompt_workflow(prompt.id, pdf_content)
        
        # Then
        assert result.status == ExecutionState.COMPLETED
        assert result.response is not None
```

## 📊 Logging Standards

### Logging Configuration
```python
# logging_setup.py
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
```

### Logging Patterns
```python
# Good logging practices
logger = logging.getLogger(__name__)

def process_document(doc_id: int):
    logger.info(f"Starting document processing for ID: {doc_id}")
    
    try:
        # Process document
        logger.debug(f"Processing steps completed for doc {doc_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to process document {doc_id}: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info(f"Document processing completed for ID: {doc_id}")
```

## 🚀 Deployment Standards

### Environment Setup
```bash
# Production environment
export ENVIRONMENT=production
export DEBUG=false
export OPENAI_API_KEY=sk-prod-...
export DATABASE_URL=postgresql://...

# Staging environment
export ENVIRONMENT=staging
export DEBUG=true
export OPENAI_API_KEY=sk-staging-...
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8512 8050

CMD ["./start.sh"]
```

### Process Management
```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'gaceta-api',
      script: 'fastapp.py',
      interpreter: 'python',
      env: {
        NODE_ENV: 'production'
      },
      error_file: './logs/api-error.log',
      out_file: './logs/api-out.log',
      log_file: './logs/api-combined.log'
    }
  ]
}
```

## 🔍 Code Review Checklist

### Before Submitting PR
- [ ] Code follows PEP 8 standards
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Environment variables documented
- [ ] Error handling implemented
- [ ] Logging statements added
- [ ] Performance considerations addressed
- [ ] Security review completed

### Review Points
- [ ] **Security**: No hardcoded secrets, proper input validation
- [ ] **Performance**: Efficient database queries, proper indexing
- [ ] **Maintainability**: Clear code structure, adequate comments
- [ ] **Testability**: Code is easily testable, mocks used appropriately
- [ ] **Documentation**: README updated, API docs current

## 📚 Documentation Standards

### Code Documentation
```python
class PDFProcessor:
    """Handles PDF document processing and text extraction.
    
    This class provides methods to download, process, and extract text
    from PDF documents for further analysis.
    
    Attributes:
        faiss_helper (FAISSHelper): Helper for vector indexing
        
    Example:
        >>> processor = PDFProcessor(faiss_helper)
        >>> documents = processor.process_latest_pdf()
    """
    
    def process_pdf(self, file_path: str) -> Optional[List[Document]]:
        """Process a PDF file and extract documents.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            Optional[List[Document]]: List of processed documents or None if failed
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ProcessingError: If PDF processing fails
        """
```

### API Documentation
```python
# FastAPI auto-generates OpenAPI docs
@app.get("/execution_session/", response_model=List[ExecutionSessionResponse])
async def get_execution_sessions(
    session_id: int = Query(..., description="Session ID to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get execution session details.
    
    Retrieves detailed information about a specific execution session
    including all associated logs and results.
    """
```

## 🔧 Development Workflow

### Git Flow
```bash
# Feature development
git checkout -b feature/new-functionality
git commit -m "feat: add new functionality"
git push origin feature/new-functionality

# Bug fixes
git checkout -b fix/bug-description
git commit -m "fix: resolve issue with PDF processing"

# Commit message format
feat: add new feature
fix: fix bug
docs: update documentation
style: formatting changes
refactor: code refactoring
test: add tests
chore: maintenance tasks
```

### Development Environment
```bash
# Virtual environment setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install
```

## 📈 Performance Guidelines

### Database Optimization
```python
# Use appropriate indexes
class ExecutionLog(Base):
    __tablename__ = "execution_logs"
    
    # Index on frequently queried fields
    session_id = Column(Integer, ForeignKey('execution_sessions.id'), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

# Optimize queries
def get_recent_logs(limit: int = 10):
    return session.query(ExecutionLog)\
        .options(joinedload(ExecutionLog.session))\
        .order_by(ExecutionLog.created_at.desc())\
        .limit(limit)\
        .all()
```

### Memory Management
```python
# Process large files in chunks
def process_large_pdf(file_path: str, chunk_size: int = 1000):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield process_chunk(chunk)
```

This development guide ensures consistency, maintainability, and scalability across the GacetaChat project.
