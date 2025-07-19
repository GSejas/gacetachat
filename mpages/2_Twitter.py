import streamlit as st

from logging_setup import setup_logging
from models import *
from stream.api import *

setup_logging()


import streamlit as st

from models import *

tab5, tab6, tab7, tab8 = st.tabs(
    ["Tweet Integration", "Tweet Manager", "Gacetas", "Get User Data"]
)


with tab5:
    authenticate()
with tab6:
    post_tweet_form()
with tab7:
    list_gacetas()
# with tab8:
#     get_me()
