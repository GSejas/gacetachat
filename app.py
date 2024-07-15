
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

# db_session = next(get_db())

def main():
    st.title("Daily Gaceta of Costa Rica Chatbot")
    
    user_id = 1  # Example user_id, should be dynamic in real use case
    template_id = 1  # Example template_id, should be dynamic in real use case
    
    tab1, tab2, tab3, tab4 = st.tabs(["Today's Processed Prompts", "Chat with Today's PDF", "Admin", "Exec Logs"])
    with tab1:
        if st.button("Load Today's Prompts"):
            if st.button("Process Today's Prompts"):
                session_id = execute_daily_prompts(user_id, template_id)
                st.success("Today's prompts have been processed.")
            # if not check_today_processed():
            #     if st.button("Process Today's Prompts"):
            #         session_id = execute_daily_prompts(user_id, template_id)
            #         st.success("Today's prompts have been processed.")
            # else:
            #     session_id = get_today_session_id()
            #     display_processed_prompts(session_id)
            # if st.checkbox("Show Successful Sessions"):
            successful_sessions = get_successful_sessions()
            for session in successful_sessions:
                st.header(f"Session ID: {session.id}")
                st.subheader(f"Completed At: {session.completed_at}")
                st.subheader(f"status: {session.status}")
                st.markdown("#### **Prompts**:")
                display_last_execution_session(session.id)

    with tab2:
        pass
        # st.subheader("Chat with Today's PDF")
        # query = st.text_input("Enter your question:")
        # if st.button("Submit"):
        #     embeddings = OpenAIEmbeddings()
        #     index, documents = process_latest_pdf()
        #     if index and documents:
        #         answer = search_in_pdf(query, index, documents, embeddings)
        #         st.write(answer)

    with tab3:
        pass
        # st.subheader("Admin: Add Prompt Template")
        # template_title = st.text_input("Template Title")
        # template_description = st.text_area("Template Description")
        # if st.button("Add Template"):
        #     add_prompt_template(template_title, template_description)
        #     st.success("Template added successfully.")
            
    with tab4:
        st.sidebar.subheader("Admin: Prompt Execution Logs")
        # limit = st.sidebar.number_input("Limit", min_value=1, max_value=10, value=3, step=1, key="limit")
        if st.button("Load Recent Execution Logs"):
            limit = st.sidebar.number_input("Limit", min_value=1, max_value=10, value=3, step=1, key="limit")
            display_recent_exec_logs(limit)
        # display_recent_exec_logs(limit)
        
@st.cache_data(show_spinner=False)
def get_successful_sessions():
    db_session = next(get_db()) 
    sessions = db_session.query(ExecutionSession).filter(
        ExecutionSession.status == ExecutionState.EXECUTED.value,
            ).order_by(ExecutionSession.created_at.desc()).limit(3).all()
    return sessions

@st.cache_data(show_spinner=False)
def check_today_processed():
    db_session = next(get_db()) 
    today = datetime.now(timezone('America/Costa_Rica')).date()
    session = db_session.query(ExecutionSession).filter(
        ExecutionSession.created_at >= today,
        ExecutionSession.created_at < today + timedelta(days=1)
    ).first()
    return session is not None

@st.cache_data(show_spinner=False)
def get_today_session_id():
    db_session = next(get_db()) 
    today = datetime.now(timezone('America/Costa_Rica')).date()
    session = db_session.query(ExecutionSession).filter(
        ExecutionSession.created_at >= today,
        ExecutionSession.created_at < today + timedelta(days=1)
    ).first()
    return session.id if session else None

def add_prompt_template(title, description):
    db_session = next(get_db()) 
    new_template = ContentTemplate(title=title, description=description)
    db_session.add(new_template)
    db_session.commit()


# @st.cache_data
# def get_session_exec_logs(session_id):
#     db_session = next(get_db()) 
#     return db_session.query(ContentExecutionLog).filter_by(execution_session_id=session_id).all()
@st.cache_data(show_spinner=False)
def display_recent_exec_logs(limit=3):
    db_session = next(get_db())  # Initialize database session
    
    # Query the most recent content execution logs
    recent_logs = db_session.query(ContentExecutionLog).order_by(ContentExecutionLog.created_at.desc()).limit(limit).all()
    
    for log in recent_logs:
        st.divider()
        
        st.write(f"Prompt: {log.prompt.prompt_text}")
        # Add expander that holds the raw prompt
        st.json(log.to_json())
            
        if log.output:
            st.write(f"id: {log.id}")
            st.write(f"state: {log.state}")
            st.write(f"Response: {log.output.response}")
            st.write(f"Sources: {log.output.sources}")
            
            with st.expander("Raw Prompt"):
                st.write(log.output.raw_prompt)
        else:
            st.write("Response: N/A")
            st.write("Sources: N/A")

        # Assuming re-run functionality is similar to the existing one
        if st.button(f"Re-run Prompt {log.prompt.id}", key=f"rere_run_{log.id}_{log.id}_{log.execution_session_id}_{log.prompt.id}"):
            re_run_prompt(log.prompt.id, log.execution_session_id)

