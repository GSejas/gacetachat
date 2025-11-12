# Configuration Guide

This guide covers all configuration options for GacetaChat, from basic settings to advanced customizations.

## 🔧 Basic Configuration

### Environment Variables

The main configuration is handled through environment variables in your `.env` file:

```env
# Core Application Settings
APP_NAME=GacetaChat
APP_VERSION=1.0.0
ENVIRONMENT=production  # development, staging, production
DEBUG=false
SECRET_KEY=your-secret-key-here

# Server Configuration
HOST=0.0.0.0
FRONTEND_PORT=8512
BACKEND_PORT=8050
WORKER_PROCESSES=2

# API Configuration
APP_SECRET_API_KEY=your-api-secret-key
API_RATE_LIMIT=100  # requests per minute
CORS_ORIGINS=["http://localhost:8512", "https://yourdomain.com"]
```

### OpenAI Configuration

```env
# OpenAI Settings
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL_NAME=gpt-4o
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.3
OPENAI_TIMEOUT=60
OPENAI_MAX_RETRIES=3

# Model Selection Strategy
USE_SMART_MODEL_SELECTION=true
FALLBACK_MODEL=gpt-3.5-turbo
COST_OPTIMIZATION=true
```

### Database Configuration

```env
# Database Settings
DATABASE_URL=sqlite:///gaceta.db
# For PostgreSQL: postgresql://user:password@localhost:5432/gaceta
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800

# Backup Settings
AUTO_BACKUP=true
BACKUP_SCHEDULE=0 2 * * *  # Daily at 2 AM
BACKUP_RETENTION_DAYS=30
```

## 📁 File Storage Configuration

### PDF Storage

```env
# PDF Storage
GACETA_PDFS_DIR=gaceta_pdfs
MAX_PDF_SIZE_MB=50
PDF_RETENTION_DAYS=365
ENABLE_PDF_COMPRESSION=true

# Download Settings
PDF_DOWNLOAD_TIMEOUT=300
MAX_DOWNLOAD_RETRIES=5
DOWNLOAD_USER_AGENT=GacetaChat/1.0
```

### FAISS Index Configuration

```env
# Vector Store Settings
FAISS_INDEX_DIR=faiss_indexes
EMBEDDING_MODEL=text-embedding-ada-002
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
INDEX_REBUILD_SCHEDULE=0 3 * * *  # Daily at 3 AM
```

## 🐦 Social Media Integration

### Twitter Configuration

```env
# Twitter API v2
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET_KEY=your-api-secret
TWITTER_CONSUMER_API_KEY=your-consumer-key
TWITTER_CONSUMER_API_SECRET_KEY=your-consumer-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-secret
TWITTER_BEARER_TOKEN=your-bearer-token

# Twitter Settings
TWITTER_AUTO_POST=true
TWITTER_POST_SCHEDULE=0 8 * * *  # Daily at 8 AM
TWITTER_CHARACTER_LIMIT=280
TWITTER_HASHTAGS=#CostaRica #Gaceta #AI
```

### Content Generation Settings

```env
# Social Media Content
ENABLE_HUMOR_MODE=true
EMOJI_USAGE=moderate  # none, light, moderate, heavy
CONTENT_TONE=professional  # formal, professional, casual, humorous
TARGET_AUDIENCE=general  # legal, business, general, academic
```

## 🔐 Security Configuration

### Authentication & Authorization

```env
# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
JWT_REFRESH_EXPIRATION_DAYS=30

# API Security
ENABLE_API_KEY_AUTH=true
REQUIRE_HTTPS=true
TRUSTED_HOSTS=["localhost", "127.0.0.1", "yourdomain.com"]

# Rate Limiting
RATE_LIMIT_ENABLED=true
GLOBAL_RATE_LIMIT=1000  # requests per day
USER_RATE_LIMIT=100     # requests per hour
IP_RATE_LIMIT=200       # requests per hour per IP
```

### Data Protection

