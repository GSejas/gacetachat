# Demo & Showcase Tutorial

## 🎬 How to Effectively Demonstrate GacetaChat

This tutorial provides a comprehensive guide for showcasing GacetaChat to potential customers, investors, partners, or team members.

## 🎯 Demo Objectives

Before starting any demo, identify your audience and objectives:

### For Potential Customers
- **Goal**: Show business value and ROI
- **Focus**: Time savings, accuracy, ease of use
- **Duration**: 10-15 minutes

### For Investors
- **Goal**: Demonstrate market opportunity and scalability
- **Focus**: Technical innovation, market size, revenue potential
- **Duration**: 15-20 minutes

### For Technical Partners
- **Goal**: Showcase technical capabilities and integration options
- **Focus**: Architecture, APIs, customization options
- **Duration**: 20-30 minutes

## 🚀 Demo Setup Checklist

### Pre-Demo Preparation (30 minutes before)

```bash
# 1. Start all services
pm2 start ecosystem.config.js

# 2. Check service health
curl http://localhost:8050/health
curl http://localhost:8512

# 3. Verify database has recent data
python -c "
from db import Session
from models import GacetaPDF
session = Session()
recent = session.query(GacetaPDF).order_by(GacetaPDF.date.desc()).first()
print(f'Latest PDF: {recent.date if recent else \"None\"}')"

# 4. Clear browser cache and cookies
# 5. Prepare demo data and scenarios
```

### Demo Environment Setup

```python
# Create demo-specific configuration
DEMO_CONFIG = {
    "openai_model": "gpt-4o",  # Use best model for demo
    "response_speed": "fast",  # Pre-cache responses
    "demo_mode": True,  # Enable demo features
    "sample_queries": [
        "What are the main news from today's gazette?",
        "Are there any new regulations affecting businesses?",
        "What economic announcements were made?"
    ]
}
```

## 📋 Demo Script Templates

### 1. **Business-Focused Demo (10 minutes)**

#### Opening (1 minute)
```
"Good morning! I'm excited to show you GacetaChat, an AI-powered system that 
transforms how legal professionals and businesses stay informed about Costa Rica's 
official gazette. 

Let me show you how we can turn a 50-page PDF into actionable insights in seconds."
```

#### Problem Statement (2 minutes)
```
"Every day, Costa Rica publishes its official gazette - a dense, 20-50 page document 
containing legal announcements, regulatory changes, and business notices. 

Traditional approach:
- Manual reading: 2-3 hours per day
- Easy to miss important information
- No way to track changes over time
- Difficult to share insights with team

Let me show you how GacetaChat solves this..."
```

#### Core Demo Flow (5 minutes)

**Step 1: Show Today's Processed Content**
```python
# Navigate to main dashboard
st.sidebar.selectbox("Select Date", available_dates)
st.write("Here's what was automatically processed from today's gazette:")

# Show pre-generated summaries
display_execution_session(session_id)
```

**Step 2: Interactive Query**
```python
# Demonstrate chat interface
user_query = "What new business regulations were announced today?"
# Show real-time processing
with st.spinner("Analyzing today's gazette..."):
    response = query_document(user_query)
    st.write(response)
```

**Step 3: Social Media Integration**
```python
# Show Twitter integration
st.write("And here's how it automatically creates social media content:")
show_twitter_summaries()
```

#### Value Proposition (1 minute)
```
"What you just saw:
- 3 hours of manual work → 30 seconds
- 100% accuracy with source citations
- Automatic social media content
- Historical tracking and analysis

This saves our customers 15 hours per week and ensures they never miss 
critical information."
```

#### Call to Action (1 minute)
```
"Would you like to try a free 30-day trial? I can set up your account right now 
and show you how to customize it for your specific needs."
```

### 2. **Technical Demo (20 minutes)**

#### Architecture Overview (3 minutes)
```python
# Show system architecture
st.mermaid("""
graph TB
    A[Daily PDF] --> B[AI Processing]
    B --> C[Vector Database]
    C --> D[Query Engine]
    D --> E[User Interface]
    B --> F[Social Media]
""")
```

#### API Demonstration (5 minutes)
```python
# Show API endpoints
import requests

# 1. Get available documents
response = requests.get("http://localhost:8050/execution_session/available")
st.json(response.json())

# 2. Query specific document
query_response = requests.post(
    "http://localhost:8050/query",
    json={"query": "economic regulations", "date": "2025-01-06"}
)
st.json(query_response.json())
```

#### Customization Options (7 minutes)
```python
# Show prompt customization
st.subheader("Custom Prompt Templates")
st.text_area("Custom Prompt", value="""
Create a summary focusing on:
1. Environmental regulations
2. Tax changes
3. Business licenses
4. Export/import rules
""")

# Show white-label options
st.subheader("White-Label Configuration")
st.color_picker("Primary Color", "#2E86AB")
st.text_input("Company Name", "Your Company Name")
st.file_uploader("Company Logo")
```