from sqlalchemy.orm import Session
# from .models import ContentExecutionLog, ExecutionState
def get_last_executed_log(db_session, prompt_id):
    db_session = next(get_db()) 
    return db_session.query(ContentExecutionLog)\
        .filter(ContentExecutionLog.state == ExecutionState.EXECUTED.value, ContentExecutionLog.prompt_id == prompt_id, ContentExecutionLog.query_response_id != None)\
        .order_by(ContentExecutionLog.created_at.desc())\
        .first()

def display_last_execution_session(session_id):
    db_session = next(get_db()) 
    import random
    
    exec_session = db_session.query(ExecutionSession).filter_by(id=session_id).first() #.limit(3).all() 
    content_template = exec_session.content_template
    # indx = sac.tabs([
    #     sac.TabsItem(label=f"{idx}", tag="10") for idx, log in enumerate(logs)
    # ], align='center', key=f"{session_id}", return_index=True)

    for prompts in content_template.prompts:
        log = get_last_executed_log(db_session, prompts.id)
        # for log in logs:
            
        st.divider()
        
        st.write(f"Prompt: {log.prompt.prompt_text[:35]}...")
        # add expander that holds the raw prompt
            
        if log.output:
            st.write(f"Response: {log.output.response}")
            with st.expander("sources"):
                st.write(f"sources: {log.output.sources}")
            
            with st.expander("Raw Prompt"):
                st.write(log.output.raw_prompt)
        else:
            st.write("Response: N/A")
            st.write("sources: N/A")

            if st.button(f"Re-run Prompt {log.prompt.id}", key=f"re_run_{log.id}_{log.execution_session_id}_{log.prompt.id}_{random.randint(1, 100)}"):
                re_run_prompt(log.prompt.id, log.execution_session_id)
                st.success(f"Prompt {log.prompt.id} re-executed successfully.")

        st.divider()

def process_latest_pdf():
    # Implement your logic to process the latest PDF and return the index and documents
    pass

def search_in_pdf(query, index, documents, embeddings):
    # Implement your logic to search in the PDF
    pass

def execute_daily_prompts(user_id, template_id):
    db_session = next(get_db()) 
    session_id = create_execution_session(user_id, template_id)
    prompts = db_session.query(Prompt).filter_by(template_id=template_id).all()
    for prompt in prompts:
        try:
            response_text = run_prompt_by_date(prompt.prompt_text)  # Function to execute the prompt
            log = log_prompt_execution(session_id, prompt.id, ExecutionState.EXECUTED.value)
            query = PromptQueryResponse(
                raw_prompt=response_text['partial'].format(), 
                response=response_text['answer'], 
                prompt_template_id=prompt.id,   
                sources=str(response_text['sources'])
            )
            
            db_session.add(query)
            db_session.commit()
            
            log.query_response_id = query.id
            log.execution_session_id = session_id
            log.template_id = template_id
            db_session.commit()
    
        except Exception as e:
            log = log_prompt_execution(session_id, prompt.id, ExecutionState.FAILED.value, error_message=str(e))
    session = db_session.query(ExecutionSession).filter_by(id=session_id).first()
    session.status = ExecutionState.EXECUTED.value
    session.completed_at = datetime.now(timezone('America/Costa_Rica'))
    db_session.commit()
    return session_id


def re_run_prompt(prompt_id, session_id):
    db_session = next(get_db()) 
    prompt = db_session.query(Prompt).filter_by(id=prompt_id).first()
    if prompt:
        try:
            response_text = run_prompt_by_date(prompt.prompt_text)
            query = PromptQueryResponse(
                raw_prompt=response_text['partial'].format(), 
                response=response_text['answer'], 
                prompt_template_id=prompt.id, 
                sources=str(response_text['sources'])
            )
            db_session.add(query)
            db_session.commit()
            
            log = log_prompt_execution(session_id, prompt.id, ExecutionState.EXECUTED.value, query_response_id=query.id, template_id=prompt.template_id)
            # log.query_response_id = query.id
            # log.execution_session_id = session_id
            # log.template_id = prompt.template_id
            # db_session.commit()
    
        except Exception as e:
            log_prompt_execution(session_id, prompt.id, ExecutionState.FAILED.value, error_message=str(e))


def run_prompt_by_date(query, date=datetime.strptime(datetime.now(pytz.timezone('America/Costa_Rica')).strftime("%Y-%m-%d"), "%Y-%m-%d")):
    db_session = next(get_db()) 
    
    existing_gaceta = db_session.query(GacetaPDF).filter_by(date=date).first()
    if existing_gaceta:
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
    return None

def create_execution_session(user_id, template_id):
    db_session = next(get_db()) 
    new_session = ExecutionSession(
        content_template_id=template_id,
        user_id=user_id,
        status=ExecutionState.INIT.value,
        created_at=datetime.now(timezone('America/Costa_Rica'))
    )
    db_session.add(new_session)
    db_session.commit()
    return new_session.id
   
def log_prompt_execution(session_id, prompt_id, state, error_message=None, **kwargs) -> ContentExecutionLog:
    db_session = next(get_db()) 
    log_entry = ContentExecutionLog(
        execution_session_id=session_id,
        prompt_id=prompt_id,
        state=state,
            error_message=error_message,
            **kwargs
    )
    db_session.add(log_entry)
    db_session.commit()
    return log_entry
    
    

if __name__ == "__main__":
    main()
