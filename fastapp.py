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
# app.py
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

@app.post("/execute_daily_prompts/")
async def execute_daily_prompts(user_id: int, template_id: int, db: Session = Depends(get_db)):
    session_id = create_execution_session(user_id, template_id, db)
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

@app.get("/successful_sessions/")
async def get_successful_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ExecutionSession).filter(
        ExecutionSession.status == ExecutionState.EXECUTED.value,
    ).order_by(ExecutionSession.created_at.desc()).all()
    return sessions

@app.get("/recent_exec_logs/")
async def get_recent_exec_logs(limit: int = 3, db: Session = Depends(get_db)):
    recent_logs = db.query(ContentExecutionLog).order_by(ContentExecutionLog.created_at.desc()).limit(limit).all()
    return recent_logs

def create_execution_session(user_id: int, template_id: int, db: Session) -> int:
    new_session = ExecutionSession(
        content_template_id=template_id,
        user_id=user_id,
        status=ExecutionState.INIT.value,
        created_at=datetime.now(timezone('America/Costa_Rica'))
    )
    db.add(new_session)
    db.commit()
    return new_session.id

def log_prompt_execution(session_id: int, prompt_id: int, state: str, db: Session, error_message: str = None, **kwargs) -> ContentExecutionLog:
    log_entry = ContentExecutionLog(
        execution_session_id=session_id,
        prompt_id=prompt_id,
        state=state,
        error_message=error_message,
        **kwargs
    )
    db.add(log_entry)
    db.commit()
    return log_entry

def run_prompt_by_date(query: str, db: Session, date: datetime = datetime.now(timezone('America/Costa_Rica')).date()):
    existing_gaceta = db.query(GacetaPDF).filter_by(date=date).first()
    if existing_gaceta:
        faiss_helper = FAISSHelper()
        latest_gaceta_dir = os.path.join(config.GACETA_PDFS_DIR, date.strftime("%Y-%m-%d"))
        
        if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
            db = faiss_helper.load_faiss_index(latest_gaceta_dir)
            llm = get_llm(model=config.OPENAI_MODEL_NAME, openai_api_key=config.OPENAI_API_KEY, temperature=config.OPENAI_TEMPERATURE)
            result = query_folder(folder_index=db, query=query, llm=llm)
            return result
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8005)
