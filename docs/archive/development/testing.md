# Testing Guide

This document provides comprehensive testing guidelines and strategies for the GacetaChat project.

## Testing Philosophy

GacetaChat follows a comprehensive testing strategy that includes:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Test system performance under load
- **Security Tests**: Test for security vulnerabilities

## Test Structure

### Directory Organization
```
test/
├── unit/
│   ├── test_pdf_processor.py
│   ├── test_faiss_helper.py
│   ├── test_qa.py
│   └── test_models.py
├── integration/
│   ├── test_api_endpoints.py
│   ├── test_database.py
│   └── test_workflow.py
├── e2e/
│   ├── test_user_journey.py
│   └── test_admin_workflow.py
├── performance/
│   ├── test_load.py
│   └── test_stress.py
├── security/
│   ├── test_auth.py
│   └── test_vulnerabilities.py
└── fixtures/
    ├── sample_data.py
    └── test_pdfs/
```

## Testing Framework

### Core Testing Libraries
```python
# requirements-test.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-asyncio>=0.21.0
pytest-xdist>=3.0.0
pytest-html>=3.1.0
pytest-benchmark>=4.0.0
factory-boy>=3.2.0
responses>=0.23.0
httpx>=0.24.0
```

### Configuration
```python
# pytest.ini
[tool:pytest]
testpaths = test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --html=reports/report.html
    --self-contained-html
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    security: Security tests
    performance: Performance tests
```

## Unit Tests

### PDF Processing Tests
```python
# test/unit/test_pdf_processor.py
import pytest
from unittest.mock import Mock, patch
from pdf_processor import PDFProcessor, PDFProcessingError

class TestPDFProcessor:
    
    @pytest.fixture
    def processor(self):
        return PDFProcessor()
    
    @pytest.fixture
    def sample_pdf_path(self):
        return "test/fixtures/sample.pdf"
    
    def test_extract_text_success(self, processor, sample_pdf_path):
        """Test successful text extraction from PDF"""
        text = processor.extract_text(sample_pdf_path)
        assert isinstance(text, str)
        assert len(text) > 0
    
    def test_extract_text_invalid_file(self, processor):
        """Test text extraction with invalid file"""
        with pytest.raises(PDFProcessingError):
            processor.extract_text("nonexistent.pdf")
    
    @patch('pdf_processor.PyPDF2.PdfReader')
    def test_extract_text_corrupted_pdf(self, mock_reader, processor):
        """Test handling of corrupted PDF files"""
        mock_reader.side_effect = Exception("PDF corrupted")
        
        with pytest.raises(PDFProcessingError):
            processor.extract_text("corrupted.pdf")
    
    def test_chunk_text(self, processor):
        """Test text chunking functionality"""
        text = "This is a sample text that should be chunked properly."
        chunks = processor.chunk_text(text, chunk_size=20, overlap=5)
        
        assert len(chunks) > 1
        assert all(len(chunk) <= 25 for chunk in chunks)  # chunk_size + overlap
    
    def test_process_pdf_complete_workflow(self, processor, sample_pdf_path):
        """Test complete PDF processing workflow"""
        result = processor.process_pdf(sample_pdf_path)
        
        assert 'text' in result
        assert 'chunks' in result
        assert 'metadata' in result
        assert len(result['chunks']) > 0
```

### FAISS Helper Tests
```python
# test/unit/test_faiss_helper.py
import pytest
import numpy as np
from unittest.mock import Mock, patch
from faiss_helper import FAISSHelper

class TestFAISSHelper:
    
    @pytest.fixture
    def faiss_helper(self):
        return FAISSHelper(dimension=384)
    
    def test_create_index(self, faiss_helper):
        """Test FAISS index creation"""
        index = faiss_helper.create_index()
        assert index is not None
        assert index.d == 384
    
    def test_add_vectors(self, faiss_helper):
        """Test adding vectors to index"""
        vectors = np.random.rand(10, 384).astype('float32')
        faiss_helper.add_vectors(vectors)
        
        assert faiss_helper.index.ntotal == 10
    
    def test_search_vectors(self, faiss_helper):
        """Test vector similarity search"""
        # Add sample vectors
        vectors = np.random.rand(100, 384).astype('float32')
        faiss_helper.add_vectors(vectors)
        
        # Search for similar vectors
        query = np.random.rand(1, 384).astype('float32')
        distances, indices = faiss_helper.search(query, k=5)
        
        assert len(distances[0]) == 5
        assert len(indices[0]) == 5
    
    def test_save_load_index(self, faiss_helper, tmp_path):
        """Test saving and loading FAISS index"""
        vectors = np.random.rand(10, 384).astype('float32')
        faiss_helper.add_vectors(vectors)
        
        # Save index
        index_path = tmp_path / "test_index.faiss"
        faiss_helper.save_index(str(index_path))
        
        # Load index
        new_helper = FAISSHelper(dimension=384)
        new_helper.load_index(str(index_path))
        
        assert new_helper.index.ntotal == 10
```

