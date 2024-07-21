

import pytz
import streamlit as st
from models import *
import os
from models import Prompt
from pdf_processor import PDFProcessor
from faiss_helper import FAISSHelper
from logging_setup import setup_logging
from config import config
from qa import get_llm, query_folder


from stream.api import *
setup_logging()

import streamlit_antd_components as sac

import streamlit as st
from datetime import datetime, timedelta
from models import *
from db import get_db
from pytz import timezone


def get_and_display_execution_session(session_id):
    try:
        logs = get_last_execution_session(session_id)
        for log in logs:
            st.divider()
            st.markdown(f" ### {log['name']}")
            st.markdown(f" #### {log['short_description']}")
            st.markdown(f"{log['response']}")
            with st.expander("sources"):
                st.write(f"Sources: {log['sources']}")
    except Exception as e:
        st.error(str(e))

def main():
    st.title("Daily Gaceta of Costa Rica Chatbot")
    
    user_id = 1  # Example user_id, should be dynamic in real use case
    template_id = 1  # Example template_id, should be dynamic in real use case
    available_days = list_available_index_days()
    available_days_str = [day.split('T')[0] for day in available_days]
    # let's make sure the session_state.date actually is in the available days
    if st.session_state.date not in available_days_str:
        st.session_state.date = available_days_str[-1]
    selected_day = st.sidebar.selectbox("Select a Day", available_days_str, index = available_days_str.index(st.session_state.date))
    st.session_state.date = selected_day
    st.sidebar.write(selected_day)
    session = get_execution_session_by_date(selected_day)
    session_id = session['id']
    st.header("Today's Processed Prompts")
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
    
    
main()