#### Integration Examples (3 minutes)
```python
# Show integration options
st.subheader("Integration Options")

# Webhook example
webhook_code = '''
POST /webhook
{
    "event": "document_processed",
    "document_id": "2025-01-06",
    "summary": "...",
    "alerts": [...]
}
'''

# API client example
api_code = '''
import gacetachat

client = gacetachat.Client(api_key="your-key")
results = client.query("business regulations", date="2025-01-06")
'''
```

#### Scalability Discussion (2 minutes)
```
"Our architecture supports:
- Multi-tenant deployments
- Custom AI models per client
- Enterprise SSO integration
- 99.9% uptime SLA
- Horizontal scaling
- Global deployment"
```

### 3. **Investor Demo (15 minutes)**

#### Market Opportunity (3 minutes)
```python
# Show market size visualization
import plotly.express as px

market_data = {
    "Segment": ["Legal Tech", "Gov Tech", "AI Content", "Document Processing"],
    "Size (Billions)": [28, 15, 3.2, 8.9],
    "Growth Rate": [12, 18, 25, 15]
}

fig = px.bar(market_data, x="Segment", y="Size (Billions)", 
             title="Total Addressable Market")
st.plotly_chart(fig)
```

#### Traction Metrics (2 minutes)
```python
# Show growth metrics
metrics = {
    "Users": 150,
    "Documents Processed": 2500,
    "Queries Answered": 5000,
    "Accuracy Rate": 95,
    "User Satisfaction": 4.8
}

col1, col2, col3 = st.columns(3)
for metric, value in metrics.items():
    col1.metric(metric, value)
```

#### Revenue Model (3 minutes)
```python
# Show revenue projections
revenue_data = {
    "Year": [2025, 2026, 2027],
    "Customers": [50, 200, 800],
    "Revenue": [50000, 500000, 2000000],
    "ARR": [1000, 2500, 2500]
}

fig = px.line(revenue_data, x="Year", y="Revenue", 
              title="Revenue Projections")
st.plotly_chart(fig)
```

#### Product Demo (5 minutes)
```
[Same as business demo but emphasize scalability and technical innovation]
```

#### Competitive Advantage (2 minutes)
```python
# Show competitive analysis
competitors = {
    "Feature": ["AI-Powered", "Real-time", "Multi-language", "Social Media", "White-label"],
    "GacetaChat": ["✅", "✅", "✅", "✅", "✅"],
    "Competitor A": ["❌", "✅", "❌", "❌", "❌"],
    "Competitor B": ["✅", "❌", "✅", "❌", "❌"]
}

st.table(competitors)
```

## 🎥 Demo Scenarios

### Scenario 1: Legal Firm Use Case
**Setup**: Law firm partner looking for regulatory updates

```python
# Pre-loaded query examples
legal_queries = [
    "What new legal procedures were established?",
    "Are there any changes to corporate law?",
    "What court appointments were announced?",
    "Any new regulations affecting contracts?"
]

# Show before/after
st.subheader("Traditional Process")
st.write("Partner spends 2 hours reading 45-page document")
st.write("Highlights important sections manually")
st.write("Creates summary for team")

st.subheader("With GacetaChat")
st.write("AI processes document in 30 seconds")
st.write("Automatically identifies relevant sections")
st.write("Creates team summary with source citations")
```

### Scenario 2: Government Contractor
**Setup**: Company tracking procurement opportunities

```python
# Business-focused queries
procurement_queries = [
    "What new government contracts were announced?",
    "Are there any tender opportunities?",
    "What regulatory changes affect contractors?",
    "Any new environmental compliance requirements?"
]

# Show procurement alert system
st.subheader("Automated Procurement Alerts")
st.write("🚨 New tender: Road construction project - $2.5M")
st.write("📋 Deadline: February 15, 2025")
st.write("📍 Location: San José Province")
st.write("🔗 Source: Gaceta Page 23, Section 4.2")
```

### Scenario 3: News Organization
**Setup**: Journalist covering government policy

```python
# Journalism-focused queries
news_queries = [
    "What are the top 3 news stories from today?",
    "Any controversial decisions announced?",
    "What economic policies were introduced?",
    "Any appointments or dismissals?"
]

# Show news generation pipeline
st.subheader("Automated News Generation")
st.write("1. AI identifies newsworthy items")
st.write("2. Generates article summaries")
st.write("3. Creates social media posts")
st.write("4. Provides journalist with source material")
```

## 📊 Demo Metrics & KPIs

### Real-time Demo Metrics
```python
# Display live metrics during demo
def show_demo_metrics():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Processing Speed", "30 sec", "↓ 85%")
    
    with col2:
        st.metric("Accuracy", "95%", "↑ 15%")
    
    with col3:
        st.metric("Time Saved", "2.5 hrs", "↑ 87%")
    
    with col4:
        st.metric("User Satisfaction", "4.8/5", "↑ 12%")
```

