# API Reference

## Overview
Complete API reference for the GacetaChat FastAPI backend.

## Status
⚠️ **Documentation in Progress**

This section is under development. Please check back later or contribute to its development.

## Base URL
```
http://localhost:8050
```

## Authentication
All API endpoints require an `X-API-KEY` header with a valid API key.

## Core Endpoints

### Execution Sessions
```bash
# Get execution session by date
GET /execution_session_by_date/?date=2025-07-06

# Get available days with processed content
GET /execution_session/available/

# List all execution sessions
GET /execution_session/
```

### Query Management
```bash
# Check global query limits
GET /check_global_limit/

# Query processed documents
POST /query/
```

### Twitter Integration
```bash
# Twitter OAuth callback
GET /twitter/callback

# Twitter authentication
POST /twitter/auth
```

## Response Formats
All responses are in JSON format with standard HTTP status codes.

## Error Handling
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (invalid API key)
- `404` - Not Found (resource not found)
- `500` - Internal Server Error

## Rate Limiting
API calls are rate-limited. Check the `X-RateLimit-*` headers in responses.

## Contributing
See [Contributing Guide](contributing.md) for API development guidelines.
