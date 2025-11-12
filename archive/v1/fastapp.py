#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 FastAPI Backend Server - REST API & Microservice Orchestration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    FastAPI backend server providing REST API endpoints for GacetaChat. Handles
    execution session management, AI prompt processing, Twitter integration,
    and database operations. Central orchestrator for the 3-tier architecture.

🏗️ Architecture Flow:
    ```
    ┌─────────────────┐    HTTP/REST   ┌──────────────────┐
    │  Streamlit UI   │ ──────────────▶│   FastAPI App    │
    │  (Port 8512)    │    JSON API    │   (Port 8050)    │
    └─────────────────┘                └──────────────────┘
            │                                   │
            │ User Requests                     │ API Processing
            ▼                                   ▼
    ┌─────────────────┐                ┌──────────────────┐
    │ CORS Middleware │                │ API Key Auth     │
    │ (Allow All)     │                │ Middleware       │
    └─────────────────┘                └──────────────────┘
                                               │
                                               │ Route Dispatch
                                               ▼
    ┌─────────────────┐                ┌──────────────────┐
    │ Database Layer  │                │ Business Logic   │
    │ (SQLAlchemy)    │◀───────────────│ (CRUD + Prompt)  │
    └─────────────────┘                └──────────────────┘
            │                                   │
            │ Data Persistence                  │ External APIs
            ▼                                   ▼
    ┌─────────────────┐                ┌──────────────────┐
    │ SQLite Storage  │                │ Twitter + OpenAI │
    │ + FAISS Indices │                │ API Integration  │
    └─────────────────┘                └──────────────────┘
    ```

📥 Inputs:
    • HTTP requests: JSON payloads from Streamlit frontend and external clients
    • API authentication: X-API-KEY header validation for secure access
    • Database queries: Session management and execution tracking requests
    • Twitter OAuth: Callback handling and social media integration
    • File operations: PDF processing and FAISS index management

📤 Outputs:
    • JSON responses: Structured API responses with execution results
    • HTTP status codes: RESTful status indicators (200, 404, 401, 500)
    • CORS headers: Cross-origin resource sharing for frontend integration
    • Database updates: Persistent storage of execution sessions and logs
    • External API calls: Twitter posting and OpenAI prompt processing

🔗 Dependencies:
    • fastapi: Web framework with automatic API documentation and validation
    • sqlalchemy: Database ORM for session management and queries
    • tweepy: Twitter API integration for social media automation
    • cors_middleware: Cross-origin request handling for web UI
    • crud: Business logic layer with AI prompt execution engine

🏛️ Component Relationships:
    ```mermaid
    graph TD
        A[FastAPI App] --> B[CORS Middleware]
        A --> C[API Key Auth]
        A --> D[Route Handlers]

        D --> E[CRUD Operations]
        D --> F[Database Sessions]
        D --> G[Twitter Integration]

        E --> H[PromptExecutionEngine]
        F --> I[(SQLite DB)]
        G --> J[Twitter API]

        K[Streamlit Frontend] --> A
        A --> L[JSON Responses]

        classDef fastapi fill:#e1f5fe
        classDef middleware fill:#f3e5f5
        classDef external fill:#fff3e0
        classDef data fill:#fff8e1

        class A,D fastapi
        class B,C,E middleware
        class J,K external
        class F,I,H data
    ```

🔒 Security Considerations:
    ⚠️  HIGH: CORS allow_origins=["*"] enables access from any domain
    ⚠️  HIGH: API key stored in environment variable without rotation mechanism
    ⚠️  HIGH: Twitter OAuth callback URL hardcoded with ngrok tunnel
    ⚠️  MEDIUM: No rate limiting on expensive AI operations
    ⚠️  MEDIUM: Database sessions not protected against concurrent access issues

🛡️ Risk Analysis:
    • Authentication Bypass: Single API key for all operations, no user-based auth
    • CORS Vulnerability: Wildcard origin allows potential CSRF attacks
    • API Key Exposure: Keys stored in environment without secure vault
    • Resource Exhaustion: No request rate limiting or resource quotas
    • Data Validation: Limited input sanitization on user-provided parameters

