
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


tab5, tab6 , tab7= st.tabs(["Tweet Integration", "Tweet Manager", "Gacetas"])


with tab5:
    authenticate()
with tab6:
    post_tweet_form()
with tab7:
    list_gacetas()