### QA System Tests
```python
# test/unit/test_qa.py
import pytest
from unittest.mock import Mock, patch
from qa import QASystem, QAError

class TestQASystem:
    
    @pytest.fixture
    def qa_system(self):
        return QASystem()
    
    @pytest.fixture
    def sample_context(self):
        return [
            "This is the first relevant document chunk.",
            "This is the second relevant document chunk.",
            "This is the third relevant document chunk."
        ]
    
    def test_generate_answer_success(self, qa_system, sample_context):
        """Test successful answer generation"""
        question = "What is the main topic?"
        
        with patch('qa.openai.ChatCompletion.create') as mock_openai:
            mock_openai.return_value = Mock(
                choices=[Mock(message=Mock(content="The main topic is testing."))]
            )
            
            answer = qa_system.generate_answer(question, sample_context)
            assert isinstance(answer, str)
            assert len(answer) > 0
    
    def test_generate_answer_api_error(self, qa_system, sample_context):
        """Test handling of OpenAI API errors"""
        question = "What is the main topic?"
        
        with patch('qa.openai.ChatCompletion.create') as mock_openai:
            mock_openai.side_effect = Exception("API Error")
            
            with pytest.raises(QAError):
                qa_system.generate_answer(question, sample_context)
    
    def test_format_context(self, qa_system, sample_context):
        """Test context formatting"""
        formatted = qa_system.format_context(sample_context)
        
        assert isinstance(formatted, str)
        assert all(chunk in formatted for chunk in sample_context)
    
    def test_validate_question(self, qa_system):
        """Test question validation"""
        # Valid question
        assert qa_system.validate_question("What is the weather?") == True
        
        # Invalid questions
        assert qa_system.validate_question("") == False
        assert qa_system.validate_question("   ") == False
        assert qa_system.validate_question("a" * 1000) == False
```

## Integration Tests

### Database Integration Tests
```python
# test/integration/test_database.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Document, Chunk, User
from crud import DocumentCRUD, UserCRUD

class TestDatabaseIntegration:
    
    @pytest.fixture
    def db_session(self):
        """Create test database session"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        yield session
        
        session.close()
    
    def test_document_crud_operations(self, db_session):
        """Test document CRUD operations"""
        crud = DocumentCRUD(db_session)
        
        # Create
        doc_data = {
            "filename": "test.pdf",
            "file_path": "/path/to/test.pdf",
            "date_published": "2024-01-01"
        }
        doc = crud.create_document(doc_data)
        assert doc.id is not None
        
        # Read
        retrieved_doc = crud.get_document(doc.id)
        assert retrieved_doc.filename == "test.pdf"
        
        # Update
        updated_doc = crud.update_document(doc.id, {"filename": "updated.pdf"})
        assert updated_doc.filename == "updated.pdf"
        
        # Delete
        crud.delete_document(doc.id)
        assert crud.get_document(doc.id) is None
    
    def test_user_crud_operations(self, db_session):
        """Test user CRUD operations"""
        crud = UserCRUD(db_session)
        
        # Create user
        user_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        user = crud.create_user(user_data)
        assert user.id is not None
        
        # Test unique constraints
        with pytest.raises(Exception):
            crud.create_user(user_data)  # Should fail due to unique constraint
```

### API Integration Tests
```python
# test/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from fastapp import app

class TestAPIEndpoints:
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_search_endpoint(self, client):
        """Test document search endpoint"""
        payload = {
            "query": "test query",
            "limit": 5
        }
        
        response = client.post("/api/search", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert "query_time" in data
    
    def test_search_endpoint_validation(self, client):
        """Test search endpoint input validation"""
        # Missing query
        response = client.post("/api/search", json={"limit": 5})
        assert response.status_code == 422
        
        # Invalid limit
        response = client.post("/api/search", json={"query": "test", "limit": -1})
        assert response.status_code == 422
    
    def test_upload_endpoint(self, client):
        """Test document upload endpoint"""
        test_file = ("test.pdf", b"fake pdf content", "application/pdf")
        
        response = client.post("/api/upload", files={"file": test_file})
        assert response.status_code == 200
        
        data = response.json()
        assert "document_id" in data
        assert "status" in data
```

## End-to-End Tests

### User Journey Tests
```python
# test/e2e/test_user_journey.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserJourney:
    
    @pytest.fixture
    def driver(self):
        """Setup Chrome driver for testing"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()
    
    def test_complete_search_workflow(self, driver):
        """Test complete user search workflow"""
        # Navigate to application
        driver.get("http://localhost:8501")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Find search input
        search_input = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        
        # Enter search query
        search_input.send_keys("test query")
        
        # Submit search
        search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
        search_button.click()
        
        # Wait for results
        results = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
        )
        
        assert results is not None
```

## Performance Tests

