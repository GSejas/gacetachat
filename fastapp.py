# from services.counter import check_global_limit, increment_global_query_count
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from pytz import timezone
from db import get_db
from models import ExecutionSession, ExecutionState, ContentTemplate, ContentExecutionLog, Prompt, PromptQueryResponse, GacetaPDF

from models import *
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from typing import List
from models import Prompt
from logging_setup import setup_logging
from config import config
from services.counter import increment_global_query_count, check_global_limit
import tweepy

setup_logging()

import streamlit_antd_components as sac

import streamlit as st
from datetime import datetime, timedelta
from models import *
from db import get_db
from langchain_openai import OpenAIEmbeddings
from pytz import timezone
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Replace these with your personal account's credentials
twitter_api_key = os.getenv("TWITTER_API_KEY")
twitter_api_secret_key = os.getenv("TWITTER_API_secret_key")


twitter_consumer_api_key = os.environ.get("TWITTER_CONSUMER_API_KEY")
twitter_consumer_api_secret_key = os.environ.get("TWITTER_CONSUMER_API_secret_key")

callback_url = 'https://c470-186-176-232-195.ngrok-free.app/twitter/callback'

from dotenv import load_dotenv
API_KEY = os.environ.get("APP_SECRET_API_KEY")


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import *
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse

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
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        exec_sessions = get_execution_session_by_date(db, date_obj)
        if exec_sessions:
            return exec_sessions
        else:
            raise HTTPException(status_code=404, detail="Execution session not found for the given date")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, should be YYYY-MM-DD")

@app.get("/execution_session/available/")
async def list_available_index_days_api(db: Session = Depends(get_db)):
    days = list_available_index_days(db)
    return [day[0] for day in days]

@app.post("/execute_daily_prompts/")
async def execute_daily_prompts(user_id: int, template_id: int, db: Session = Depends(get_db)):
    session_id = create_execution_session(db, user_id, template_id)
    prompts = db.query(Prompt).filter_by(template_id=template_id).all()
    for prompt in prompts:
        try:
            response_text = run_prompt_by_date(prompt.prompt_text, db)  # Function to execute the prompt
            log = log_prompt_execution(session_id, prompt.id, ExecutionState.EXECUTED.value, db)
            query = PromptQueryResponse(
                raw_prompt=response_text['partial'].format(), 
                response=response_text['answer'], 
                prompt_template_id=prompt.id,   
                sources=str(response_text['sources'])
            )
            
            db.add(query)
            db.commit()
            
            log.query_response_id = query.id
            log.execution_session_id = session_id
            log.template_id = template_id
            db.commit()
    
        except Exception as e:
            log_prompt_execution(session_id, prompt.id, ExecutionState.FAILED.value, str(e), db)
    session = db.query(ExecutionSession).filter_by(id=session_id).first()
    session.status = ExecutionState.EXECUTED.value
    session.completed_at = datetime.now(timezone('America/Costa_Rica'))
    db.commit()
    return {"session_id": session_id}



@app.get("/execution_session/", response_model=List[dict])
async def execution_session_api(session_id: str, db: Session = Depends(get_db)):
    logs = display_last_execution_session(db, session_id)
    return logs


from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, asc
# from . import models, schemas
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

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
    query = db.query(models.ContentExecutionLog).join(models.Prompt).add_entity(models.Prompt)

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
            response=log.output.response if log.query_response_id  else None,
            sources=log.output.sources if log.query_response_id  else None
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
    db: Session = Depends(get_db)
):
    params = LogQueryParams(
        limit=limit,
        offset=offset,
        order=order,
        prompt_text=prompt_text,
        state=state
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

from oauth_helpers import generate_code_challenge, generate_code_verifier

from redis import Redis

redis_client = Redis(
    host="165.227.177.167", port=6379, db=0, password='foofoojaaa', decode_responses=True
)


def get_refreshed_access_token():
    refresh_token = redis_client.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token not found or expired")
    
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
        raise HTTPException(status_code=500, detail=f"Error! Failed to refresh access token: {e}")



@app.get("/twitter/login")
async def login():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
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
        code_verifiers[auth._state ] = auth
        print(f"state: {auth._state}")
        return RedirectResponse(f"{redirect_url}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error! Failed to get authorization URL: {e}")

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
        redis_client.set("access_token", access_token['access_token'], ex=3600)  # Expire after 1 hour
        redis_client.set("refresh_token", access_token['refresh_token'])  # No expiry for refresh token
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error! Failed to fetch access token: {e}")


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
async def get_gacetas(db: Session = Depends(get_db), date: Optional[date_type] = None, order: Optional[str] = "desc"):
    try:
        query = db.query(GacetaPDF)
        if date:
            start_date = datetime.combine(date, datetime.min.time())
            end_date = datetime.combine(date, datetime.max.time())
            query = query.filter(and_(GacetaPDF.date >= start_date, GacetaPDF.date <= end_date))
        
        if order == "asc":
            query = query.order_by(asc(GacetaPDF.date))
        else:
            query = query.order_by(desc(GacetaPDF.date))
        
        gacetas = query.all()

        res = {
            "gacetas": [
                {
                    "gaceta": gaceta.to_json(),
                    "twitter_prompts": get_twitter_prompts(db, gaceta.id, 1)
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