```env
# Privacy & Security
ENABLE_DATA_ENCRYPTION=true
ENCRYPTION_KEY=your-encryption-key
LOG_SENSITIVE_DATA=false
GDPR_COMPLIANCE=true
DATA_RETENTION_DAYS=90

# Audit Logging
ENABLE_AUDIT_LOG=true
AUDIT_LOG_LEVEL=INFO
AUDIT_LOG_FILE=logs/audit.log
```

## 📊 Monitoring & Logging

### Logging Configuration

```env
# Logging Settings
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/gaceta.log
LOG_MAX_SIZE_MB=100
LOG_BACKUP_COUNT=5
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Structured Logging
ENABLE_JSON_LOGGING=true
LOG_CORRELATION_ID=true
LOG_USER_ACTIONS=true
```

### Monitoring Integration

```env
# Sentry Error Tracking
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1

# Metrics Collection
ENABLE_METRICS=true
METRICS_PORT=9090
PROMETHEUS_ENABLED=true

# Health Checks
HEALTH_CHECK_INTERVAL=30  # seconds
HEALTH_CHECK_TIMEOUT=10   # seconds
```

## ⚡ Performance Configuration

### Caching Settings

```env
# Redis Cache
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your-redis-password
CACHE_TTL=3600  # 1 hour
CACHE_MAX_SIZE=1000

# Application Cache
ENABLE_MEMORY_CACHE=true
MEMORY_CACHE_SIZE=100MB
CACHE_COMPRESSION=true
```

### Processing Optimization

```env
# Background Processing
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_WORKER_CONCURRENCY=4
CELERY_TASK_TIME_LIMIT=600

# PDF Processing
ENABLE_PARALLEL_PROCESSING=true
MAX_CONCURRENT_PDFS=3
PDF_PROCESSING_TIMEOUT=300
```

## 🌐 Internationalization

### Language Settings

```env
# Localization
DEFAULT_LANGUAGE=es
SUPPORTED_LANGUAGES=["es", "en"]
TIMEZONE=America/Costa_Rica
DATE_FORMAT=%Y-%m-%d
TIME_FORMAT=%H:%M:%S

# Content Localization
ENABLE_AUTO_TRANSLATION=false
TRANSLATION_SERVICE=google  # google, deepl, azure
FALLBACK_LANGUAGE=en
```

## 📧 Notification Configuration

### Email Settings

```env
# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_TLS=true

# Email Notifications
ENABLE_EMAIL_NOTIFICATIONS=true
ADMIN_EMAIL=admin@yourdomain.com
ERROR_NOTIFICATION_EMAIL=errors@yourdomain.com
```

### Alert Configuration

```env
# System Alerts
ALERT_ON_PROCESSING_FAILURE=true
ALERT_ON_HIGH_ERROR_RATE=true
ALERT_ON_QUOTA_EXCEEDED=true
ERROR_RATE_THRESHOLD=5  # percent
QUOTA_WARNING_THRESHOLD=80  # percent
```

## 🔄 Backup & Recovery

### Automated Backups

```env
# Backup Configuration
ENABLE_AUTO_BACKUP=true
BACKUP_SCHEDULE=0 2 * * *  # Daily at 2 AM
BACKUP_LOCATION=/backups/gaceta
BACKUP_COMPRESSION=gzip
BACKUP_ENCRYPTION=true

# S3 Backup (Optional)
S3_BACKUP_ENABLED=false
S3_BUCKET_NAME=gaceta-backups
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_REGION=us-east-1
```

### Recovery Settings

```env
# Recovery Configuration
POINT_IN_TIME_RECOVERY=true
RECOVERY_RETENTION_DAYS=30
AUTO_RECOVERY_ENABLED=false
RECOVERY_NOTIFICATION=true
```

## 🎨 UI Customization

### Appearance Settings

