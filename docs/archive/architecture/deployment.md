# Deployment Architecture

This document describes the deployment strategies, infrastructure requirements, and operational procedures for the GacetaChat platform.

## Deployment Overview

GacetaChat supports multiple deployment models to accommodate different use cases, from local development to enterprise-scale production environments.

## Deployment Models

### 1. Local Development
- **Environment**: Developer workstation
- **Database**: SQLite
- **Dependencies**: Python virtual environment
- **Purpose**: Development and testing

### 2. Single Server Deployment
- **Environment**: VPS or dedicated server
- **Database**: SQLite or PostgreSQL
- **Web Server**: Nginx + Gunicorn
- **Purpose**: Small to medium-scale production

### 3. Containerized Deployment
- **Environment**: Docker containers
- **Orchestration**: Docker Compose or Kubernetes
- **Database**: PostgreSQL container
- **Purpose**: Scalable production deployment

### 4. Cloud Deployment
- **Environment**: AWS, GCP, or Azure
- **Database**: Managed database service
- **Services**: Managed services for scaling
- **Purpose**: Enterprise-scale production

## Infrastructure Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **Memory**: 4GB RAM
- **Storage**: 20GB SSD
- **Network**: 10 Mbps bandwidth
- **OS**: Linux (Ubuntu 20.04+ recommended)

### Recommended Requirements
- **CPU**: 4+ cores
- **Memory**: 8GB+ RAM
- **Storage**: 100GB+ SSD
- **Network**: 100 Mbps bandwidth
- **OS**: Linux (Ubuntu 22.04 LTS)

### Production Requirements
- **CPU**: 8+ cores
- **Memory**: 16GB+ RAM
- **Storage**: 500GB+ SSD
- **Network**: 1 Gbps bandwidth
- **Load Balancer**: High availability setup

## Docker Deployment

### Docker Compose Configuration
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/gacetachat
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./gaceta_pdfs:/app/gaceta_pdfs
      - ./logs:/app/logs

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=gacetachat
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
```

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

## Kubernetes Deployment

### Namespace Configuration
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: gacetachat
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gacetachat-web
  namespace: gacetachat
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gacetachat-web
  template:
    metadata:
      labels:
        app: gacetachat-web
    spec:
      containers:
      - name: web
        image: gacetachat:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: gacetachat-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: gacetachat-service
  namespace: gacetachat
spec:
  selector:
    app: gacetachat-web
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Cloud Deployment

### AWS Architecture
```yaml
# Infrastructure as Code (Terraform)
provider "aws" {
  region = var.aws_region
}

# VPC and Networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "gacetachat-vpc"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "gacetachat-cluster"

  capacity_providers = ["FARGATE"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight           = 1
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier             = "gacetachat-db"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_encrypted      = true
  
  db_name  = "gacetachat"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = true
}
```

### GCP Architecture
```yaml
# Cloud Run Service
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: gacetachat
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/memory: "2Gi"
        run.googleapis.com/cpu: "1"
    spec:
      containers:
      - image: gcr.io/project-id/gacetachat:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: gacetachat-secrets
              key: database-url
        resources:
          limits:
            memory: "2Gi"
            cpu: "1"
```

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.10
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: Run tests
      run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: |
        docker build -t gacetachat:${{ github.sha }} .
        docker tag gacetachat:${{ github.sha }} gacetachat:latest
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push gacetachat:${{ github.sha }}
        docker push gacetachat:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        # Deploy to your chosen platform
        kubectl set image deployment/gacetachat-web web=gacetachat:${{ github.sha }}
        kubectl rollout status deployment/gacetachat-web
```

## Environment Configuration

