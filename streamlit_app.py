import pytz
import streamlit as st

from logging_setup import setup_logging
from models import *
from stream.api import *

setup_logging()


from datetime import datetime

import streamlit as st

from db import get_db
from models import *

# Initialize session state for query count if not present
if "query_count" not in st.session_state:
    st.session_state["query_count"] = 0

# Initialize session state for itemid if not present
if "date" not in st.session_state:
    # Set the timezone to Costa Rica
    costa_rica_tz = pytz.timezone("America/Costa_Rica")
    current_time = datetime.now(costa_rica_tz)

    # Get the date string in the format "YYYY-MM-DD"
    date_str = current_time.strftime("%Y-%m-%d")
    st.session_state["date"] = date_str


# Check if redirected with a code
redirect_params = st.query_params
if "date" in redirect_params:
    available_days = list_available_index_days()
    available_days_str = [day.split("T")[0] for day in available_days]
    date = redirect_params.get("date")
    if date in available_days_str:
        st.session_state.date = date
    else:
        st.warning("Invalid date selected. Please select a valid date.")
else:
    st.session_state.date = st.session_state.get("date", "")

admin_userid = 1


def ui_start_session(db, userid):
    my_expander_3 = st.expander(label="Session", expanded=True)
    with my_expander_3:
        # Option to start a new chat session
        if st.button("Start New Chat Session"):
            new_session = ExecutionSession(
                user_id=userid, status=ExecutionState.INIT.value
            )
            db.add(new_session)
            db.commit()
            st.session_state["current_session_id"] = new_session.id

            # Generate the initial message
            initial_message = "I'm a helpful ai reporting assistant, tasked with helping out extract information from the daily Gaceta of Costa Rica. How can I help you today?"
            initial_chat_message = ChatMessage(
                session_id=new_session.id, role="assistant", content=initial_message
            )
            db.add(initial_chat_message)
            db.commit()
            st.session_state.messages = [
                {"role": "assistant", "content": initial_message}
            ]

        # Select an active chat session
        active_sessions = (
            db.query(ExecutionSession)
            .filter_by(user_id=userid, status=ExecutionState.INIT.value)
            .all()
        )
        session_id = st.selectbox(
            "Select Chat Session", [sess.id for sess in active_sessions]
        )

        if session_id:
            st.session_state["current_session_id"] = session_id

        if "current_session_id" in st.session_state:
            current_session = (
                db.query(ExecutionSession)
                .filter_by(id=st.session_state["current_session_id"])
                .first()
            )
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


import streamlit as st

from db import get_db

db = next(get_db())


def main():
    st.set_page_config(
        page_title="Gaceta AI Admin",
        page_icon="🧊",
        # layout="wide",
        initial_sidebar_state="expanded",
    )

    # Check the health of the service
    with st.spinner("Checking service health..."):
        service_healthy = check_health()

    if service_healthy:
        st.success("Service is up and running!")

        pages = {
            "Dashboard": [
                st.Page("mpages\\1_Home.py", title="Home"),
                st.Page("mpages\\2_Twitter.py", title="TwitterBot Integration"),
            ],
            "Admin": [
                st.Page("mpages\\3_Admin.py", title="App Logs"),
            ],
        }

        pg = st.navigation(pages)

        pg.run()

    else:
        st.error("Service is down. Please try again later.")
        st.markdown(
            """
            <style>
            .loader {
                border: 16px solid #f3f3f3;
                border-radius: 50%;
                border-top: 16px solid #3498db;
                width: 120px;
                height: 120px;
                -webkit-animation: spin 2s linear infinite; /* Safari */
                animation: spin 2s linear infinite;
            }

            /* Safari */
            @-webkit-keyframes spin {
                0% { -webkit-transform: rotate(0deg); }
                100% { -webkit-transform: rotate(360deg); }
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            <div class="loader"></div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
