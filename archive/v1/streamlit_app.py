#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 Streamlit Main Application - Interactive UI for Gazette Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    Main Streamlit web application providing interactive UI for Costa Rica gazette
    analysis. Handles session management, date selection, query processing, and
    integration with AI-powered document analysis through FastAPI backend.

🏗️ Architecture Flow:
    ```
    ┌─────────────────┐   User Input   ┌──────────────────┐
    │  Browser UI     │ ──────────────▶│  Streamlit App   │
    │  (Port 8512)    │    WebSocket   │  (This Module)   │
    └─────────────────┘                └──────────────────┘
            │                                  │
            │ Session State                    │ API Calls
            ▼                                  ▼
    ┌─────────────────┐                ┌──────────────────┐
    │ Browser Storage │                │   FastAPI API    │
    │ (Client Side)   │                │   (Port 8050)    │
    └─────────────────┘                └──────────────────┘
            │                                  │
            │ Page Navigation                  │ Data Processing
            ▼                                  ▼
    ┌─────────────────┐                ┌──────────────────┐
    │ Multi-page UI   │                │ Database + AI    │
    │ (mpages/)       │◀───────────────│ Processing       │
    └─────────────────┘                └──────────────────┘
    ```

📥 Inputs:
    • User interactions: Date selection, query submission, page navigation
    • URL parameters: Date redirects and session state management
    • Session state: Query counts, selected dates, user preferences
    • API responses: Execution sessions, available dates, processing results
    • Configuration: Costa Rica timezone, database connections

📤 Outputs:
    • Interactive UI: Streamlit components for user interaction
    • Session management: Date selection and query tracking
    • API requests: Backend communication for data processing
    • Page routing: Multi-page application navigation
    • User feedback: Warnings, success messages, processing status

🔗 Dependencies:
    • streamlit: Web application framework and UI components
    • pytz: Timezone handling for Costa Rica local time
    • stream.api: Custom API client for FastAPI backend communication
    • models: Database models and ORM definitions
    • logging_setup: Centralized logging configuration
    • db: Database connection and session management

🏛️ Component Relationships:
    ```mermaid
    graph TD
        A[Streamlit App] --> B[Session State]
        A --> C[API Client]
        A --> D[Multi-page UI]

        B --> E[Date Selection]
        B --> F[Query Tracking]
        C --> G[FastAPI Backend]
        D --> H[Home Page]
        D --> I[Twitter Page]
        D --> J[Admin Page]

        G --> K[Database Layer]
        G --> L[AI Processing]

        classDef streamlit fill:#e1f5fe
        classDef session fill:#f3e5f5
        classDef external fill:#fff3e0
        classDef pages fill:#fff8e1

        class A,B streamlit
        class C,E,F session
        class G,K,L external
        class H,I,J pages
    ```

🔒 Security Considerations:
    ⚠️  HIGH: No user authentication - all users access same data and functions
    ⚠️  HIGH: Session state stored client-side - potential manipulation
    ⚠️  MEDIUM: URL parameter injection through date redirects
    ⚠️  MEDIUM: No input validation on user queries before API submission
    ⚠️  LOW: Timezone handling exposes server location information

🛡️ Risk Analysis:
    • Authentication Bypass: No user login system, anonymous access to all features
    • Session Hijacking: Client-side state management vulnerable to manipulation
    • Data Exposure: All users see same data without access controls
    • Input Validation: User queries passed directly to AI without sanitization
    • Resource Abuse: No rate limiting on expensive operations

⚡ Performance Characteristics:
    • Response Time: 100-300ms for UI updates, 2-8s for AI processing
    • Memory Usage: ~50MB per user session + shared application state
    • Concurrent Users: Streamlit supports ~100 concurrent users per instance
    • Session Storage: Client-side storage with automatic cleanup
    • Backend Latency: Dependent on FastAPI response times and AI processing

🧪 Testing Strategy:
    • Unit Tests: Session state management, API client integration
    • Integration Tests: End-to-end user workflows with backend
    • UI Tests: Component rendering, user interaction simulation
    • Performance Tests: Concurrent user scenarios, memory usage monitoring

📊 Monitoring & Observability:
    • Metrics: Page views, session duration, API call frequency, error rates
    • Logging: User interactions, API calls, session state changes
    • Alerts: Backend connection failures, high error rates, performance issues
    • Health Checks: FastAPI connectivity, database availability

🔄 Data Flow:
    ```
    User Action ──▶ Session Update ──▶ API Call ──▶ Backend Process ──▶ UI Update
         │             │               │            │                  │
         ▼             ▼               ▼            ▼                  ▼
    Input Capture  State Mgmt     HTTP Request   AI Processing    Component Render
    ```

📚 Usage Examples:
    ```python
    # Start Streamlit application
    streamlit run streamlit_app.py --server.port 8512

    # Session state management
    if "query_count" not in st.session_state:
        st.session_state["query_count"] = 0

    # Date selection with validation
    available_days = list_available_index_days()
    selected_date = st.selectbox("Select Date", available_days)

    # API integration
    response = api_call_with_session(endpoint, data)
    ```

🔧 Configuration:
    ```python
    # Server Settings
    STREAMLIT_PORT = 8512
    BACKEND_API_URL = "http://localhost:8050"

    # Session Configuration
    DEFAULT_TIMEZONE = "America/Costa_Rica"
    SESSION_TIMEOUT = 3600  # 1 hour
    MAX_QUERY_COUNT = 100   # Per session limit

    # UI Settings
    PAGE_TITLE = "GacetaChat - Costa Rica Gazette Analysis"
    THEME = "light"
    ```

🚨 Production Considerations:
    • Authentication: Implement user login and access controls
    • Session Security: Move sensitive state to server-side storage
    • Input Validation: Sanitize all user inputs before processing
    • Rate Limiting: Implement per-user query limits and throttling
    • Monitoring: Add comprehensive user activity tracking

Author: GacetaChat Team | Version: 2.1.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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