### Environment Variables
```bash
# Application Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/database
REDIS_URL=redis://localhost:6379

# External Services
OPENAI_API_KEY=your-openai-api-key
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret

# Storage Configuration
STORAGE_BACKEND=s3
S3_BUCKET_NAME=gacetachat-documents
S3_REGION=us-east-1
S3_ACCESS_KEY_ID=your-access-key
S3_SECRET_ACCESS_KEY=your-secret-key

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

### Configuration Files
```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    
class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///dev.db'
    
class ProductionConfig(Config):
    DEBUG = False
    # Production-specific settings
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///test.db'
```

## Monitoring and Logging

### Application Monitoring
```python
# monitoring.py
import logging
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
```python
# health.py
from flask import Flask, jsonify
import psutil
import redis

app = Flask(__name__)

@app.route('/health')
def health_check():
    """System health check endpoint"""
    try:
        # Check database connectivity
        db_status = check_database()
        
        # Check Redis connectivity
        redis_status = check_redis()
        
        # Check system resources
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'redis': redis_status,
            'memory_usage': memory_usage,
            'cpu_usage': cpu_usage
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
```

## Security Considerations

### SSL/TLS Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Secrets Management
```yaml
# Kubernetes Secrets
apiVersion: v1
kind: Secret
metadata:
  name: gacetachat-secrets
type: Opaque
data:
  database-url: base64-encoded-url
  openai-api-key: base64-encoded-key
  oauth-client-secret: base64-encoded-secret
```

## Backup and Recovery

### Database Backup
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="gacetachat"

# Create backup
pg_dump $DATABASE_URL > $BACKUP_DIR/gacetachat_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/gacetachat_$DATE.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/gacetachat_$DATE.sql.gz s3://gacetachat-backups/

# Clean up old backups
find $BACKUP_DIR -name "gacetachat_*.sql.gz" -mtime +7 -delete
```

### Disaster Recovery
```bash
#!/bin/bash
# restore.sh
BACKUP_FILE=$1

# Stop application
kubectl scale deployment gacetachat-web --replicas=0

# Restore database
gunzip -c $BACKUP_FILE | psql $DATABASE_URL

# Restart application
kubectl scale deployment gacetachat-web --replicas=3
```

## Performance Optimization

### Caching Strategy
```python
# caching.py
import redis
from functools import wraps

redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL'))

def cache_result(expiration=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = redis_client.get(cache_key)
            
            if cached_result:
                return json.loads(cached_result)
            
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### Database Optimization
```sql
-- Database indexes for performance
CREATE INDEX idx_documents_date ON documents(created_at);
CREATE INDEX idx_chunks_document_id ON chunks(document_id);
CREATE INDEX idx_embeddings_similarity ON embeddings USING ivfflat (vector vector_cosine_ops);
```

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Session state management
- Database connection pooling
- Distributed caching

### Vertical Scaling
- Resource monitoring
- Performance profiling
- Bottleneck identification
- Capacity planning

## Troubleshooting

### Common Issues
1. **Database Connection Failures**
   - Check connection string
   - Verify database is running
   - Check firewall rules

2. **High Memory Usage**
   - Monitor vector index size
   - Implement pagination
   - Optimize queries

3. **Slow Response Times**
   - Enable caching
   - Optimize database queries
   - Scale horizontally

### Debugging Tools
```bash
# Log analysis
kubectl logs -f deployment/gacetachat-web

# Performance monitoring
kubectl top pods -n gacetachat

# Database monitoring
psql $DATABASE_URL -c "SELECT * FROM pg_stat_activity;"
```

## Deployment Checklist

### Pre-deployment
- [ ] Run all tests
- [ ] Security scan
- [ ] Performance testing
- [ ] Backup current state
- [ ] Prepare rollback plan

### Deployment
- [ ] Deploy to staging
- [ ] Validate staging deployment
- [ ] Deploy to production
- [ ] Run smoke tests
- [ ] Monitor system health

### Post-deployment
- [ ] Verify all services running
- [ ] Check application logs
- [ ] Monitor performance metrics
- [ ] Update documentation
- [ ] Notify stakeholders
