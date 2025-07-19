import streamlit as st

from crud import re_run_prompt
from db import get_db
from stream.api import fetch_recent_exec_logs


def display_recent_exec_logs(limit=3):
    # Query the most recent content execution logs
    recent_logs = fetch_recent_exec_logs(limit=limit)

    for log in recent_logs:
        st.divider()

        st.write(f"Prompt: {log['prompt_text']}")
        # Add expander that holds the raw prompt
        st.json(log, expanded=False)

        if log["query_response_id"]:
            st.write(f"id: {log['id']}")
            st.write(f"state: {log['state']}")
            st.markdown(f"### Response: \n\n{log['response']}")
            with st.expander("sources"):
                st.write(f"Sources: {log['sources']}")

            # with st.expander("Raw Prompt"):
            #     st.write(log['raw_prompt'])
        else:
            st.write("Response: N/A")
            st.write("Sources: N/A")

        # Assuming re-run functionality is similar to the existing one
        if st.button(
            f"Re-run Prompt", key=f"rere_run_{log['id']}_{log['execution_session_id']}"
        ):
            re_run_prompt(next(get_db()), log["promp_id"], log["execution_session_id"])


st.sidebar.subheader("Admin: Prompt Execution Logs")
limit = st.sidebar.number_input(
    "Limit", min_value=1, max_value=25, value=3, step=1, key="limit"
)
# if st.button("Load Recent Execution Logs"):
display_recent_exec_logs(limit)