### Load Testing
```python
# test/performance/test_load.py
import pytest
import time
import concurrent.futures
from fastapi.testclient import TestClient
from fastapp import app

class TestPerformance:
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_search_performance(self, client):
        """Test search endpoint performance"""
        payload = {"query": "test query", "limit": 10}
        
        start_time = time.time()
        response = client.post("/api/search", json=payload)
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Should complete within 2 seconds
    
    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests"""
        def make_request():
            return client.post("/api/search", json={"query": "test", "limit": 5})
        
        # Submit 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in futures]
        
        # All requests should succeed
        assert all(response.status_code == 200 for response in responses)
    
    @pytest.mark.benchmark
    def test_pdf_processing_benchmark(self, benchmark):
        """Benchmark PDF processing performance"""
        from pdf_processor import PDFProcessor
        
        processor = PDFProcessor()
        result = benchmark(processor.process_pdf, "test/fixtures/sample.pdf")
        
        assert 'text' in result
        assert 'chunks' in result
```

## Security Tests

### Authentication Tests
```python
# test/security/test_auth.py
import pytest
from fastapi.testclient import TestClient
from fastapp import app

class TestSecurity:
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_unauthorized_access(self, client):
        """Test unauthorized access to protected endpoints"""
        response = client.get("/api/admin/users")
        assert response.status_code == 401
    
    def test_sql_injection_prevention(self, client):
        """Test SQL injection prevention"""
        malicious_query = "'; DROP TABLE users; --"
        
        response = client.post("/api/search", json={"query": malicious_query})
        assert response.status_code == 200  # Should not crash
        
        # Database should still be intact
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_xss_prevention(self, client):
        """Test XSS prevention"""
        xss_payload = "<script>alert('xss')</script>"
        
        response = client.post("/api/search", json={"query": xss_payload})
        assert response.status_code == 200
        
        # Response should not contain raw script tags
        assert "<script>" not in response.text
```

## Test Fixtures and Utilities

### Test Data Factory
```python
# test/fixtures/factories.py
import factory
from datetime import datetime
from models import Document, User, Chunk

class DocumentFactory(factory.Factory):
    class Meta:
        model = Document
    
    filename = factory.Sequence(lambda n: f"document_{n}.pdf")
    file_path = factory.LazyAttribute(lambda obj: f"/path/to/{obj.filename}")
    date_published = factory.LazyFunction(datetime.now)
    status = "processed"

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    created_at = factory.LazyFunction(datetime.now)

class ChunkFactory(factory.Factory):
    class Meta:
        model = Chunk
    
    document_id = factory.SubFactory(DocumentFactory)
    content = factory.Faker('text', max_nb_chars=1000)
    page_number = factory.Faker('random_int', min=1, max=100)
    chunk_index = factory.Faker('random_int', min=0, max=50)
```

### Mock Data
```python
# test/fixtures/sample_data.py
import json
from datetime import datetime

SAMPLE_PDF_CONTENT = """
This is a sample PDF document for testing purposes.
It contains multiple paragraphs and sections.

Section 1: Introduction
This section introduces the document.

Section 2: Main Content
This section contains the main content of the document.
It includes various types of information for testing.

Section 3: Conclusion
This section concludes the document.
"""

SAMPLE_SEARCH_RESULTS = [
    {
        "id": 1,
        "content": "This is the first search result.",
        "score": 0.95,
        "metadata": {"page": 1, "section": "Introduction"}
    },
    {
        "id": 2,
        "content": "This is the second search result.",
        "score": 0.87,
        "metadata": {"page": 2, "section": "Main Content"}
    }
]

SAMPLE_USER_DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "created_at": datetime.now().isoformat()
}
```

## Test Configuration

### Environment Setup
```bash
# test.env
TESTING=true
DATABASE_URL=sqlite:///test.db
OPENAI_API_KEY=test-key
LOG_LEVEL=ERROR
CACHE_ENABLED=false
```

### Test Commands
```bash
# Run all tests
pytest

# Run specific test category
pytest -m unit
pytest -m integration
pytest -m e2e

# Run with coverage
pytest --cov=. --cov-report=html

# Run performance tests
pytest -m performance --benchmark-only

# Run tests in parallel
pytest -n auto

# Run specific test file
pytest test/unit/test_pdf_processor.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

## Continuous Integration

### GitHub Actions Workflow
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Test Metrics and Reporting

### Coverage Requirements
- **Minimum Coverage**: 80%
- **Critical Components**: 95%
- **New Code**: 100%

### Test Reporting
```python
# Generate test report
pytest --html=reports/test_report.html --self-contained-html

# Generate coverage report
pytest --cov=. --cov-report=html --cov-report=term

# Generate performance report
pytest --benchmark-only --benchmark-html=reports/performance.html
```

## Best Practices

### Writing Good Tests
1. **Clear Test Names**: Use descriptive test names
2. **Arrange-Act-Assert**: Structure tests clearly
3. **Single Responsibility**: One assertion per test
4. **Independent Tests**: Tests should not depend on each other
5. **Fast Tests**: Keep tests fast and efficient

### Test Data Management
1. **Use Factories**: Generate test data with factories
2. **Clean Up**: Always clean up test data
3. **Isolation**: Each test should have its own data
4. **Realistic Data**: Use realistic test data

### Mock Strategy
1. **External Dependencies**: Mock external APIs
2. **Slow Operations**: Mock time-consuming operations
3. **Non-deterministic**: Mock random or time-based operations
4. **Side Effects**: Mock operations with side effects

This comprehensive testing guide ensures that GacetaChat maintains high quality and reliability through systematic testing practices.
