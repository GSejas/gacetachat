# Streamlit Best Practices and Standards for GacetaChat

## Core Development Standards

### 1. Project Structure and Organization

#### Recommended Directory Structure
```
gacetachat/
├── app.py                      # Main application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py            # Application configuration
│   └── theme.py               # UI theme configuration
├── components/
│   ├── __init__.py
│   ├── base.py                # Base component classes
│   ├── chat.py                # Chat interface components
│   ├── navigation.py          # Navigation components
│   ├── cards.py               # Card components
│   └── forms.py               # Form components
├── pages/
│   ├── __init__.py
│   ├── home.py                # Home page
│   ├── chat.py                # Chat page
│   ├── analytics.py           # Analytics page
│   └── admin.py               # Admin page
├── services/
│   ├── __init__.py
│   ├── api.py                 # API service layer
│   ├── cache.py               # Caching service
│   └── auth.py                # Authentication service
├── utils/
│   ├── __init__.py
│   ├── helpers.py             # Utility functions
│   ├── validators.py          # Input validation
│   └── formatters.py          # Data formatting
├── assets/
│   ├── styles/
│   │   ├── main.css          # Main stylesheet
│   │   ├── components.css    # Component styles
│   │   └── theme.css         # Theme variables
│   ├── images/
│   └── icons/
└── tests/
    ├── __init__.py
    ├── test_components.py
    ├── test_pages.py
    └── test_services.py
```

### 2. Code Organization Standards

#### Base Component Pattern
```python
# components/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import streamlit as st

class BaseComponent(ABC):
    """Base class for all Streamlit components"""
    
    def __init__(self, key: Optional[str] = None, **kwargs):
        self.key = key or f"{self.__class__.__name__}_{id(self)}"
        self.props = kwargs
        
    @abstractmethod
    def render(self) -> Any:
        """Render the component"""
        pass
    
    def apply_styles(self, styles: str) -> None:
        """Apply custom CSS styles"""
        st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)
    
    def validate_props(self) -> bool:
        """Validate component props"""
        return True

class StatefulComponent(BaseComponent):
    """Base class for components with state management"""
    
    def __init__(self, key: Optional[str] = None, **kwargs):
        super().__init__(key, **kwargs)
        self.state_key = f"component_state_{self.key}"
        
    @property
    def state(self) -> Dict[str, Any]:
        """Get component state"""
        if self.state_key not in st.session_state:
            st.session_state[self.state_key] = {}
        return st.session_state[self.state_key]
    
    def update_state(self, **kwargs) -> None:
        """Update component state"""
        self.state.update(kwargs)
```

#### Enhanced Chat Component
```python
# components/chat.py
from typing import List, Dict, Callable, Optional
import streamlit as st
from .base import StatefulComponent

class ChatMessage:
    def __init__(self, role: str, content: str, timestamp: Optional[str] = None):
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()

class ChatInterface(StatefulComponent):
    """Enhanced chat interface with typing indicators and message history"""
    
    def __init__(self, 
                 key: Optional[str] = None,
                 on_message: Optional[Callable[[str], str]] = None,
                 placeholder: str = "Type your message...",
                 max_messages: int = 100,
                 **kwargs):
        super().__init__(key, **kwargs)
        self.on_message = on_message
        self.placeholder = placeholder
        self.max_messages = max_messages
        
    def render(self) -> None:
        """Render chat interface"""
        self._render_messages()
        self._render_input()
        self._render_typing_indicator()
        
    def _render_messages(self) -> None:
        """Render chat messages"""
        messages = self.state.get('messages', [])
        
        # Create scrollable message container
        message_container = st.container()
        with message_container:
            for message in messages[-self.max_messages:]:
                with st.chat_message(message.role):
                    st.markdown(message.content)
                    if hasattr(message, 'timestamp'):
                        st.caption(f"Sent at {message.timestamp}")
    
    def _render_input(self) -> None:
        """Render chat input with enhanced features"""
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.chat_input(
                placeholder=self.placeholder,
                key=f"{self.key}_input"
            )
            
        with col2:
            if st.button("🗑️", help="Clear chat", key=f"{self.key}_clear"):
                self.clear_messages()
                st.rerun()
        
        if user_input:
            self._handle_user_message(user_input)
    
    def _render_typing_indicator(self) -> None:
        """Show typing indicator when processing"""
        if self.state.get('is_typing', False):
            st.markdown("""
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
            """, unsafe_allow_html=True)
    
    def _handle_user_message(self, message: str) -> None:
        """Handle user message"""
        # Add user message
        self.add_message("user", message)
        
        # Show typing indicator
        self.update_state(is_typing=True)
        
        # Process message
        if self.on_message:
            try:
                response = self.on_message(message)
                self.add_message("assistant", response)
            except Exception as e:
                self.add_message("assistant", f"Sorry, I encountered an error: {str(e)}")
        
        # Hide typing indicator
        self.update_state(is_typing=False)
        st.rerun()
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to chat"""
        messages = self.state.get('messages', [])
        messages.append(ChatMessage(role, content))
        self.update_state(messages=messages)
    
    def clear_messages(self) -> None:
        """Clear all messages"""
        self.update_state(messages=[])
```