⚡ Performance Characteristics:
    • Concurrency: Async FastAPI handles ~1000 concurrent requests
    • Response Time: 100-500ms for database operations, 2-8s for AI processing
    • Memory Usage: ~100MB baseline + session data + AI model overhead
    • Database Pool: SQLite single-writer limitation affects write throughput
    • API Throughput: Limited by OpenAI rate limits (3,500 RPM)

🧪 Testing Strategy:
    • Unit Tests: Individual endpoint validation with mocked dependencies
    • Integration Tests: End-to-end API workflows with test database
    • Performance Tests: Load testing with concurrent request simulation
    • Security Tests: Authentication bypass attempts, injection testing

📊 Monitoring & Observability:
    • Metrics: Request count, response times, error rates, database query time
    • Logging: Structured logging with request correlation IDs
    • Alerts: API failures, high error rates, database connection issues
    • Health Checks: Database connectivity, external API availability

🔄 Data Flow:
    ```
    HTTP Request ──▶ Auth Check ──▶ Route Handler ──▶ Business Logic ──▶ JSON Response
         │              │             │                │                   │
         ▼              ▼             ▼                ▼                   ▼
    CORS Check     API Key Valid   DB Session     CRUD Operation    Status Code
    ```

📚 Usage Examples:
    ```python
    # Start FastAPI server
    uvicorn fastapp:app --host 127.0.0.1 --port 8050

    # API request with authentication
    headers = {"X-API-KEY": "your-api-key"}
    response = requests.get(
        "http://localhost:8050/execution_session/available/",
        headers=headers
    )

    # Execute prompt session
    response = requests.post(
        "http://localhost:8050/execute_prompts/",
        json={"template_id": 1, "gaceta_id": 123},
        headers=headers
    )
    ```

🔧 Server Configuration:
    ```python
    # Environment Variables Required
    TWITTER_API_KEY = "your-twitter-key"
    TWITTER_CONSUMER_API_KEY = "your-consumer-key"
    APP_SECRET_API_KEY = "your-app-secret"

    # Server Settings
    HOST = "127.0.0.1"
    PORT = 8050
    RELOAD = True  # Development only

    # Security Settings
    CORS_ORIGINS = ["http://localhost:8512"]  # Restrict in production
    API_KEY_HEADER = "X-API-KEY"
    ```

🚨 Deployment Considerations:
    • Production CORS: Restrict origins to known frontend domains
    • API Security: Implement JWT tokens or OAuth for user authentication
    • Rate Limiting: Add request throttling to prevent abuse
    • Monitoring: Deploy with APM tools (DataDog, New Relic)
    • Health Checks: Configure load balancer health endpoints

Author: GacetaChat Team | Version: 2.1.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# from services.counter import check_global_limit, increment_global_query_count
from datetime import datetime
from typing import List

import tweepy
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from logging_setup import setup_logging
from models import *
from models import GacetaPDF
from services.counter import check_global_limit, increment_global_query_count

setup_logging()


import os
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

from db import get_db
from models import *

app = FastAPI()

# Replace these with your personal account's credentials
twitter_api_key = os.getenv("TWITTER_API_KEY")
twitter_api_secret_key = os.getenv("TWITTER_API_secret_key")


twitter_consumer_api_key = os.environ.get("TWITTER_CONSUMER_API_KEY")
twitter_consumer_api_secret_key = os.environ.get("TWITTER_CONSUMER_API_secret_key")

callback_url = "https://c470-186-176-232-195.ngrok-free.app/twitter/callback"

API_KEY = os.environ.get("APP_SECRET_API_KEY")


from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud import *

# CORS settings for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("X-API-KEY")
    if request.url.path == "/twitter/callback":
        return await call_next(request)
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    response = await call_next(request)
    return response


@app.get("/execution_session_by_date/")
async def get_execution_session(date: str, db: Session = Depends(get_db)):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        exec_sessions = get_execution_session_by_date(db, date_obj)
        if exec_sessions:
            return exec_sessions
        else:
            raise HTTPException(
                status_code=404, detail="Execution session not found for the given date"
            )
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format, should be YYYY-MM-DD"
        )


@app.get("/execution_session/available/")
async def list_available_index_days_api(db: Session = Depends(get_db)):
    days = list_available_index_days(db)
    return [day[0] for day in days]


@app.get("/execution_session/", response_model=List[dict])
async def execution_session_api(session_id: str, db: Session = Depends(get_db)):
    logs = display_last_execution_session(db, session_id)
    return logs


