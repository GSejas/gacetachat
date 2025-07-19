import os
import traceback
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from config import config
from faiss_helper import FAISSHelper
from models import *
from qa import get_llm, query_folder


def get_last_executed_log(db: Session, prompt_id: int, session_id):
    try:
        return (
            db.query(ContentExecutionLog)
            .filter(
                ContentExecutionLog.state == ExecutionState.EXECUTED.value,
                ContentExecutionLog.execution_session_id == session_id,
                ContentExecutionLog.prompt_id == prompt_id,
                ContentExecutionLog.query_response_id != None,
            )
            .order_by(ContentExecutionLog.created_at.desc())
            .first()
        )
    except NoResultFound:
        return None


def get_twitter_prompts(db: Session, gaceta_id: int, twitter_prompt_id):
    try:
        gaceta = db.query(GacetaPDF).filter_by(id=gaceta_id).one()
        exec_session = gaceta.exec_sess
        exec = []
        if exec_session:
            for session in exec_session:
                logs = []
                content_exec_logs = session.logs
                for exec_log in content_exec_logs:
                    if exec_log.prompt_id == twitter_prompt_id:
                        logs.append(
                            {
                                "id": exec_log.id,
                                "name": exec_log.prompt.name,
                                "state": exec_log.state,
                                "short_description": exec_log.prompt.short_description,
                                "prompt_text": exec_log.prompt.prompt_text,
                                "response": (
                                    exec_log.output.response
                                    if exec_log.query_response_id
                                    else None
                                ),
                                "sources": (
                                    exec_log.output.sources
                                    if exec_log.query_response_id
                                    else None
                                ),
                                "raw_prompt": (
                                    exec_log.output.raw_prompt
                                    if exec_log.query_response_id
                                    else None
                                ),
                                "prompt_id": exec_log.prompt.id,
                                "execution_session_id": exec_log.execution_session_id,
                            }
                        )
                exec.append(
                    {
                        "exec_session": session.to_json() if session else None,
                        "logs": logs,
                    }
                )
        return exec
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Execution session not found")


import logging


def display_last_execution_session(db: Session, session_id: str):
    try:
        logging.info(f"Fetching execution session with ID: {session_id}")
        exec_session = db.query(ExecutionSession).filter_by(id=session_id).one()
        content_template = exec_session.content_template
        logs = []
        all_prompts = (
            db.query(Prompt).filter(Prompt.template_id == content_template.id).all()
        )

        for prompt in all_prompts:
            log = get_last_executed_log(db, prompt.id, session_id)
            if log:
                logs.append(
                    {
                        "name": log.prompt.name,
                        "short_description": log.prompt.short_description,
                        "prompt_text": log.prompt.prompt_text,
                        "response": (
                            log.output.response if log.query_response_id else None
                        ),
                        "sources": (
                            log.output.sources if log.query_response_id else None
                        ),
                        "raw_prompt": (
                            log.output.raw_prompt if log.query_response_id else None
                        ),
                        "prompt_id": log.prompt.id,
                        "execution_session_id": log.execution_session_id,
                    }
                )
                logging.info(
                    f"Found executed log for prompt ID: {prompt.id} in session ID: {session_id}"
                )
            else:
                logs.append(
                    {
                        "name": prompt.name,
                        "short_description": prompt.short_description,
                        "prompt_text": prompt.prompt_text,
                        "response": "Ups! No hemos generado este prompt aun! Generalo con el UI!",
                        "sources": (
                            "No sources yet"
                            if prompt.doc_aware
                            else "No sources needed"
                        ),
                        "raw_prompt": prompt.prompt_text,
                        "prompt_id": prompt.id,
                        "execution_session_id": session_id,
                    }
                )
                logging.warning(
                    f"No executed log found for prompt ID: {prompt.id} in session ID: {session_id}"
                )

        return logs
    except NoResultFound:
        logging.error(f"Execution session not found for ID: {session_id}")
        raise HTTPException(status_code=404, detail="Execution session not found")


def get_scheduled_prompts(db: Session, template_id: int):
    return (
        db.query(Prompt)
        .filter(Prompt.template_id == template_id, Prompt.scheduled_execution == True)
        .all()
    )


