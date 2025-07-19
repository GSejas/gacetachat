# GacetaChat AI Development Instructions

## System Architecture
GacetaChat is a **3-tier microservices architecture** for processing Costa Rica's official gazette:
- **Frontend**: Streamlit app on port 8512 (`streamlit_app.py`, `mpages/`)
- **Backend**: FastAPI on port 8050 (`fastapp.py`)
- **Processor**: Background PDF processing (`download_gaceta.py`)
- **Data**: SQLite + FAISS vector store for semantic search

All services are orchestrated by **PM2** (see `ecosystem.config.js`). The system follows an event-driven pattern where PDF processing triggers AI analysis via `PromptExecutionEngine`.

## Core Data Flow
1. **PDF Ingestion**: `download_gaceta.py` scrapes gov site → stores in `gaceta_pdfs/{date}/`
2. **Processing**: `PDFProcessor` + `FAISSHelper` extract text → generate embeddings → store in SQLite
3. **Querying**: User queries → `query_folder()` → FAISS similarity search → OpenAI completion
4. **Sessions**: All interactions tracked via `ExecutionSession` and `ContentExecutionLog` models

## Key Development Patterns

### Database Models (`models.py`)
- **State Management**: `ExecutionState` enum tracks processing states
- **Template System**: `ContentTemplate` → `Prompt` → `ContentExecutionLog` hierarchy
- **Document Tracking**: `GacetaPDF` links to execution sessions

### Session Management
```python
# Always use this pattern for DB operations
def get_execution_session_by_date(db: Session, date: datetime):
    return db.query(ExecutionSession).filter(ExecutionSession.date == date).first()
```

### AI Processing Pipeline
```python
# Core pattern in crud.py
engine = PromptExecutionEngine()
result = engine.execute_prompt(prompt_id, document_id)
# Always updates ExecutionSession with state tracking
```

## Critical Commands

### Development Setup
```bash
# Required services startup sequence
uvicorn fastapp:app --host 127.0.0.1 --port 8050  # Backend first
streamlit run streamlit_app.py --server.port 8512  # Frontend second
python download_gaceta.py                          # Background processor
```

### Testing with Tox
```bash
tox -e smoke-test    # Quick system verification
tox -e py           # Full test suite with coverage
tox -e lint         # Code quality checks
```

### Database Operations
```python
# Always use Session context manager
from db import Session
with Session() as db:
    # Database operations here
    db.commit()
```

## Integration Points

### OpenAI Integration (`qa.py`)
- Uses `langchain_openai.ChatOpenAI` with custom prompts
- Context window managed via `query_folder()` function
- Rate limiting handled in `services/counter.py`

### FAISS Vector Search (`faiss_helper.py`)
- Index stored per PDF date: `gaceta_pdfs/{date}/index.faiss`
- Embeddings generated via `OpenAIEmbeddings`
- Similarity search with configurable top-k results

### Twitter Integration (`fastapp.py`)
- OAuth flow via `tweepy` library
- Automated content generation from processed PDFs
- Managed through `2_Twitter.py` Streamlit page

## Project-Specific Conventions

### File Organization
- `mpages/`: Streamlit multi-page structure (`1_Home.py`, `2_Twitter.py`, `3_Admin.py`)
- `services/`: Business logic modules (counter, utilities)
- `test/`: Organized by component (`backend/`, `smoke/`, `integration/`)

### Error Handling
- Comprehensive logging via `logging_setup.py`
- State tracking in `ExecutionState` enum
- Graceful degradation in UI components

### Configuration (`config.py`)
- Environment-based config with defaults
- Separate test configurations via `TESTING` env var
- OpenAI model selection centralized

## Development Workflow
1. **Local Development**: Use individual service commands above
2. **Production**: Deploy via PM2 with `ecosystem.config.js`
3. **Testing**: Smoke tests verify basic functionality, integration tests verify component interaction
4. **Documentation**: MkDocs site with architecture docs in `docs/`

## Common Pitfalls
- **Service Dependencies**: Backend must start before frontend (FastAPI provides data endpoints)
- **Database Migrations**: Run model updates via SQLAlchemy before service restart
- **FAISS Indexes**: Each PDF date needs separate index files - don't share indexes across dates
- **Session State**: Streamlit session state separate from database sessions - manage carefully
