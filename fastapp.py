from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pytz import timezone
from db import get_db
from models import ExecutionSession, ExecutionState, ContentTemplate, ContentExecutionLog, Prompt, PromptQueryResponse, GacetaPDF
from process_pdf import process_latest_pdf, search_in_pdf

import pytz
import streamlit as st
from models import *
from process_pdf import process_latest_pdf, search_in_pdf
# from langchain_openai import OpenAIEmbeddings
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from typing import List
import streamlit as st
import os
from models import Prompt
from pdf_processor import PDFProcessor
from faiss_helper import FAISSHelper
from logging_setup import setup_logging
from config import config
from qa import get_llm, query_folder

setup_logging()

import streamlit_antd_components as sac

import streamlit as st
from datetime import datetime, timedelta
from models import *
from db import get_db
from langchain_openai import OpenAIEmbeddings
from pytz import timezone


app = FastAPI()


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import *
from datetime import datetime
from typing import List


@app.get("/execution_session_by_date/")
async def get_execution_session(date: str, db: Session = Depends(get_db)):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        session = get_execution_session_by_date(db, date_obj)
        if session:
            return session
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
from sqlalchemy import desc, asc
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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