def get_manual_prompts(db: Session, template_id: int):
    return (
        db.query(Prompt)
        .filter(Prompt.template_id == template_id, Prompt.scheduled_execution == False)
        .all()
    )


def get_execution_session_prompts_results(db: Session, session_id: str):
    session = db.query(ExecutionSession).filter_by(id=session_id).first()
    if not session:
        return {}
    prompt_results = {}
    for log in session.logs:
        if log.state == ExecutionState.EXECUTED.value and log.query_response_id:
            prompt_results[log.prompt.alias] = log.output.response
    return prompt_results


import os
import traceback
from datetime import datetime

from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session

from config import config
from faiss_helper import FAISSHelper
from models import (
    ContentExecutionLog,
    ExecutionSession,
    ExecutionState,
    Prompt,
    PromptQueryResponse,
)
from qa import get_llm, query_folder


class PromptExecutionEngine:
    def __init__(self, db: Session):
        self.db = db

    def run_prompt_by_date(self, query: str, **kargs):
        date = kargs.pop("date", None)
        if date is None:
            llm = get_llm(**kargs)
            result = llm.invoke(
                [
                    (
                        "system",
                        "You are an ai assistant, helping summarize and communicate simple news for the world and costa rica.",
                    ),
                    ("human", query),
                ]
            )
            return {
                "answer": result.content,
                "partial": query,
                "sources": [],
                "ai_references": None,
            }
            # return result

        faiss_helper = FAISSHelper()
        latest_gaceta_dir = os.path.join(
            config.GACETA_PDFS_DIR, date.strftime("%Y-%m-%d")
        )

        if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
            db = faiss_helper.load_faiss_index(latest_gaceta_dir)

            llm = get_llm(
                model=config.OPENAI_MODEL_NAME,
                openai_api_key=config.OPENAI_API_KEY,
                temperature=config.OPENAI_TEMPERATURE,
            )
            result = query_folder(
                folder_index=db,
                query=query,
                llm=llm,
            )
            return result

    def execute_prompt(
        self,
        prompt: Prompt,
        session_id: str,
        model: str = config.OPENAI_MODEL_NAME,
        temp: float = config.OPENAI_TEMPERATURE,
        max_tokens: int = config.OPENAI_MAX_TOKENS,
    ):
        prompt_text = prompt.prompt_text

        exec_session = self.db.query(ExecutionSession).filter_by(id=session_id).first()
        if not exec_session:
            return {}

        gaceta = exec_session.gaceta
        date = gaceta.date if gaceta else None

        prompt_results = self.get_execution_session_prompts_results(session_id)

        # Replace aliases with results from previous executions
        for alias, result in prompt_results.items():
            placeholder = f"{{{{{alias}}}}}"
            prompt_text = prompt_text.replace(placeholder, result)

        prompt_template = PromptTemplate.from_template(prompt_text)
        formatted_prompt = prompt_template.invoke({}).text

        return self.run_prompt_by_date(
            formatted_prompt,
            model=model,
            date=date if prompt.doc_aware else None,
            temperature=temp,
            max_tokens=max_tokens,
        )

    def get_prompts(self, template_id, re_execute):
        if re_execute:
            return self.db.query(Prompt).filter_by(template_id=template_id).all()
        return self.get_scheduled_prompts(template_id)

    def process_prompts(self, prompts, session_id):
        for prompt in prompts:
            try:
                self.execute_and_log_prompt(prompt, session_id)
            except Exception as e:
                self.log_execution_failure(prompt, session_id, e)

    def log_execution_failure(self, prompt, session_id, exception):
        error_message = f"{str(exception)}\n\n{traceback.format_exc()}"
        self.log_prompt_execution(
            session_id,
            prompt.id,
            ExecutionState.FAILED.value,
            error_message=error_message,
        )

    def execute_and_log_prompt(self, prompt, session_id):
        response_text = self.execute_prompt(prompt, session_id)
        query = PromptQueryResponse(
            raw_prompt=(
                response_text["partial"].format() if response_text["partial"] else None
            ),
            response=response_text["answer"],
            prompt_template_id=prompt.id,
            sources=str(response_text["sources"]),
        )
        self.db.add(query)
        self.db.commit()
        self.log_prompt_execution(
            session_id,
            prompt.id,
            ExecutionState.EXECUTED.value,
            query_response_id=query.id,
            template_id=prompt.template_id,
        )

    def update_session_status(self, session_id, prompts):
        session = self.db.query(ExecutionSession).filter_by(id=session_id).first()
        all_executed = all(
            get_last_executed_log(self.db, prompt.id, session_id) is not None
            for prompt in prompts
        )
        session.status = (
            ExecutionState.EXECUTED.value
            if all_executed
            else ExecutionState.FAILED.value
        )
        session.completed_at = datetime.now() if all_executed else None
        self.db.commit()

    def execute_content_template_prompts(
        self, user_id: int, template_id: int, gaceta_id=None, re_execute=False
    ):
        session_id = self.create_execution_session(user_id, template_id, gaceta_id)
        prompts = (
            self.get_scheduled_prompts(template_id)
            if not re_execute
            else self.db.query(Prompt).filter_by(template_id=template_id).all()
        )

        self.process_prompts(prompts, session_id)
        self.update_session_status(session_id, prompts)
        return session_id

    def re_execute_prompt(self, session_id: str, prompt_id: int, **kargs):
        prompt = self.db.query(Prompt).filter_by(id=prompt_id).first()
        if prompt:

            try:
                self.execute_and_log_prompt(prompt, session_id)
            except Exception as e:
                self.log_execution_failure(prompt, session_id, e)

    def get_execution_session_prompts_results(self, session_id: str):
        session = self.db.query(ExecutionSession).filter_by(id=session_id).first()
        if not session:
            return {}
        prompt_results = {}
        for log in session.logs:
            if log.state == ExecutionState.EXECUTED.value and log.query_response_id:
                prompt_results[log.prompt.alias] = log.output.response
        return prompt_results

    def create_execution_session(self, user_id: int, template_id: int, gaceta_id: int):
        new_session = ExecutionSession(
            content_template_id=template_id,
            user_id=user_id,
            status=ExecutionState.INIT.value,
            created_at=datetime.now(),
            document_id=gaceta_id,
        )
        self.db.add(new_session)
        self.db.commit()
        return new_session.id

    def log_prompt_execution(
        self,
        session_id: int,
        prompt_id: int,
        state: str,
        error_message: str = None,
        **kwargs,
    ):
        log_entry = ContentExecutionLog(
            execution_session_id=session_id,
            prompt_id=prompt_id,
            state=state,
            error_message=error_message,
            **kwargs,
        )
        self.db.add(log_entry)
        self.db.commit()
        return log_entry

    def get_scheduled_prompts(self, template_id: int):
        return (
            self.db.query(Prompt)
            .filter(
                Prompt.template_id == template_id, Prompt.scheduled_execution == True
            )
            .all()
        )


