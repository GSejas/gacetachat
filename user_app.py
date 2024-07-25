
import pytz
import streamlit as st
from app import chat_with_document, display_recent_exec_logs, get_and_display_execution_session
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

import traceback
import random
import csv

from stream.api import *
setup_logging()

import streamlit_antd_components as sac

import streamlit as st
from datetime import datetime, timedelta
from models import *
from db import get_db
from langchain_openai import OpenAIEmbeddings
from pytz import timezone


# Initialize session state for itemid if not present
if 'date' not in st.session_state:
    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone('America/Costa_Rica')
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")
    st.session_state['date'] = date_str
    
    
# Check if redirected with a code
redirect_params = st.query_params
if 'date' in redirect_params:
    available_days = list_available_index_days()
    available_days_str = [day.split('T')[0] for day in available_days]
    date = redirect_params.get('date')
    if date in available_days_str:
        st.session_state.date = date
    else:
        st.warning("Invalid date selected. Please select a valid date.")
else:
    st.session_state.date = st.session_state.get('date', '')
    
admin_userid = 1

def ui_start_session(db, userid):
    my_expander_3 = st.expander(label='Session', expanded=True)
    with my_expander_3:
        # Option to start a new chat session
        if st.button("Start New Chat Session"):
            new_session = ExecutionSession(user_id=userid, status=ExecutionState.INIT.value)
            db.add(new_session)
            db.commit()
            st.session_state["current_session_id"] = new_session.id
        
            # Generate the initial message
            initial_message = "I'm a helpful ai reporting assistant, tasked with helping out extract information from the daily Gaceta of Costa Rica. How can I help you today?"
            initial_chat_message = ChatMessage(session_id=new_session.id, role="assistant", content=initial_message)
            db.add(initial_chat_message)
            db.commit()
            st.session_state.messages = [{"role": "assistant", "content": initial_message}]

        # Select an active chat session
        active_sessions = db.query(ExecutionSession).filter_by(user_id=userid, status=ExecutionState.INIT.value).all()
        session_id = st.selectbox("Select Chat Session", [sess.id for sess in active_sessions])

        if session_id:
            st.session_state["current_session_id"] = session_id

        
        if "current_session_id" in st.session_state:
            current_session = db.query(ExecutionSession).filter_by(id=st.session_state["current_session_id"]).first()
        else:
            current_session = None
        
        # Options to reset or archive chat sessions
        col1, col2 = st.columns(2)
        if col1.button("Delete Chat Session"):
            st.session_state.messages = []
            db.query(ExecutionSession).filter_by(session_id=current_session.id).delete()
            db.commit()

        if col2.button("Archive Chat Session"):
            current_session.status = ExecutionState.OUTDATED.value
            db.commit()
            st.session_state.pop("current_session_id", None)



def main():
    st.title("Daily Gaceta of Costa Rica Chatbot")
    
    user_id = None  # Example user_id, should be dynamic in real use case
    template_id = 1  # Example template_id, should be dynamic in real use case
    available_days = list_available_index_days()
    available_days_str = [day.split('T')[0] for day in available_days]
    selected_day = st.sidebar.selectbox("Select a Day", available_days_str, index = available_days_str.index(st.session_state.date))
    st.session_state.date = selected_day
    tab1, tab2, tab4 = st.tabs(["Today's Processed Prompts", "Chat with Today's PDF", "About"])
    with tab1:
        xec_sessions = get_execution_session_by_date(selected_day)
        session_ids = [session['id'] for session in xec_sessions]
        session_id = st.selectbox("Select Session", session_ids)
        # st.header(f"Session ID: {session_id}")
        st.header("Today's Processed Prompts")
        # Application description
        st.markdown("""
        ## How It Works
        This web application processes prompts based on the Daily Gaceta of Costa Rica and allows users to interact with the processed PDF of the day. 
        - **Today's Processed Prompts**: View and manage the prompts processed for today.
        - **Chat with Today's PDF**: Enter questions to search through today's PDF and get answers.
        - **Admin**: View detailed logs of prompt executions.
        """)
        # st.subheader(f"Completed At: {session['completed_at']}")
        # st.subheader(f"status: {session['status']}")
        get_and_display_execution_session(session_id)
    
    with tab2:
        db = next(get_db()) 
        
        with st.sidebar:

                ui_start_session(db, admin_userid)
                
                my_expander_1 = st.expander(label='ChatGPT Settings')  
                with my_expander_1:
                    st.session_state["openai_model"] = st.selectbox("Select OpenAI Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
                    temperature = st.slider("Select Temperature", 0.1, 1.0, 0.5, 0.1)
                    st.session_state["temperature"] = temperature


        if "current_session_id" in st.session_state:
            current_session = db.query(ExecutionSession).filter_by(id=st.session_state["current_session_id"]).first()
        else:
            current_session = None

        if current_session:
            messages = db.query(ChatMessage).filter_by(session_id=current_session.id).all()
            st.session_state.messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        else:
            st.session_state.messages = []


        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input new message
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = chat_with_document(
                    date=selected_day, 
                    query=prompt,
                    temperature=st.session_state.get("temperature", 0.5),
                    model=st.session_state.get("openai_model", "gpt-3.5-turbo"),
                    history=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ])
                st.markdown(response['answer'])

            st.session_state.messages.append({"role": "assistant", "content": response['answer']})

            # Save messages to the database
            user_message = ChatMessage(session_id=current_session.id, role="user", content=prompt)
            assistant_message = ChatMessage(session_id=current_session.id, role="assistant", content=response['answer'])
            db.add(user_message)
            db.add(assistant_message)
            db.commit()
            st.rerun()
        
    with tab4:
        st.sidebar.subheader("Admin: Prompt Execution Logs")
        limit = st.sidebar.number_input("Limit", min_value=1, max_value=10, value=3, step=1, key="limit")
        # if st.button("Load Recent Execution Logs"):
        display_recent_exec_logs(limit)
        

if __name__ == "__main__":
    main()
