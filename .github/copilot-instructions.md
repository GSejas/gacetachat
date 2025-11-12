# GacetaChat AI Development Instructions

## System Architecture
GacetaChat is a **3-tier microservices architecture** for processing Costa Rica's official gazette:
- **Frontend**: Streamlit app on port 8512 (`streamlit_app.py`, `mpages/`)
- **Backend**: FastAPI on port 8050 (`fastapp.py`)
- **Processor**: Background PDF processing (`download_gaceta.py`)
- **Data**: SQLite + FAISS vector store for semantic search

All services are orchestrated by **PM2** (see `ecosystem.config.js`) or **Docker** (`Dockerfile`, `startup.py`). The system follows an event-driven pattern where PDF processing triggers AI analysis via `PromptExecutionEngine`.

## Core Data Flow
1. **PDF Ingestion**: `download_gaceta.py` scrapes gov site → stores in `gaceta_pdfs/{date}/`
2. **Processing**: `PDFProcessor` + `FAISSHelper` extract text → generate embeddings → store in SQLite
3. **Querying**: User queries → `query_folder()` → FAISS similarity search → OpenAI completion
4. **Sessions**: All interactions tracked via `ExecutionSession` and `ContentExecutionLog` models

## Key Development Patterns

### Database Models (`models.py`)
- **State Management**: `ExecutionState` enum tracks processing states (INIT → EXECUTED → APPROVED/FAILED)
- **Template System**: `ContentTemplate` → `Prompt` → `ContentExecutionLog` hierarchy
- **Document Tracking**: `GacetaPDF` links to execution sessions via foreign keys
- **UUID Sessions**: `ExecutionSession.id` uses UUID strings, not integers

### Session Management
```python
# Always use this pattern for DB operations
from db import get_db
with get_db() as db:
    session = db.query(ExecutionSession).filter(ExecutionSession.date == date).first()
    db.commit()  # Always commit when making changes
```

### AI Processing Pipeline (`crud.py`)
```python
# Core pattern: PromptExecutionEngine handles all AI interactions
engine = PromptExecutionEngine(db_session)
result = engine.execute_prompt(prompt_text, session_id)
# Returns: {"partial": processed_query, "answer": ai_response, "sources": context_docs}
```

### Prompt Template System
- Prompts support `{{alias}}` substitution from previous execution results
- `alias` field in Prompt model enables cross-prompt variable passing
- `scheduled_execution` controls automatic processing vs manual triggers

## Critical Commands

### Development Setup
```bash
# Option 1: Individual services (development)
uvicorn fastapp:app --host 127.0.0.1 --port 8050 --reload  # Backend first
streamlit run streamlit_app.py --server.port 8512          # Frontend second  
python download_gaceta.py                                  # Background processor (optional)

# Option 2: PM2 orchestration (production-like)
pm2 start ecosystem.config.js
pm2 logs            # View all service logs
pm2 monit           # Real-time monitoring dashboard

# Option 3: Docker containerization (production)
docker run -p 8050:8050 -p 8512:8512 -e OPENAI_API_KEY=${OPENAI_API_KEY} gacetachat:latest
# OR using the VS Code task: "Start FastAPI Backend" (Docker-based)
```

### Testing with Tox
```bash
tox -e smoke-test    # Quick system verification (30 seconds)
tox -e py310         # Full test suite with coverage
tox -e lint          # Code quality checks (flake8, mypy, bandit)
tox -e format        # Auto-format with black/isort
```

### Database Operations
```python
# CRITICAL: Always use context manager for DB sessions
from db import get_db
db = next(get_db())  # For dependency injection
# OR
with get_db() as db:  # For standalone operations
    # Your database operations
    db.commit()
```

## Integration Points

### OpenAI Integration (`qa.py`)
- Uses `langchain_openai.ChatOpenAI` with temperature=0.3 by default
- Context window managed via `pop_docs_upto_limit()` function  
- Rate limiting handled in `services/counter.py`
- Model selection: `gpt-4o` (configurable via `config.py`)

### FAISS Vector Search (`faiss_helper.py`)
- **Index Structure**: `gaceta_pdfs/{YYYY-MM-DD}/index.faiss` + `index.pkl`
- Embeddings: OpenAI text-embedding-ada-002 via `OpenAIEmbeddings`
- **CRITICAL**: Each date requires separate index - never share across dates
- Load with `allow_dangerous_deserialization=True` (required for FAISS)

### Twitter Integration (`mpages/2_Twitter.py`)
- OAuth flow via `tweepy` library in `oauth_helpers.py`
- Automated content generation from specific prompt templates
- State management through Streamlit session state

## Project-Specific Conventions

### File Organization
- `mpages/`: Streamlit multi-page structure (`1_Home.py`, `2_Twitter.py`, `3_Admin.py`)
- `services/`: Business logic modules (counter for rate limiting)
- `test/`: Two-tier structure (`backend/` for unit tests, `smoke/` for basic verification)
- Date-based storage: All PDF and index files organized by `YYYY-MM-DD` format

### Error Handling & Logging
```python
# Standard logging pattern
from logging_setup import setup_logging
setup_logging()  # Call at module top level

# State tracking pattern
execution_log.state = ExecutionState.FAILED.value
db.commit()
```

### Configuration Patterns (`config.py`)
- Environment variables with fallbacks: `os.getenv("VAR", "default")`
- Test isolation via `TESTING=true` environment variable
- OpenAI settings centralized in Config class

### Streamlit Session State Management
```python
# Initialize session state safely
if "query_count" not in st.session_state:
    st.session_state["query_count"] = 0

# Costa Rica timezone handling
costa_rica_tz = pytz.timezone("America/Costa_Rica")
date_str = datetime.now(costa_rica_tz).strftime("%Y-%m-%d")
```

## Development Workflow
1. **Local Development**: Use individual service commands above
2. **Production**: Deploy via PM2 with `ecosystem.config.js` OR Docker with `Dockerfile`
3. **Testing**: Smoke tests verify basic functionality, integration tests verify component interaction
4. **Documentation**: MkDocs site with architecture docs in `docs/`

## Docker Deployment Patterns
```python
# startup.py orchestrates all services in containerized environment
def start_backend():    # FastAPI on port 8050
def start_frontend():   # Streamlit on port 8512  
def start_pdf_processor():  # Background gazette processing

# VS Code tasks.json includes Docker deployment task:
# "Start FastAPI Backend" -> runs Docker container with both ports exposed
```

## Common Pitfalls
- **Service Dependencies**: Backend (port 8050) must start before frontend (port 8512)
- **Database Sessions**: Always use context managers; avoid session leaks
- **FAISS Indexes**: Each PDF date needs separate index files - don't share indexes across dates
- **Streamlit State**: Session state is separate from database sessions - manage carefully
- **UUID Fields**: `ExecutionSession.id` is string UUID, not integer - filter accordingly
- **Environment Setup**: Missing `OPENAI_API_KEY` will cause runtime failures, not import errors
- **Docker vs PM2**: Choose deployment method consistently - Docker for containerized, PM2 for process management