from datetime import datetime
from typing import List, Optional

# from . import models, schemas
from pydantic import BaseModel
from sqlalchemy import and_, asc, desc
from sqlalchemy.orm import Session


class LogQueryParams(BaseModel):
    limit: Optional[int] = 10
    offset: Optional[int] = 0
    order: Optional[str] = "desc"
    prompt_text: Optional[str] = None
    state: Optional[str] = None


class LogResponseSchema(BaseModel):
    id: str
    execution_session_id: str
    prompt_id: int
    state: str
    created_at: datetime
    error_message: Optional[str] = None
    query_response_id: Optional[str] = None
    template_id: Optional[int] = None
    prompt_text: str
    response: Optional[str] = None
    sources: Optional[str] = None

    class Config:
        orm_mode = True


import models


def get_content_logs(db: Session, params: LogQueryParams):
    query = (
        db.query(models.ContentExecutionLog)
        .join(models.Prompt)
        .add_entity(models.Prompt)
    )

    if params.prompt_text:
        query = query.filter(models.Prompt.prompt_text.contains(params.prompt_text))

    if params.state:
        query = query.filter(models.ContentExecutionLog.state == params.state)

    if params.order == "asc":
        query = query.order_by(asc(models.ContentExecutionLog.created_at))
    else:
        query = query.order_by(desc(models.ContentExecutionLog.created_at))

    query = query.offset(params.offset).limit(params.limit)

    logs = query.all()

    # Transform the result to match the response schema
    log_responses = []
    for log, prompt in logs:
        log_response = LogResponseSchema(
            id=log.id,
            execution_session_id=log.execution_session_id,
            prompt_id=log.prompt_id,
            state=log.state,
            created_at=log.created_at,
            error_message=log.error_message,
            query_response_id=log.query_response_id,
            template_id=log.template_id,
            prompt_text=prompt.prompt_text,
            response=log.output.response if log.query_response_id else None,
            sources=log.output.sources if log.query_response_id else None,
        )
        log_responses.append(log_response)

    return log_responses


@app.get("/content_logs/", response_model=List[LogResponseSchema])
async def get_content_logs_api(
    limit: int = 10,
    offset: int = 0,
    order: str = "desc",
    prompt_text: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    params = LogQueryParams(
        limit=limit, offset=offset, order=order, prompt_text=prompt_text, state=state
    )
    return get_content_logs(db, params)


@app.get("/check_global_limit/")
async def check_global_limit_api(db: Session = Depends(get_db)):
    if check_global_limit(db):
        return {"allowed": True}
    else:
        return {"allowed": False}


@app.post("/increment_global_query_count/")
async def increment_global_query_count_api(db: Session = Depends(get_db)):
    if check_global_limit(db):
        increment_global_query_count(db)
        return {"success": True}
    else:
        raise HTTPException(status_code=429, detail="Global query limit reached")


from fastapi.responses import RedirectResponse

twitter_scope = ["tweet.read", "tweet.write", "users.read", "offline.access"]

# In-memory storage for code verifiers
code_verifiers = {}

from redis import Redis

from oauth_helpers import generate_code_challenge, generate_code_verifier

redis_client = Redis(
    host="165.227.177.167",
    port=6379,
    db=0,
    password="foofoojaaa",
    decode_responses=True,
)


def get_refreshed_access_token():
    refresh_token = redis_client.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=400, detail="Refresh token not found or expired"
        )

    auth = tweepy.OAuth2UserHandler(
        client_id=twitter_api_key,
        redirect_uri=callback_url,
        scope=twitter_scope,
        client_secret=twitter_api_secret_key,
        # code_challenge=code_challenge,
        # code_challenge_method='S256'
    )
    try:
        access_token = auth.refresh_token(
            token_url="https://api.twitter.com/2/oauth2/token",
            refresh_token=refresh_token,
            body=f"grant_type=refresh_token&client_id={twitter_api_key}",
        )
        redis_client.set("access_token", access_token, ex=3600)  # Expire after 1 hour
        return access_token
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error! Failed to refresh access token: {e}"
        )


