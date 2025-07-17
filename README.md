# GacetaChat 🇨🇷

> AI-powered chatbot system for automated processing and analysis of Costa Rica's daily official gazette (Gaceta Oficial)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.100+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Overview

GacetaChat is a sophisticated AI-powered system that automatically downloads, processes, and analyzes Costa Rica's daily official gazette. It provides intelligent content summarization, social media automation, and interactive query capabilities for legal professionals, journalists, and citizens.

## ✨ Key Features

- **🤖 Automated PDF Processing**: Daily download and processing of official gazette PDFs
- **🔍 Semantic Search**: FAISS-powered vector search for accurate information retrieval
- **💬 Interactive Chat**: ChatGPT-powered Q&A with document context
- **🐦 Social Media Integration**: Automated Twitter content generation
- **📊 Multi-format Content**: Newsletter, headlines, economic updates, legal changes
- **🎭 Humorous Summaries**: Engaging 280-character news summaries with emojis
- **📱 Multi-platform**: Web interface with mobile-responsive design
- **🔒 Rate Limiting**: Built-in usage controls and session management

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │   Background    │
│   Frontend      │◄──►│    Backend      │◄──►│   Processor     │
│   (Port 8512)   │    │   (Port 8050)   │    │  (Scheduled)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Pages    │    │   SQLite DB     │    │   PDF Source    │
│   - Home        │    │   - Users       │    │   (Gov Site)    │
│   - Twitter     │    │   - Sessions    │    │                 │
│   - Admin       │    │   - Prompts     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key
- Twitter API Keys (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gacetachat.git
   cd gacetachat
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   OPENAI_API_KEY=your_openai_api_key_here
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET_KEY=your_twitter_api_secret
   APP_SECRET_API_KEY=your_app_secret_key
   ```

4. **Initialize the database**
   ```bash
   python -c "from models import *; from db import engine; Base.metadata.create_all(bind=engine)"
   ```

5. **Run the application**
   ```bash
   # Start FastAPI backend
   uvicorn fastapp:app --host 127.0.0.1 --port 8050

   # Start Streamlit frontend (in another terminal)
   streamlit run app.py --server.port 8512

   # Start background processor (in another terminal)
   python download_gaceta.py
   ```

## 📖 Usage

### Web Interface

1. **Navigate to** `http://localhost:8512`
2. **Select a date** from the sidebar to view processed content
3. **Use the chat interface** to ask questions about the gazette
4. **View generated summaries** and social media content

### API Endpoints

```bash
# Get execution sessions
GET /execution_session_by_date/?date=2025-07-06

# Get available days
GET /execution_session/available

# Check query limits
GET /check_global_limit/
```

## 🏢 Business Model & Commercialization

See [COMMERCIALIZATION.md](./docs/COMMERCIALIZATION.md) for detailed guidance on:
- Market positioning strategies
- Pricing models
- White-label opportunities
- Revenue streams
- Customer acquisition

## 🛠️ Development

### Project Structure
```
gacetachat/
├── app.py                 # Main Streamlit application
├── fastapp.py            # FastAPI backend
├── download_gaceta.py    # Background PDF processor
├── models.py             # Database models
├── config.py             # Configuration settings
├── mpages/               # Streamlit pages
│   ├── 1_Home.py
│   ├── 2_Twitter.py
│   └── 3_Admin.py
├── services/             # Business logic
├── stream/               # API integration
├── test/                 # Test suites
└── docs/                 # Documentation
```

### Development Standards

See [DEVELOPMENT.md](./docs/DEVELOPMENT.md) for:
- Code style guidelines
- Testing procedures
- Deployment practices
- Database migrations

## 🐛 Known Issues & Pain Points

See [PAIN_POINTS.md](./docs/PAIN_POINTS.md) for detailed analysis of:
- Technical challenges
- Performance bottlenecks
- User experience issues
- Scalability concerns

## 🔧 Configuration

### Environment Variables
```env
# Required
OPENAI_API_KEY=sk-...
APP_SECRET_API_KEY=your-secret-key

# Optional
TWITTER_API_KEY=your-twitter-key
TWITTER_API_SECRET_KEY=your-twitter-secret
TWITTER_CONSUMER_API_KEY=your-consumer-key
TWITTER_CONSUMER_API_SECRET_KEY=your-consumer-secret
```

### Model Configuration
```python
# config.py
OPENAI_MODEL_NAME = "gpt-4o"
OPENAI_MAX_TOKENS = 2000
OPENAI_TEMPERATURE = 0.3
```

## 📊 Monitoring & Analytics

- **Query Usage**: Daily limits and tracking
- **Processing Status**: Document processing states
- **Error Logging**: Comprehensive error tracking
- **Performance Metrics**: Response times and success rates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Costa Rica's National Printing Office for providing open access to the official gazette
- OpenAI for providing the GPT models
- The Streamlit and FastAPI communities for excellent documentation

## 📞 Support

For support, email support@gacetachat.com or create an issue in the GitHub repository.

---

**Made with ❤️ in Costa Rica 🇨🇷**