```env
# UI Configuration
APP_TITLE=GacetaChat
APP_FAVICON=/static/favicon.ico
APP_LOGO=/static/logo.png
THEME=default  # default, dark, light, custom

# Branding
PRIMARY_COLOR=#2E86AB
SECONDARY_COLOR=#A23B72
ACCENT_COLOR=#F18F01
BACKGROUND_COLOR=#FFFFFF
```

### Feature Toggles

```env
# Feature Flags
ENABLE_CHAT_INTERFACE=true
ENABLE_TWITTER_INTEGRATION=true
ENABLE_PDF_VIEWER=true
ENABLE_ADMIN_PANEL=true
ENABLE_API_DOCS=true
ENABLE_DEMO_MODE=false

# Advanced Features
ENABLE_CUSTOM_PROMPTS=true
ENABLE_BULK_PROCESSING=false
ENABLE_WEBHOOKS=false
ENABLE_ANALYTICS=true
```

## 🛠️ Development Configuration

### Development Settings

```env
# Development Mode
DEBUG=true
RELOAD_ON_CHANGE=true
ENABLE_PROFILING=true
SHOW_DEBUG_TOOLBAR=true

# Testing
TEST_DATABASE_URL=sqlite:///test_gaceta.db
MOCK_EXTERNAL_APIS=true
DISABLE_RATE_LIMITING=true
ENABLE_TEST_DATA=true

# Development Tools
ENABLE_SWAGGER_UI=true
ENABLE_REDOC=true
ENABLE_DEBUG_ENDPOINTS=true
```

## 📋 Configuration Validation

### Validation Script

Create a configuration validation script:

```python
# config_validator.py
import os
from typing import Dict, Any

def validate_config() -> Dict[str, Any]:
    """Validate all configuration settings."""
    errors = []
    warnings = []
    
    # Required settings
    required_vars = [
        'OPENAI_API_KEY',
        'APP_SECRET_API_KEY',
        'SECRET_KEY'
    ]
    
    for var in required_vars:
        if not os.getenv(var):
            errors.append(f"Missing required environment variable: {var}")
    
    # Validate OpenAI API key format
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and not api_key.startswith('sk-'):
        errors.append("Invalid OpenAI API key format")
    
    # Check database URL
    db_url = os.getenv('DATABASE_URL')
    if db_url and db_url.startswith('sqlite:') and 'production' in os.getenv('ENVIRONMENT', ''):
        warnings.append("Using SQLite in production is not recommended")
    
    return {
        'errors': errors,
        'warnings': warnings,
        'status': 'valid' if not errors else 'invalid'
    }

if __name__ == "__main__":
    result = validate_config()
    print(f"Configuration status: {result['status']}")
    
    if result['errors']:
        print("Errors:")
        for error in result['errors']:
            print(f"  - {error}")
    
    if result['warnings']:
        print("Warnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")
```

## 🚀 Production Deployment

### Production Checklist

Before deploying to production:

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS with `REQUIRE_HTTPS=true`
- [ ] Set up proper logging and monitoring
- [ ] Configure automated backups
- [ ] Set appropriate rate limits
- [ ] Enable security features
- [ ] Test all integrations
- [ ] Validate configuration

### Environment-Specific Configs

Create separate config files for each environment:

```bash
# Development
.env.development

# Staging
.env.staging

# Production
.env.production
```

Load the appropriate config based on environment:

```python
# config.py
import os
from dotenv import load_dotenv

env = os.getenv('ENVIRONMENT', 'development')
load_dotenv(f'.env.{env}')
```

!!! warning "Security Note"
    Never commit `.env` files containing secrets to version control. Use environment-specific configuration management tools in production.

## 📞 Getting Help

If you need help with configuration:

1. Check the [FAQ](../reference/faq.md)
2. Review [troubleshooting guide](../operations/troubleshooting.md)
3. Join our [Discord community](https://discord.gg/gacetachat)
4. Create an issue on [GitHub](https://github.com/gacetachat/gacetachat/issues)

!!! tip "Pro Tip"
    Start with the default configuration and modify settings gradually. Test changes in a development environment before applying to production.