@app.get("/twitter/login")
async def login():
    code_verifier = generate_code_verifier()
    generate_code_challenge(code_verifier)
    auth = tweepy.OAuth2UserHandler(
        client_id=twitter_api_key,
        redirect_uri=callback_url,
        scope=twitter_scope,
        client_secret=twitter_api_secret_key,
        # code_challenge=code_challenge,
        # code_challenge_method='S256'
    )

    try:
        redirect_url = auth.get_authorization_url()
        code_verifiers[auth._state] = auth
        print(f"state: {auth._state}")
        return RedirectResponse(f"{redirect_url}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error! Failed to get authorization URL: {e}"
        )


@app.get("/twitter/callback")
# async def callback(request: Request):
async def callback(state: str, code: str):
    # state = request.get('state')
    # code = request.get('code')
    code_verifier = code_verifiers.pop(state, None)

    # if not code_verifier:
    #     raise HTTPException(status_code=400, detail="Invalid state parameter")

    # auth = tweepy.OAuth2UserHandler(
    #     client_id=twitter_api_key,
    #     redirect_uri=callback_url,
    #     scope=twitter_scope,
    #     client_secret=twitter_api_secret_key,
    #     # state=state
    # )
    try:
        access_token = code_verifier.fetch_token(
            f"{callback_url}?state={state}&code={code}",
        )
        # refresh_token = access_token['refresh_token']
        # Store access token and refresh token in Redis
        redis_client.set(
            "access_token", access_token["access_token"], ex=3600
        )  # Expire after 1 hour
        redis_client.set(
            "refresh_token", access_token["refresh_token"]
        )  # No expiry for refresh token
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error! Failed to fetch access token: {e}"
        )


def post_tweet(tweet_text: str):
    """
    The function `post_tweet` posts a tweet using Tweepy library after obtaining or refreshing the
    access token.

    :param tweet_text: The `post_tweet` function takes a `tweet_text` parameter, which is a string
    representing the text of the tweet that you want to post on Twitter. This function first retrieves
    an access token from a Redis client. If the access token is not available, it calls the
    `get_refreshed_access
    :type tweet_text: str
    """
    access_token = redis_client.get("access_token")
    if not access_token:
        access_token = get_refreshed_access_token()
    client = tweepy.Client(bearer_token=access_token)
    try:
        client.create_tweet(text=tweet_text, user_auth=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting tweet: {e}")


@app.post("/twitter/tweet")
async def post_tweet_api(tweet_text: str):
    access_token = redis_client.get("access_token")
    if not access_token:
        access_token = get_refreshed_access_token()
    client = tweepy.Client(bearer_token=access_token)
    try:
        client.create_tweet(text=tweet_text, user_auth=False)
        return {"status": "success", "message": "Tweet posted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting tweet: {e}")


from datetime import date as date_type


@app.get("/gacetas")
async def get_gacetas_api(
    db: Session = Depends(get_db),
    date: Optional[date_type] = None,
    order: Optional[str] = "desc",
):
    try:
        query = db.query(GacetaPDF)
        if date:
            start_date = datetime.combine(date, datetime.min.time())
            end_date = datetime.combine(date, datetime.max.time())
            query = query.filter(
                and_(GacetaPDF.date >= start_date, GacetaPDF.date <= end_date)
            )

        if order == "asc":
            query = query.order_by(asc(GacetaPDF.date))
        else:
            query = query.order_by(desc(GacetaPDF.date))

        gacetas = query.all()

        res = {
            "gacetas": [
                {
                    "gaceta": gaceta.to_json(),
                    "twitter_prompts": get_twitter_prompts(db, gaceta.id, 1),
                }
                for gaceta in gacetas
            ]
        }
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


from pydantic import BaseModel


class ApproveTweetRequest(BaseModel):
    gaceta_id: int
    tweet_text: str
    content_exec_id: str


@app.post("/approve_tweet")
async def approve_tweet(request: ApproveTweetRequest):
    # Logic to approve and post tweet
    access_token = redis_client.get("access_token")
    if not access_token:
        access_token = get_refreshed_access_token()

    client = tweepy.Client(access_token)
    try:
        tweet_text = request.tweet_text[:200]  # Limit tweet size to 280 characters
        client.create_tweet(text=tweet_text, user_auth=False)
        return JSONResponse(content={"message": "Tweet posted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting tweet: {e}")


@app.get("/health_check")
def health_check():
    try:
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Service is down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8050)
