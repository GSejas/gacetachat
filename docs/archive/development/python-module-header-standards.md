# Python Module Header Standards

## Overview
Standardized header format for all Python modules in the GacetaChat project to ensure consistency, maintainability, and proper documentation.

## Standard Module Header Template

### Complete Header Template
```python
#!/usr/bin/env python3
"""
Module Name: {module_name}
Description: {brief_description}

This module provides {detailed_description_of_functionality}.

Key Features:
- {feature_1}
- {feature_2}
- {feature_3}

Usage Example:
    ```python
    from {module_name} import {main_class_or_function}
    
    # Basic usage
    instance = {main_class_or_function}()
    result = instance.method()
    ```

Dependencies:
    - {dependency_1}: {purpose}
    - {dependency_2}: {purpose}

Author: GacetaChat Development Team
Created: {creation_date}
Last Modified: {last_modified_date}
Version: {version}

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
    - {important_note_1}
    - {important_note_2}

See Also:
    - {related_module_1}: {relationship}
    - {related_module_2}: {relationship}
"""

# Standard library imports
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# Third-party imports
import pandas as pd
import numpy as np

# Local application imports
from config import config
from models import Base, ExecutionSession
from utils import helper_function

# Module metadata
__version__ = "{version}"
__author__ = "GacetaChat Development Team"
__email__ = "dev@gacetachat.com"
__status__ = "Development"  # "Development", "Production", "Deprecated"

# Module-level constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
SUPPORTED_FORMATS = ['pdf', 'txt', 'json']

# Logging setup
import logging
logger = logging.getLogger(__name__)
```

## Header Components Explained

### 1. Shebang Line
```python
#!/usr/bin/env python3
```
- **Required**: For executable scripts
- **Optional**: For library modules
- **Purpose**: Specifies Python interpreter for direct execution

### 2. Module Docstring
```python
"""
Module Name: {module_name}
Description: {brief_description}
...
"""
```
- **Required**: All modules must have comprehensive docstrings
- **Format**: Triple quotes with structured sections
- **Content**: Name, description, features, usage, dependencies, metadata

### 3. Import Organization
```python
# Standard library imports
import os
import sys

# Third-party imports
import pandas as pd

# Local application imports
from config import config
```
- **Required**: Organize imports in three sections
- **Order**: Standard library, third-party, local imports
- **Style**: Alphabetical within each section

### 4. Module Metadata
```python
__version__ = "1.0.0"
__author__ = "GacetaChat Development Team"
__status__ = "Development"
```
- **Required**: Version, author, status
- **Optional**: Email, license, maintainer
- **Format**: Double underscore variables

### 5. Constants
```python
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
```
- **Style**: UPPERCASE with underscores
- **Location**: After imports, before classes/functions
- **Documentation**: Comment explaining purpose

## Specific Module Types

### 1. Main Application Modules
```python
#!/usr/bin/env python3
"""
Module Name: fastapp.py
Description: FastAPI backend server for GacetaChat application

This module implements the main FastAPI server that provides REST API endpoints
for document processing, search functionality, and user interactions.

Key Features:
- RESTful API endpoints for document operations
- Authentication and session management
- Integration with FAISS vector search
- OpenAI API integration for chat functionality

Usage Example:
    ```python
    # Run the server
    uvicorn fastapp:app --host 127.0.0.1 --port 8050
    
    # Or programmatically
    from fastapp import app
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8050)
    ```

Dependencies:
    - fastapi: Web framework for building APIs
    - uvicorn: ASGI server for FastAPI
    - sqlalchemy: Database ORM
    - openai: OpenAI API client

Author: GacetaChat Development Team
Created: 2024-01-15
Last Modified: 2024-07-18
Version: 1.2.0

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
    - Server runs on port 8050 by default
    - Requires OPENAI_API_KEY environment variable
    - Database must be initialized before starting

See Also:
    - streamlit_app.py: Frontend application
    - models.py: Database models
    - crud.py: Database operations
"""
```

### 2. Database Models
```python
"""
Module Name: models.py
Description: SQLAlchemy database models for GacetaChat application

This module defines all database models using SQLAlchemy ORM, including
tables for execution sessions, prompts, logs, and user data.

Key Features:
- SQLAlchemy ORM model definitions
- Relationship mappings between entities
- Database schema validation
- Enum definitions for state management

Usage Example:
    ```python
    from models import ExecutionSession, ContentExecutionLog
    from db import Session
    
    # Create a new session
    with Session() as db:
        session = ExecutionSession(user_id=1, date=datetime.now())
        db.add(session)
        db.commit()
    ```

Dependencies:
    - sqlalchemy: ORM framework
    - enum: Python enumeration support
    - datetime: Date and time handling

Author: GacetaChat Development Team
Created: 2024-01-10
Last Modified: 2024-07-18
Version: 1.1.0

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
    - Uses SQLite for development, PostgreSQL for production
    - All models inherit from Base class
    - Foreign key relationships are properly defined

See Also:
    - db.py: Database connection and session management
    - crud.py: Database CRUD operations
"""
```

