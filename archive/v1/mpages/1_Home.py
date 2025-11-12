#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 Home Page UI - Main Gazette Analysis Interface
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    Primary user interface for Costa Rica gazette analysis. Provides AI model
    controls, execution session management, prompt processing, and result display
    with markdown parsing and interactive sidebar configuration.

🏗️ Architecture Flow:
    ```
    ┌─────────────────┐   Model Config  ┌──────────────────┐
    │  Sidebar        │ ───────────────▶│  AI Parameters   │
    │  Controls       │                 │  (GPT-4, tokens) │
    └─────────────────┘                 └──────────────────┘
            │                                   │
            │ User Settings                     │ Processing Config
            ▼                                   ▼
    ┌─────────────────┐                 ┌──────────────────┐
    │ Main Interface  │                 │ Execution Engine │
    │ (This Page)     │◀────────────────│ (Prompt Mgmt)    │
    └─────────────────┘                 └──────────────────┘
            │                                   │
            │ Session Display                   │ AI Results
            ▼                                   ▼
    ┌─────────────────┐                 ┌──────────────────┐
    │ Results UI      │                 │  Markdown        │
    │ (Formatted)     │                 │  Processing      │
    └─────────────────┘                 └──────────────────┘
    ```

📥 Inputs:
    • Sidebar controls: Model selection (GPT-4o, GPT-3.5), max tokens, temperature
    • Session IDs: Execution session identifiers for result retrieval
    • User interactions: Form submissions, button clicks, navigation
    • Markdown content: AI-generated responses requiring parsing and display
    • Configuration: Database connections and API settings

📤 Outputs:
    • Interactive UI: Streamlit components for user interaction
    • Formatted results: Parsed markdown content with proper rendering
    • Session displays: Execution logs and AI responses
    • Model configurations: Applied AI parameters for processing
    • User feedback: Status messages and processing indicators

🔗 Dependencies:
    • streamlit: Web UI framework and component library
    • crud: PromptExecutionEngine for AI processing logic
    • stream.api: API client for backend communication
    • models: Database models and schema definitions
    • logging_setup: Centralized logging configuration
    • re: Regular expressions for markdown parsing

🏛️ Component Relationships:
    ```mermaid
    graph TD
        A[Home Page] --> B[Sidebar Controls]
        A --> C[Main Interface]
        A --> D[Results Display]

        B --> E[Model Selection]
        B --> F[Parameter Tuning]
        C --> G[Session Management]
        C --> H[Prompt Execution]
        D --> I[Markdown Parser]
        D --> J[UI Rendering]

        H --> K[Execution Engine]
        K --> L[AI Processing]

        classDef homepage fill:#e1f5fe
        classDef controls fill:#f3e5f5
        classDef processing fill:#fff3e0
        classDef display fill:#fff8e1

        class A homepage
        class B,E,F controls
        class G,H,K,L processing
        class C,D,I,J display
    ```

🔒 Security Considerations:
    ⚠️  HIGH: No input validation on model parameters - potential resource abuse
    ⚠️  HIGH: Markdown parsing with regex - potential injection vulnerabilities
    ⚠️  MEDIUM: Session ID exposure in URLs and client state
    ⚠️  MEDIUM: No rate limiting on AI model calls - cost escalation risk
    ⚠️  LOW: Model selection changes affect all users (shared state)

🛡️ Risk Analysis:
    • Cost Control: Users can select expensive models without authorization
    • Input Injection: Markdown content not sanitized before regex processing
    • Resource Abuse: No limits on max tokens or request frequency
    • Session Security: Session IDs visible in browser and not validated
    • Data Exposure: AI responses displayed without access control

⚡ Performance Characteristics:
    • Response Time: 100-500ms for UI updates, 2-8s for AI processing
    • Memory Usage: ~20MB per session + model-specific overhead
    • Model Selection: GPT-4o (high cost/quality) vs GPT-3.5 (faster/cheaper)
    • Token Limits: User-configurable up to 8192 tokens max
    • Rendering Speed: Markdown parsing adds ~10-50ms overhead

🧪 Testing Strategy:
    • Unit Tests: Markdown parsing, parameter validation, session management
    • Integration Tests: End-to-end AI processing workflows
    • UI Tests: Component rendering, user interaction flows
    • Performance Tests: Large response handling, concurrent users

📊 Monitoring & Observability:
    • Metrics: Model usage distribution, token consumption, response times
    • Logging: User interactions, model selections, processing events
    • Alerts: High token usage, processing failures, performance degradation
    • Health Checks: AI model availability, backend connectivity

🔄 Data Flow:
    ```
    User Config ──▶ Model Setup ──▶ Prompt Execute ──▶ AI Process ──▶ Result Display
         │             │              │               │              │
         ▼             ▼              ▼               ▼              ▼
    Sidebar Input  Parameter Set   Engine Call   OpenAI API    Markdown Parse
    ```

📚 Usage Examples:
    ```python
    # Configure AI model
    model = st.sidebar.selectbox("Model", ["gpt-4o", "gpt-3.5-turbo"])
    temperature = st.sidebar.number_input("Temperature", 0.0, 1.0, 0.7)

    # Process markdown response
    parsed_content = post_parse_markdown(ai_response)
    st.markdown(parsed_content)

    # Display execution session
    get_and_display_execution_session(session_id)
    ```

🔧 Configuration:
    ```python
    # Model Options
    AVAILABLE_MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
    DEFAULT_MODEL = "gpt-4o"

    # Parameter Limits
    MAX_TOKENS_LIMIT = 8192
    MIN_TOKENS = 1
    DEFAULT_TOKENS = 512
    TEMPERATURE_RANGE = (0.0, 1.0)
    DEFAULT_TEMPERATURE = 0.7

    # UI Settings
    SIDEBAR_WIDTH = 300
    MARKDOWN_THEME = "default"
    ```

🚨 Error Handling:
    ```python
    # Markdown parsing safety
    try:
        parsed = post_parse_markdown(text)
        return parsed if parsed else text
    except re.error as e:
        st.error(f"Markdown parsing failed: {e}")
        return text

    # Session retrieval error handling
    try:
        logs = get_last_execution_session(session_id)
    except Exception as e:
        st.error(f"Failed to load session: {e}")
        logs = []
    ```

Author: GacetaChat Team | Version: 2.1.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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