### Performance Comparison
```python
# Show before/after comparison
comparison_data = {
    "Task": ["Document Review", "Summary Creation", "Query Response", "Social Media"],
    "Manual (hours)": [2.5, 0.5, 0.25, 0.5],
    "GacetaChat (minutes)": [0.5, 0.5, 0.5, 0.5],
    "Time Saved (%)": [98, 95, 92, 95]
}

fig = px.bar(comparison_data, x="Task", y=["Manual (hours)", "GacetaChat (minutes)"],
             title="Time Savings Comparison")
st.plotly_chart(fig)
```

## 🔧 Demo Tools & Setup

### Pre-Demo Setup Script
```python
# demo_setup.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def setup_demo_environment():
    """Prepare demo environment with sample data"""
    
    # 1. Generate sample processed content
    sample_content = generate_sample_content()
    
    # 2. Pre-cache AI responses for common queries
    precache_responses()
    
    # 3. Set up demo user account
    create_demo_user()
    
    # 4. Configure demo-specific settings
    configure_demo_settings()
    
    st.success("Demo environment ready!")

def generate_sample_content():
    """Generate realistic sample content for demo"""
    return {
        "news_summary": "3 major economic announcements...",
        "legal_changes": "New corporate registration procedures...",
        "social_media": "🇨🇷 Big news today! New tax incentives..."
    }

def precache_responses():
    """Pre-cache responses for common demo queries"""
    demo_queries = [
        "What are today's main news?",
        "Any new business regulations?",
        "What economic announcements were made?"
    ]
    
    for query in demo_queries:
        # Cache response to avoid demo delays
        cache_ai_response(query)
```

### Demo Troubleshooting
```python
# Common demo issues and solutions
demo_issues = {
    "Slow AI Response": {
        "cause": "API rate limiting",
        "solution": "Use pre-cached responses",
        "prevention": "Run demo_setup.py before demo"
    },
    "Database Lock": {
        "cause": "Concurrent access",
        "solution": "Restart services",
        "prevention": "Use read-only demo mode"
    },
    "Missing PDF": {
        "cause": "Download failure",
        "solution": "Use backup sample PDF",
        "prevention": "Verify PDFs exist before demo"
    }
}
```

## 🎯 Demo Best Practices

### Do's
- **Practice the demo** at least 3 times before presenting
- **Have backup plans** for technical failures
- **Keep it interactive** - let audience ask questions
- **Use real data** whenever possible
- **Show source citations** to build trust
- **Demonstrate mobile experience** if relevant
- **End with clear next steps**

### Don'ts
- **Don't show raw technical errors** to business audience
- **Don't spend too much time on setup**
- **Don't demo features that aren't working**
- **Don't make claims you can't support**
- **Don't forget to check internet connection**
- **Don't rush through the value proposition**

### Technical Tips
```python
# Demo mode configuration
def enable_demo_mode():
    st.session_state.demo_mode = True
    st.session_state.fast_responses = True
    st.session_state.sample_data = True
    
    # Hide technical details
    st.session_state.show_debug = False
    st.session_state.show_errors = False
    
    # Enable demo features
    st.session_state.auto_scroll = True
    st.session_state.highlight_features = True
```

## 📈 Follow-up Actions

### After the Demo
1. **Send follow-up email** within 24 hours
2. **Provide trial access** if requested
3. **Schedule technical deep-dive** for qualified prospects
4. **Share relevant case studies** and documentation
5. **Connect on LinkedIn** for ongoing relationship

### Demo Feedback Collection
```python
# Post-demo survey
def collect_demo_feedback():
    st.subheader("Demo Feedback")
    
    rating = st.slider("How would you rate this demo?", 1, 5, 5)
    
    interest = st.selectbox("Interest level", [
        "Very interested - want to start trial",
        "Interested - need more information",
        "Somewhat interested - will consider",
        "Not interested at this time"
    ])
    
    feedback = st.text_area("What impressed you most?")
    
    concerns = st.text_area("Any concerns or questions?")
    
    if st.button("Submit Feedback"):
        save_feedback(rating, interest, feedback, concerns)
        st.success("Thank you for your feedback!")
```

## 🚀 Demo Success Metrics

### Immediate Success Indicators
- **Engagement**: Audience asks questions and shows interest
- **Understanding**: Audience grasps the value proposition
- **Next Steps**: Clear follow-up actions are scheduled
- **Positive Feedback**: Audience expresses interest or excitement

### Long-term Success Metrics
- **Trial Conversions**: 30% of demos → trials
- **Sales Conversions**: 15% of demos → sales
- **Referrals**: 10% of demos → referrals
- **Partnership Opportunities**: 5% of demos → partnerships

This comprehensive demo guide ensures you can effectively showcase GacetaChat's capabilities to any audience, whether they're potential customers, investors, or technical partners.