### 3. Utility Modules
```python
"""
Module Name: faiss_helper.py
Description: FAISS vector database operations and utilities

This module provides helper functions and classes for managing FAISS vector
indexes, including loading, saving, and querying vector embeddings.

Key Features:
- FAISS index creation and management
- Vector embedding storage and retrieval
- Similarity search functionality
- Index optimization and persistence

Usage Example:
    ```python
    from faiss_helper import FAISSHelper
    
    helper = FAISSHelper()
    index = helper.load_faiss_index('path/to/index')
    results = helper.search(index, query_vector, k=5)
    ```

Dependencies:
    - faiss-cpu: Facebook AI Similarity Search library
    - numpy: Numerical computing
    - pickle: Object serialization

Author: GacetaChat Development Team
Created: 2024-01-20
Last Modified: 2024-07-18
Version: 1.0.5

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
    - Requires faiss-cpu package installation
    - Index files are stored in gaceta_pdfs/{date}/ directories
    - Vector dimensions must match between operations

See Also:
    - qa.py: Question-answering functionality
    - pdf_processor.py: Document processing
"""
```

### 4. Test Modules
```python
"""
Module Name: test_prompt_execution_engine.py
Description: Unit tests for PromptExecutionEngine class

This module contains comprehensive unit tests for the PromptExecutionEngine
class, testing all major functionality including prompt execution, session
management, and database operations.

Key Features:
- Unit tests with pytest framework
- Mock objects for external dependencies
- Database session testing
- Error condition testing

Usage Example:
    ```python
    # Run tests
    pytest test/backend/test_prompt_execution_engine.py -v
    
    # Run with coverage
    pytest test/backend/test_prompt_execution_engine.py --cov=crud
    ```

Dependencies:
    - pytest: Testing framework
    - unittest.mock: Mocking library
    - sqlalchemy: Database testing

Author: GacetaChat Development Team
Created: 2024-02-01
Last Modified: 2024-07-18
Version: 1.0.2

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
    - Uses mock database sessions for testing
    - All external API calls are mocked
    - Tests cover both success and failure scenarios

See Also:
    - crud.py: Module under test
    - conftest.py: Test configuration
    - test_integration.py: Integration tests
"""
```

## Implementation Guidelines

### 1. Required Fields
All modules must include:
- Module name and description
- Key features list
- Usage example
- Dependencies
- Author and dates
- Version number

### 2. Optional Fields
Modules may include:
- License information
- Copyright notice
- Special notes
- See Also references
- Status indicator

### 3. Version Numbering
Follow semantic versioning:
- **MAJOR.MINOR.PATCH**
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### 4. Documentation Standards
- Use clear, concise language
- Provide working code examples
- Explain complex concepts
- Reference related modules
- Keep documentation current

## Maintenance

### 1. Regular Updates
- Update "Last Modified" date when changing module
- Increment version number for significant changes
- Review and update dependencies list
- Verify code examples still work

### 2. Consistency Checks
- Ensure all modules follow the same format
- Verify import organization is consistent
- Check that metadata is accurate
- Validate documentation links

### 3. Quality Assurance
- Run automated checks for header compliance
- Review headers during code reviews
- Update templates when standards change
- Document any deviations and reasons

## Tools and Automation

### 1. Header Template Generator
```python
# Tool to generate standard headers
def generate_module_header(module_name, description, features=None):
    # Implementation for automatic header generation
    pass
```

### 2. Header Validation
```python
# Tool to validate header compliance
def validate_module_header(file_path):
    # Implementation for header validation
    pass
```

### 3. Automated Updates
- Pre-commit hooks for header validation
- Automated version number updates
- Dependency scanning and updates
- Documentation link validation

## Examples by Module Category

### Core Application Files
- `fastapp.py`: FastAPI backend server
- `streamlit_app.py`: Streamlit frontend application
- `download_gaceta.py`: Background PDF processing

### Data Layer
- `models.py`: SQLAlchemy database models
- `db.py`: Database connection management
- `crud.py`: Database CRUD operations

### Business Logic
- `qa.py`: Question-answering functionality
- `pdf_processor.py`: PDF document processing
- `faiss_helper.py`: Vector search operations

### Utilities
- `config.py`: Configuration management
- `logging_setup.py`: Logging configuration
- `oauth_helpers.py`: Authentication utilities

### Testing
- `test_*.py`: All test modules
- `conftest.py`: Test configuration
- `test_integration.py`: Integration tests

This standard ensures consistency across all Python modules in the GacetaChat project while providing comprehensive documentation for developers.
