from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pytz import timezone
from models import *

from pdf_processor import PDFProcessor
from faiss_helper import FAISSHelper
from logging_setup import setup_logging
from config import config
from qa import get_llm, query_folder
import traceback
import os
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException

def get_last_executed_log(db: Session, prompt_id: int):
    try:
        return db.query(ContentExecutionLog)\
            .filter(ContentExecutionLog.state == ExecutionState.EXECUTED.value, ContentExecutionLog.prompt_id == prompt_id, ContentExecutionLog.query_response_id != None)\
            .order_by(ContentExecutionLog.created_at.desc())\
            .first()
    except NoResultFound:
        return None

def display_last_execution_session(db: Session, session_id: str):
    try:
        exec_session = db.query(ExecutionSession).filter_by(id=session_id).one()
        content_template = exec_session.content_template
        logs = []
        for prompt in content_template.prompts:
            log = get_last_executed_log(db, prompt.id)
            if log:
                logs.append({
                    "name": log.prompt.name,
                    "short_description": log.prompt.short_description,
                    "prompt_text": log.prompt.prompt_text,
                    "response": log.output.response if log.query_response_id else None,
                    "sources": log.output.sources if log.query_response_id else None,
                    "raw_prompt": log.output.raw_prompt if log.query_response_id else None,
                    "prompt_id": log.prompt.id,
                    "execution_session_id": log.execution_session_id
                })
        return logs
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Execution session not found")


def execute_content_template_prompts(db: Session, user_id: int, template_id: int, gaceta_id=None):
    session_id = create_execution_session(db, user_id, template_id, gaceta_id)
    prompts = db.query(Prompt).filter_by(template_id=template_id).all()
    for prompt in prompts:
        try:
            response_text = run_prompt_by_date(prompt.prompt_text)
            query = PromptQueryResponse(
                raw_prompt=response_text['partial'].format(), 
                response=response_text['answer'], 
                prompt_template_id=prompt.id,   
                sources=str(response_text['sources'])
            )
            db.add(query)
            db.commit()
            log = log_prompt_execution(db, session_id, prompt.id, ExecutionState.EXECUTED.value, query_response_id=query.id, template_id=prompt.template_id)
        except Exception as e:
            error_message = f"{str(e)}\n\n{traceback.format_exc()}"
            log = log_prompt_execution(db, session_id, prompt.id, ExecutionState.FAILED.value, error_message=error_message)
    session = db.query(ExecutionSession).filter_by(id=session_id).first()
    # session.status = ExecutionState.EXECUTED.value
    # session.completed_at = datetime.now(timezone('America/Costa_Rica'))

    # Check if all prompts have been executed successfully
    prompts = session.content_template.prompts
    all_executed = all(get_last_executed_log(db, prompt.id) is not None for prompt in prompts)
    if all_executed:
        session.status = ExecutionState.EXECUTED.value
        session.completed_at = datetime.now(timezone('America/Costa_Rica'))
    else:
        session.status = ExecutionState.FAILED.value
        session.completed_at = None

    db.commit()
    return session_id

def re_run_prompt(db: Session, prompt_id: int, session_id: int):
    prompt = db.query(Prompt).filter_by(id=prompt_id).first()
    if prompt:
        try:
            response_text = run_prompt_by_date(prompt.prompt_text)
            query = PromptQueryResponse(
                raw_prompt=response_text['partial'].format(), 
                response=response_text['answer'], 
                prompt_template_id=prompt.id, 
                sources=str(response_text['sources'])
            )
            db.add(query)
            db.commit()
            log = log_prompt_execution(db, session_id, prompt.id, ExecutionState.EXECUTED.value, query_response_id=query.id, template_id=prompt.template_id)
        except Exception as e:
            log_prompt_execution(db, session_id, prompt.id, ExecutionState.FAILED.value, error_message=str(e))

def create_execution_session(db: Session, user_id: int, template_id: int, gaceta_id:int):
    new_session = ExecutionSession(
        content_template_id=template_id,
        user_id=user_id,
        status=ExecutionState.INIT.value,
        created_at=datetime.now(timezone('America/Costa_Rica')),
        document_id=gaceta_id
    )
    db.add(new_session)
    db.commit()
    return new_session.id

def log_prompt_execution(db: Session, session_id: int, prompt_id: int, state: str, error_message: str = None, **kwargs):
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

def run_prompt_by_date(query: str, date: datetime = datetime.now(timezone('America/Costa_Rica')).date()):
    faiss_helper = FAISSHelper()
    latest_gaceta_dir = os.path.join(config.GACETA_PDFS_DIR, datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d"))
    
    # Placeholder function for running the prompt. Replace with actual logic.
    if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
        db = faiss_helper.load_faiss_index(latest_gaceta_dir)
            
        llm = get_llm(model=config.OPENAI_MODEL_NAME, openai_api_key=config.OPENAI_API_KEY, temperature=config.OPENAI_TEMPERATURE)
        result = query_folder(
            folder_index=db,
            query=query,
            llm=llm,
        )
        
        return result


def get_execution_session_by_date(db: Session, date: datetime):
    return db.query(ExecutionSession).filter(
        ExecutionSession.created_at >= date,
        ExecutionSession.created_at < date + timedelta(days=1),
        ExecutionSession.status == ExecutionState.EXECUTED.value
    ).first()


def list_available_index_days(db: Session):
    return db.query(GacetaPDF.date.desc()).distinct().all()