# Other CRUD functions remain unchanged

# def run_prompt_by_date(query: str, date: datetime = datetime.now(timezone('America/Costa_Rica')).date()):
#     faiss_helper = FAISSHelper()
#     latest_gaceta_dir = os.path.join(config.GACETA_PDFS_DIR, datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d"))

#     # Placeholder function for running the prompt. Replace with actual logic.
#     if os.path.exists(os.path.join(latest_gaceta_dir, "index.faiss")):
#         db = faiss_helper.load_faiss_index(latest_gaceta_dir)

#         llm = get_llm(model=config.OPENAI_MODEL_NAME, openai_api_key=config.OPENAI_API_KEY, temperature=config.OPENAI_TEMPERATURE)
#         result = query_folder(
#             folder_index=db,
#             query=query,
#             llm=llm,
#         )

#         return result


def get_execution_session_by_date(db: Session, date: datetime):
    query = db.query(GacetaPDF)
    if date:
        start_date = datetime.combine(date, datetime.min.time())
        end_date = datetime.combine(date, datetime.max.time())
        query = query.filter(
            and_(GacetaPDF.date >= start_date, GacetaPDF.date <= end_date)
        )

    gacetas = query.first()
    return gacetas.exec_sess
    # return db.query(ExecutionSession).filter(
    #     ExecutionSession.created_at >= date,
    #     ExecutionSession.created_at < date + timedelta(days=1),
    #     ExecutionSession.status == ExecutionState.EXECUTED.value
    # ).first()


def list_available_index_days(db: Session):
    return db.query(GacetaPDF.date.desc()).distinct().all()