### 3. State Management Best Practices

#### Session State Management
```python
# utils/state.py
from typing import Any, Dict, Optional
import streamlit as st

class StateManager:
    """Centralized state management for Streamlit apps"""
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get value from session state"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set value in session state"""
        st.session_state[key] = value
    
    @staticmethod
    def update(updates: Dict[str, Any]) -> None:
        """Update multiple values in session state"""
        for key, value in updates.items():
            st.session_state[key] = value
    
    @staticmethod
    def clear(key: str) -> None:
        """Clear value from session state"""
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def initialize_defaults(defaults: Dict[str, Any]) -> None:
        """Initialize default values if not present"""
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

# Usage in app initialization
def initialize_app_state():
    StateManager.initialize_defaults({
        'user_id': 1,
        'current_date': datetime.now().strftime('%Y-%m-%d'),
        'query_count': 0,
        'chat_messages': [],
        'selected_model': 'gpt-4o',
        'max_tokens': 512,
        'temperature': 0.7
    })
```

### 4. Performance Optimization Standards

#### Caching Strategy
```python
# services/cache.py
import streamlit as st
from typing import Any, Callable, Optional
import hashlib
import json

class CacheManager:
    """Advanced caching utilities for Streamlit"""
    
    @staticmethod
    def cache_data(ttl: int = 3600, show_spinner: bool = True):
        """Enhanced data caching decorator"""
        def decorator(func: Callable) -> Callable:
            return st.cache_data(ttl=ttl, show_spinner=show_spinner)(func)
        return decorator
    
    @staticmethod
    def cache_resource(show_spinner: bool = True):
        """Enhanced resource caching decorator"""
        def decorator(func: Callable) -> Callable:
            return st.cache_resource(show_spinner=show_spinner)(func)
        return decorator
    
    @staticmethod
    def generate_cache_key(data: Any) -> str:
        """Generate consistent cache key from data"""
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(serialized.encode()).hexdigest()
    
    @staticmethod
    def invalidate_cache(func: Callable) -> None:
        """Invalidate cache for specific function"""
        if hasattr(func, 'clear'):
            func.clear()

# Usage examples
@CacheManager.cache_data(ttl=3600)
def get_gaceta_data(date: str) -> Dict[str, Any]:
    """Get Gaceta data with caching"""
    return api_call_to_get_gaceta(date)

@CacheManager.cache_resource()
def load_ml_model() -> Any:
    """Load ML model with resource caching"""
    return load_expensive_model()
```

#### Lazy Loading Pattern
```python
# utils/lazy_loading.py
from typing import Any, Callable, Optional
import streamlit as st

class LazyLoader:
    """Lazy loading utilities for Streamlit components"""
    
    @staticmethod
    def lazy_load(
        loader_func: Callable,
        placeholder_func: Optional[Callable] = None,
        error_handler: Optional[Callable] = None
    ) -> Any:
        """Lazy load content with placeholder"""
        container = st.container()
        
        with container:
            if placeholder_func:
                placeholder = placeholder_func()
            else:
                placeholder = st.empty()
            
            try:
                # Load content
                content = loader_func()
                placeholder.empty()
                return content
            except Exception as e:
                placeholder.empty()
                if error_handler:
                    error_handler(e)
                else:
                    st.error(f"Error loading content: {str(e)}")
                return None
    
    @staticmethod
    def skeleton_placeholder() -> None:
        """Show skeleton loading placeholder"""
        st.markdown("""
        <div class="skeleton-container">
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line short"></div>
        </div>
        """, unsafe_allow_html=True)
```

### 5. Error Handling Standards

#### Comprehensive Error Handling
```python
# utils/error_handling.py
import streamlit as st
import logging
from typing import Any, Callable, Optional
from enum import Enum

class ErrorType(Enum):
    VALIDATION = "validation"
    API = "api"
    PROCESSING = "processing"
    NETWORK = "network"
    AUTHENTICATION = "authentication"

class ErrorHandler:
    """Centralized error handling for Streamlit apps"""
    
    @staticmethod
    def handle_error(
        error: Exception,
        error_type: ErrorType,
        user_message: Optional[str] = None,
        show_details: bool = False
    ) -> None:
        """Handle errors with appropriate user feedback"""
        
        # Log the error
        logging.error(f"{error_type.value}: {str(error)}")
        
        # Get user-friendly message
        if user_message:
            message = user_message
        else:
            message = ErrorHandler._get_default_message(error_type)
        
        # Show error to user
        if error_type == ErrorType.VALIDATION:
            st.error(f"⚠️ {message}")
        elif error_type == ErrorType.API:
            st.error(f"🔌 {message}")
        elif error_type == ErrorType.PROCESSING:
            st.error(f"⚙️ {message}")
        elif error_type == ErrorType.NETWORK:
            st.error(f"🌐 {message}")
        elif error_type == ErrorType.AUTHENTICATION:
            st.error(f"🔐 {message}")
        
        # Show details if requested
        if show_details:
            with st.expander("Error Details"):
                st.code(str(error))
    
    @staticmethod
    def _get_default_message(error_type: ErrorType) -> str:
        """Get default error message for error type"""
        messages = {
            ErrorType.VALIDATION: "Please check your input and try again.",
            ErrorType.API: "Service temporarily unavailable. Please try again later.",
            ErrorType.PROCESSING: "Processing failed. Please try again.",
            ErrorType.NETWORK: "Network connection issue. Please check your connection.",
            ErrorType.AUTHENTICATION: "Authentication required. Please log in."
        }
        return messages.get(error_type, "An unexpected error occurred.")
    
    @staticmethod
    def safe_execute(
        func: Callable,
        error_type: ErrorType,
        fallback: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """Safely execute function with error handling"""
        try:
            return func(**kwargs)
        except Exception as e:
            ErrorHandler.handle_error(e, error_type)
            if fallback:
                return fallback()
            return None
```

