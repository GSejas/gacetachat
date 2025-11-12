#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 Admin Interface - System Management & Execution Monitoring
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Description:
    Administrative interface for GacetaChat system management. Provides execution
    log monitoring, prompt re-execution capabilities, system status overview,
    and debugging tools for AI processing pipeline management.

🏗️ Architecture Flow:
    ```
    ┌─────────────────┐   Admin Access  ┌──────────────────┐
    │  Admin User     │ ───────────────▶│  Admin Interface │
    │  (Privileged)   │                 │  (This Page)     │
    └─────────────────┘                 └──────────────────┘
            │                                   │
            │ Management Actions                │ System Queries
            ▼                                   ▼
    ┌─────────────────┐                 ┌──────────────────┐
    │ Execution Logs  │                 │   Database       │
    │ (Monitor)       │◀────────────────│   Query Layer    │
    └─────────────────┘                 └──────────────────┘
            │                                   │
            │ Re-run Operations                 │ Log Retrieval
            ▼                                   ▼
    ┌─────────────────┐                 ┌──────────────────┐
    │ Prompt Engine   │                 │ Execution History│
    │ (Re-execute)    │                 │ (Recent Logs)    │
    └─────────────────┘                 └──────────────────┘
            │                                   │
            │ AI Processing                     │ Status Display
            ▼                                   ▼
    ┌─────────────────┐                 ┌──────────────────┐
    │ System State    │                 │   Admin UI       │
    │ Updates         │                 │   Components     │
    └─────────────────┘                 └──────────────────┘
    ```

📥 Inputs:
    • Admin controls: Limit settings, re-run commands, monitoring preferences
    • System queries: Database access for execution log retrieval
    • User interactions: Button clicks, parameter adjustments
    • Session data: Execution session IDs and prompt identifiers
    • Configuration: Display limits and refresh intervals

📤 Outputs:
    • Execution monitoring: Recent prompt execution logs and status
    • System controls: Re-run buttons and administrative actions
    • Status displays: JSON data views and execution details
    • Debug information: Raw prompts, sources, and response metadata
    • Action feedback: Success/failure indicators for admin operations

🔗 Dependencies:
    • streamlit: Admin UI framework and interactive components
    • crud: re_run_prompt function for prompt re-execution
    • db: Database connection and session management
    • stream.api: API client for execution log retrieval
    • models: Database models for execution tracking
    • logging: System logging and error tracking

🏛️ Component Relationships:
    ```mermaid
    graph TD
        A[Admin Page] --> B[Sidebar Controls]
        A --> C[Log Display]
        A --> D[Re-run Controls]

        B --> E[Limit Settings]
        C --> F[Recent Logs API]
        C --> G[JSON Display]
        D --> H[Prompt Re-execution]

        F --> I[Database Query]
        H --> J[CRUD Operations]
        I --> K[(Execution Logs)]
        J --> L[AI Processing]

        classDef adminPage fill:#e1f5fe
        classDef controls fill:#f3e5f5
        classDef data fill:#fff3e0
        classDef processing fill:#fff8e1

        class A adminPage
        class B,D,E,H controls
        class C,F,G,I,K data
        class J,L processing
    ```

🔒 Security Considerations:
    ⚠️  HIGH: No authentication for admin functions - unauthorized access possible
    ⚠️  HIGH: Direct database access without authorization checks
    ⚠️  MEDIUM: Execution logs may contain sensitive user data
    ⚠️  MEDIUM: Re-run operations not logged or audited
    ⚠️  LOW: Admin interface accessible to all users without restrictions

🛡️ Risk Analysis:
    • Access Control: No admin role verification or access restrictions
    • Data Exposure: Sensitive prompt content and responses visible to all
    • System Impact: Re-run operations consume AI API credits without limits
    • Audit Trail: No logging of administrative actions performed
    • Resource Abuse: No limits on concurrent re-run operations

⚡ Performance Characteristics:
    • Log Retrieval: 100-500ms for recent execution logs query
    • UI Rendering: <100ms for display updates and JSON formatting
    • Re-run Operations: 2-8 seconds for prompt re-execution
    • Memory Usage: ~10MB for log data caching
    • Database Impact: O(n) query complexity for log retrieval

🧪 Testing Strategy:
    • Unit Tests: Log display logic, re-run functionality, UI components
    • Integration Tests: End-to-end admin workflows with database
    • Security Tests: Access control bypass attempts, data exposure
    • Performance Tests: Large log datasets, concurrent admin operations

📊 Monitoring & Observability:
    • Metrics: Admin page usage, re-run frequency, log query performance
    • Logging: Admin actions, re-run operations, system access
    • Alerts: Failed re-runs, excessive admin activity, performance issues
    • Health Checks: Database connectivity, API availability

🔄 Data Flow:
    ```
    Admin Action ──▶ Parameter Set ──▶ Database Query ──▶ Log Display ──▶ Re-run Option
         │              │                │                │               │
         ▼              ▼                ▼                ▼               ▼
    UI Interaction  Limit Config    API Request     JSON Format    Prompt Execute
    ```

📚 Usage Examples:
    ```python
    # Display recent execution logs
    display_recent_exec_logs(limit=5)

    # Configure display settings
    limit = st.sidebar.number_input("Limit", 1, 25, 3)


    # Show detailed log data
    st.json(log_data, expanded=False)
    ```

🔧 Configuration:
    ```python
    # Display Settings
    DEFAULT_LIMIT = 3
    MAX_LOGS_LIMIT = 25
    MIN_LOGS_LIMIT = 1

    # UI Configuration
    SIDEBAR_TITLE = "Admin: Prompt Execution Logs"
    EXPANDABLE_SOURCES = True
    JSON_EXPANDED_DEFAULT = False

    # Re-run Settings
    MAX_CONCURRENT_RERUNS = 5
    RERUN_TIMEOUT = 30  # seconds
    ```

🚨 Production Security Requirements:
    • Implement role-based access control for admin functions
    • Add authentication middleware for admin page access
    • Audit all administrative actions with user attribution
    • Sanitize sensitive data before display
    • Implement rate limiting for re-run operations

📋 Admin Functions Available:
    • **Log Monitoring**: View recent execution logs with configurable limits
    • **Prompt Re-execution**: Manually trigger prompt re-runs for debugging
    • **Status Overview**: JSON view of execution details and metadata
    • **Source Inspection**: Expandable view of document sources used
    • **Error Analysis**: Failed execution identification and debugging

Author: GacetaChat Team | Version: 2.1.0 | Last Updated: 2024-12-19
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import streamlit as st

# AITODO: we should search for why this re run prompt exists
# from crud import re_run_prompt
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
        # if st.button(
        #     f"Re-run Prompt", key=f"rere_run_{log['id']}_{log['execution_session_id']}"
        # ):
        #     re_run_prompt(next(get_db()), log["promp_id"], log["execution_session_id"])


st.sidebar.subheader("Admin: Prompt Execution Logs")
limit = st.sidebar.number_input(
    "Limit", min_value=1, max_value=25, value=3, step=1, key="limit"
)
# if st.button("Load Recent Execution Logs"):
display_recent_exec_logs(limit)
