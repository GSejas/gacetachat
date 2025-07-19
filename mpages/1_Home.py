import streamlit as st

from crud import PromptExecutionEngine
from logging_setup import setup_logging
from models import *
from stream.api import *

setup_logging()


import streamlit as st

from db import get_db
from models import *


def post_parse_markdown(text):
    import re

    # Pattern to match Markdown code blocks that start with ```markdown and end with ```
    pattern = r"```markdown\n([\s\S]*?)\n```"

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text, flags=re.DOTALL | re.MULTILINE)

    # If no matches are found, return the original text
    if not matches:
        return text

    return matches[0]


# Sidebar controls for model, maxtokens, and temperature
model = st.sidebar.selectbox(
    "Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], index=0
)  # Example model names, replace with actual
maxtokens = st.sidebar.number_input(
    "Max Tokens", min_value=1, max_value=2048 * 4, value=512
)
temperature = st.sidebar.number_input(
    "Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01
)


def get_and_display_execution_session(session_id):
    try:
        logs = get_last_execution_session(session_id)
        for log in logs:
            st.divider()
            st.markdown(f" ### {log['name']}")
            st.markdown(f" #### {log['short_description']}")
            st.markdown(post_parse_markdown(f"{log['response']}"))
            with st.expander("sources"):
                st.write(f"Sources: {log['sources']}")

            if st.button("Re-Run Prompt", key=f"re-run-prompt-{log['prompt_id']}"):
                prompt_execution_engine = PromptExecutionEngine(next(get_db()))
                prompt_execution_engine.re_execute_prompt(
                    session_id,
                    log["prompt_id"],
                    model=model,
                    temp=temperature,
                    max_tokens=maxtokens,
                )
                st.rerun()
    except Exception as e:
        st.error(str(e))


def run_execution_template(session, template_id, gaceta_id):
    prompt_execution_engine = PromptExecutionEngine(session)
    try:
        prompt_execution_engine.execute_content_template_prompts(
            None, template_id, gaceta_id=gaceta_id, re_execute=False
        )
        st.success("Execution template run successfully!")
    except Exception as e:
        st.error(f"Failed to run execution template: {e}")
    finally:
        session.close()


def main():
    st.title("Daily Gaceta of Costa Rica Chatbot")

    user_id = 1  # Example user_id, should be dynamic in real use case
    template_id = 1  # Example template_id, should be dynamic in real use case
    available_days = list_available_index_days()
    available_days_str = [day.split("T")[0] for day in available_days]
    # let's make sure the session_state.date actually is in the available days
    if st.session_state.date not in available_days_str:
        st.session_state.date = available_days_str[-1]
    selected_day = st.sidebar.selectbox(
        "Select a Day",
        available_days_str,
        index=available_days_str.index(st.session_state.date),
    )
    st.session_state.date = selected_day
    # st.sidebar.write(selected_day)

    tab1, tab2 = st.tabs(
        [":orange-background[Today's Processed Prompts]", "View Gaceta"]
    )

    try:
        with tab1:
            xec_sessions = get_execution_session_by_date(selected_day)
            if xec_sessions:
                session_options = {
                    f"Session {i+1} - ID: {session['id']}": session
                    for i, session in enumerate(xec_sessions)
                }
                selected_option = st.selectbox(
                    "Select a session",
                    options=list(session_options.keys()),
                    key="session-selection",
                )
                selected_session = session_options[selected_option]
                session_id = selected_session["id"]

                # Save the selected session ID in session state
                st.session_state["selected_session_id"] = session_id

                st.header("Today's Processed Prompts")
                st.markdown(
                    """
                ## How It Works
                This web application processes prompts based on the Daily Gaceta of Costa Rica and allows users to interact with the processed PDF of the day. 
                - **Today's Processed Prompts**: View and manage the prompts processed for today.
                - **Chat with Today's PDF**: Enter questions to search through today's PDF and get answers.
                - **Admin**: View detailed logs of prompt executions.
                """
                )
                # st.subheader(f"Completed At: {session['completed_at']}")
                # st.subheader(f"status: {session['status']}")
                get_and_display_execution_session(session_id)
            else:
                st.error("No execution sessions found for the selected day.")
        with tab2:
            from streamlit_pdf_viewer import pdf_viewer

            pdf_viewer(
                f"gaceta_pdfs\\{st.session_state.date}\\gaceta.pdf",
                pages_to_render=[
                    0,
                    1,
                    2,
                ],
            )

    except Exception as e:
        st.error(f"Error fetching execution session: {e}")

    if st.button("Run Execution Template"):

        response = get_gacetas("/gacetas", params={"date": selected_day})
        gacetas = response.json()
        run_execution_template(
            next(get_db()), template_id, gacetas["gacetas"][0]["gaceta"]["id"]
        )
        st.rerun()


main()