### 6. Testing Standards

#### Component Testing
```python
# tests/test_components.py
import unittest
from unittest.mock import Mock, patch
import streamlit as st
from components.chat import ChatInterface

class TestChatInterface(unittest.TestCase):
    """Test cases for ChatInterface component"""
    
    def setUp(self):
        """Set up test environment"""
        self.chat = ChatInterface(key="test_chat")
    
    def test_initialization(self):
        """Test component initialization"""
        self.assertIsNotNone(self.chat.key)
        self.assertEqual(self.chat.key, "test_chat")
    
    def test_add_message(self):
        """Test adding messages"""
        self.chat.add_message("user", "Hello")
        messages = self.chat.state.get('messages', [])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].role, "user")
        self.assertEqual(messages[0].content, "Hello")
    
    def test_clear_messages(self):
        """Test clearing messages"""
        self.chat.add_message("user", "Hello")
        self.chat.clear_messages()
        messages = self.chat.state.get('messages', [])
        self.assertEqual(len(messages), 0)
    
    @patch('streamlit.chat_input')
    def test_user_input_handling(self, mock_input):
        """Test user input handling"""
        mock_input.return_value = "Test message"
        mock_handler = Mock(return_value="Response")
        
        chat = ChatInterface(key="test", on_message=mock_handler)
        chat._handle_user_message("Test message")
        
        mock_handler.assert_called_once_with("Test message")
        messages = chat.state.get('messages', [])
        self.assertEqual(len(messages), 2)  # User message + response
```

### 7. Documentation Standards

#### Component Documentation
```python
# components/cards.py
from typing import Optional, Dict, Any
import streamlit as st
from .base import BaseComponent

class InfoCard(BaseComponent):
    """
    Display information in a card format.
    
    Args:
        title (str): Card title
        content (str): Card content
        icon (Optional[str]): Icon to display
        color (str): Card color theme ('primary', 'secondary', 'success', 'warning', 'error')
        expandable (bool): Whether the card can be expanded
        
    Example:
        >>> card = InfoCard(
        ...     title="Daily Summary",
        ...     content="Today's Gaceta contains 25 new entries",
        ...     icon="📊",
        ...     color="primary"
        ... )
        >>> card.render()
    """
    
    def __init__(self, 
                 title: str,
                 content: str,
                 icon: Optional[str] = None,
                 color: str = "primary",
                 expandable: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.content = content
        self.icon = icon
        self.color = color
        self.expandable = expandable
        
    def render(self) -> None:
        """Render the info card"""
        # Implementation here
        pass
```

### 8. Security Standards

#### Input Validation
```python
# utils/validators.py
from typing import Any, Dict, List, Optional
import re

class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate date format (YYYY-MM-DD)"""
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(pattern, date_str) is not None
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize user input"""
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\']', '', input_str)
        return sanitized.strip()
    
    @staticmethod
    def validate_query_length(query: str, max_length: int = 500) -> bool:
        """Validate query length"""
        return len(query) <= max_length
```

## Development Workflow

### 1. Development Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
black .
mypy .
```

### 2. Code Quality Standards
- **Type Hints**: Use type hints for all function parameters and return values
- **Documentation**: Comprehensive docstrings for all classes and functions
- **Testing**: Minimum 80% test coverage
- **Linting**: Pass all flake8, black, and mypy checks
- **Security**: Regular security audits and dependency updates

### 3. Performance Monitoring
```python
# utils/performance.py
import time
import streamlit as st
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Log performance metrics
        execution_time = end_time - start_time
        if execution_time > 1.0:  # Log slow operations
            st.warning(f"Slow operation detected: {func.__name__} took {execution_time:.2f}s")
        
        return result
    return wrapper
```

This comprehensive set of standards ensures that GacetaChat maintains high code quality, performance, and user experience while following Streamlit best practices.
