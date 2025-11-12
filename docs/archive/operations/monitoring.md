# Monitoring and Observability

This document outlines the monitoring, observability, and alerting strategies for the GacetaChat platform.

## Overview

Comprehensive monitoring and observability are critical for maintaining system reliability, performance, and user satisfaction. GacetaChat implements a multi-layered monitoring approach covering infrastructure, application, and business metrics.

## Monitoring Architecture

### Three Pillars of Observability

#### 1. Metrics
- **System Metrics**: CPU, memory, disk, network
- **Application Metrics**: Response times, error rates, throughput
- **Business Metrics**: User engagement, document processing, revenue

#### 2. Logs
- **Application Logs**: Structured logging for all components
- **System Logs**: Operating system and infrastructure logs
- **Audit Logs**: Security and compliance tracking

#### 3. Traces
- **Distributed Tracing**: Request flow across services
- **Performance Tracing**: Bottleneck identification
- **Error Tracing**: Root cause analysis

## Metrics Collection

### Application Metrics

#### Core Application Metrics
```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info

# Request metrics
REQUEST_COUNT = Counter(
    'gacetachat_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'gacetachat_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

# Document processing metrics
DOCUMENT_PROCESSING_TIME = Histogram(
    'gacetachat_document_processing_seconds',
    'Time taken to process documents',
    ['document_type']
)

PDF_PROCESSING_COUNT = Counter(
    'gacetachat_pdf_processed_total',
    'Total number of PDFs processed',
    ['status']
)

# Search metrics
SEARCH_QUERY_COUNT = Counter(
    'gacetachat_search_queries_total',
    'Total number of search queries',
    ['query_type']
)

SEARCH_RESPONSE_TIME = Histogram(
    'gacetachat_search_response_seconds',
    'Search response time in seconds'
)

# Database metrics
DATABASE_CONNECTIONS = Gauge(
    'gacetachat_database_connections',
    'Number of active database connections'
)

DATABASE_QUERY_TIME = Histogram(
    'gacetachat_database_query_seconds',
    'Database query execution time',
    ['query_type']
)

# Vector database metrics
FAISS_INDEX_SIZE = Gauge(
    'gacetachat_faiss_index_size',
    'Size of FAISS index'
)

FAISS_SEARCH_TIME = Histogram(
    'gacetachat_faiss_search_seconds',
    'FAISS search time in seconds'
)
```

#### Business Metrics
```python
# business_metrics.py
from prometheus_client import Counter, Gauge

# User metrics
ACTIVE_USERS = Gauge(
    'gacetachat_active_users',
    'Number of active users',
    ['time_period']
)

USER_REGISTRATIONS = Counter(
    'gacetachat_user_registrations_total',
    'Total user registrations'
)

# Usage metrics
DOCUMENTS_VIEWED = Counter(
    'gacetachat_documents_viewed_total',
    'Total documents viewed'
)

SEARCH_SUCCESS_RATE = Gauge(
    'gacetachat_search_success_rate',
    'Percentage of successful searches'
)

# Revenue metrics
SUBSCRIPTION_REVENUE = Gauge(
    'gacetachat_subscription_revenue',
    'Monthly subscription revenue'
)

API_USAGE_REVENUE = Gauge(
    'gacetachat_api_usage_revenue',
    'Monthly API usage revenue'
)
```

### Infrastructure Metrics

#### System Metrics
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'gacetachat'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
    scrape_interval: 5s

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['localhost:9187']

  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['localhost:9121']
```

#### Custom Metrics Collection
```python
# monitoring.py
import psutil
import time
from prometheus_client import Gauge, start_http_server

# System metrics
CPU_USAGE = Gauge('gacetachat_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('gacetachat_memory_usage_percent', 'Memory usage percentage')
DISK_USAGE = Gauge('gacetachat_disk_usage_percent', 'Disk usage percentage')

class SystemMonitor:
    def __init__(self):
        self.running = True
    
    def collect_metrics(self):
        """Collect system metrics"""
        while self.running:
            # CPU metrics
            CPU_USAGE.set(psutil.cpu_percent(interval=1))
            
            # Memory metrics
            memory = psutil.virtual_memory()
            MEMORY_USAGE.set(memory.percent)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            DISK_USAGE.set(disk.percent)
            
            time.sleep(60)  # Collect every minute
    
    def start(self):
        """Start metrics collection"""
        start_http_server(8001)  # Metrics endpoint
        self.collect_metrics()
```

## Logging Strategy

### Structured Logging
```python
# logging_config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'execution_time'):
            log_entry['execution_time'] = record.execution_time
            
        return json.dumps(log_entry)

def setup_logging():
    """Setup structured logging"""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger('gacetachat')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger
```

### Application Logging
```python
# app_logging.py
import logging
import time
from functools import wraps

logger = logging.getLogger('gacetachat')

def log_execution_time(func):
    """Decorator to log function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"Function {func.__name__} executed successfully",
                extra={
                    'function': func.__name__,
                    'execution_time': execution_time,
                    'status': 'success'
                }
            )
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Function {func.__name__} failed: {str(e)}",
                extra={
                    'function': func.__name__,
                    'execution_time': execution_time,
                    'status': 'error',
                    'error': str(e)
                }
            )
            raise
    return wrapper

def log_user_action(user_id, action, details=None):
    """Log user actions for audit purposes"""
    logger.info(
        f"User action: {action}",
        extra={
            'user_id': user_id,
            'action': action,
            'details': details or {},
            'audit': True
        }
    )
```

### Log Aggregation
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

## Alerting Rules

### Prometheus Alerting Rules
```yaml
# alert_rules.yml
groups:
  - name: gacetachat_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(gacetachat_requests_total{status_code=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} requests/second"

      # High response time
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(gacetachat_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s"

      # High memory usage
      - alert: HighMemoryUsage
        expr: gacetachat_memory_usage_percent > 90
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}%"

      # Database connection issues
      - alert: DatabaseConnectionIssues
        expr: gacetachat_database_connections > 50
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High database connection count"
          description: "Database connections: {{ $value }}"

      # PDF processing failures
      - alert: PDFProcessingFailures
        expr: rate(gacetachat_pdf_processed_total{status="failed"}[10m]) > 0.1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High PDF processing failure rate"
          description: "PDF processing failure rate: {{ $value }}"

      # Search performance degradation
      - alert: SearchPerformanceDegradation
        expr: histogram_quantile(0.95, rate(gacetachat_search_response_seconds_bucket[5m])) > 3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Search performance degradation"
          description: "95th percentile search time: {{ $value }}s"
```

### Alert Manager Configuration
```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@gacetachat.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
  - name: 'web.hook'
    email_configs:
      - to: 'admin@gacetachat.com'
        subject: 'GacetaChat Alert: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          Labels: {{ .Labels }}
          {{ end }}

    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#alerts'
        title: 'GacetaChat Alert'
        text: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}
```

## Dashboards

### Grafana Dashboard Configuration
```json
{
  "dashboard": {
    "title": "GacetaChat Monitoring Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(gacetachat_requests_total[5m])",
            "legendFormat": "{{ method }} {{ endpoint }}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(gacetachat_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(gacetachat_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "System Resources",
        "type": "graph",
        "targets": [
          {
            "expr": "gacetachat_cpu_usage_percent",
            "legendFormat": "CPU Usage"
          },
          {
            "expr": "gacetachat_memory_usage_percent",
            "legendFormat": "Memory Usage"
          }
        ]
      },
      {
        "title": "Search Performance",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(gacetachat_search_queries_total[5m])",
            "legendFormat": "Search Rate"
          },
          {
            "expr": "histogram_quantile(0.95, rate(gacetachat_search_response_seconds_bucket[5m]))",
            "legendFormat": "Search Response Time"
          }
        ]
      }
    ]
  }
}
```

### Business Intelligence Dashboard
```python
# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from prometheus_api_client import PrometheusConnect

class BusinessDashboard:
    def __init__(self):
        self.prometheus = PrometheusConnect(url="http://localhost:9090")
    
    def render_dashboard(self):
        st.title("GacetaChat Business Intelligence Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active_users = self.get_active_users()
            st.metric("Active Users", active_users)
        
        with col2:
            daily_queries = self.get_daily_queries()
            st.metric("Daily Queries", daily_queries)
        
        with col3:
            success_rate = self.get_success_rate()
            st.metric("Success Rate", f"{success_rate:.1%}")
        
        with col4:
            response_time = self.get_avg_response_time()
            st.metric("Avg Response Time", f"{response_time:.2f}s")
        
        # Charts
        self.render_usage_trends()
        self.render_error_analysis()
        self.render_performance_metrics()
    
    def get_active_users(self):
        """Get active users from Prometheus"""
        query = 'gacetachat_active_users{time_period="daily"}'
        result = self.prometheus.get_current_metric_value(metric_name=query)
        return result[0]['value'][1] if result else 0
    
    def render_usage_trends(self):
        """Render usage trends chart"""
        st.subheader("Usage Trends")
        
        # Get hourly request data
        query = 'rate(gacetachat_requests_total[1h])'
        data = self.prometheus.get_metric_range_data(
            metric_name=query,
            start_time='now-24h',
            end_time='now'
        )
        
        if data:
            df = pd.DataFrame(data)
            fig = px.line(df, x='timestamp', y='value', title='Request Rate (24h)')
            st.plotly_chart(fig)
```

## Health Checks

### Application Health Checks
```python
# health.py
from flask import Flask, jsonify
import psutil
import redis
import psycopg2
from datetime import datetime

app = Flask(__name__)

class HealthChecker:
    def __init__(self):
        self.checks = {
            'database': self.check_database,
            'redis': self.check_redis,
            'disk_space': self.check_disk_space,
            'memory': self.check_memory,
            'external_apis': self.check_external_apis
        }
    
    def check_database(self):
        """Check database connectivity"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            return {'status': 'healthy', 'latency': 0.01}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def check_redis(self):
        """Check Redis connectivity"""
        try:
            r = redis.Redis.from_url(REDIS_URL)
            r.ping()
            return {'status': 'healthy'}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def check_disk_space(self):
        """Check disk space"""
        disk_usage = psutil.disk_usage('/')
        free_percent = (disk_usage.free / disk_usage.total) * 100
        
        if free_percent < 10:
            return {'status': 'unhealthy', 'free_percent': free_percent}
        elif free_percent < 20:
            return {'status': 'warning', 'free_percent': free_percent}
        else:
            return {'status': 'healthy', 'free_percent': free_percent}
    
    def check_memory(self):
        """Check memory usage"""
        memory = psutil.virtual_memory()
        
        if memory.percent > 90:
            return {'status': 'unhealthy', 'usage_percent': memory.percent}
        elif memory.percent > 80:
            return {'status': 'warning', 'usage_percent': memory.percent}
        else:
            return {'status': 'healthy', 'usage_percent': memory.percent}
    
    def check_external_apis(self):
        """Check external API connectivity"""
        try:
            # Check OpenAI API
            import openai
            openai.models.list()
            return {'status': 'healthy', 'apis': ['openai']}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def get_health_status(self):
        """Get overall health status"""
        results = {}
        overall_status = 'healthy'
        
        for check_name, check_func in self.checks.items():
            result = check_func()
            results[check_name] = result
            
            if result['status'] == 'unhealthy':
                overall_status = 'unhealthy'
            elif result['status'] == 'warning' and overall_status == 'healthy':
                overall_status = 'warning'
        
        return {
            'status': overall_status,
            'timestamp': datetime.utcnow().isoformat(),
            'checks': results
        }

health_checker = HealthChecker()

@app.route('/health')
def health():
    """Health check endpoint"""
    health_status = health_checker.get_health_status()
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

@app.route('/health/live')
def liveness():
    """Kubernetes liveness probe"""
    return jsonify({'status': 'alive'}), 200

@app.route('/health/ready')
def readiness():
    """Kubernetes readiness probe"""
    health_status = health_checker.get_health_status()
    if health_status['status'] in ['healthy', 'warning']:
        return jsonify({'status': 'ready'}), 200
    else:
        return jsonify({'status': 'not ready'}), 503
```

## Performance Monitoring

### APM Integration
```python
# apm.py
from elastic_apm import Client
from elastic_apm.contrib.flask import ElasticAPM

# Initialize APM client
apm_client = Client(
    service_name='gacetachat',
    secret_token='your-secret-token',
    server_url='http://localhost:8200'
)

# Flask integration
def init_apm(app):
    apm = ElasticAPM(app)
    return apm

# Custom performance tracking
def track_performance(operation_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with apm_client.capture_span(operation_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Database Performance Monitoring
```python
# db_monitoring.py
import time
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    
    # Log slow queries
    if total > 1.0:  # Log queries taking more than 1 second
        logger.warning(
            f"Slow query detected: {total:.2f}s",
            extra={
                'query_time': total,
                'statement': statement[:200],  # First 200 chars
                'slow_query': True
            }
        )
    
    # Update metrics
    DATABASE_QUERY_TIME.labels(query_type='unknown').observe(total)
```

## Incident Response

### Incident Response Workflow
```python
# incident_response.py
import json
from datetime import datetime
from enum import Enum

class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentManager:
    def __init__(self):
        self.incidents = {}
    
    def create_incident(self, title, description, severity, affected_components):
        """Create new incident"""
        incident_id = self.generate_incident_id()
        incident = {
            'id': incident_id,
            'title': title,
            'description': description,
            'severity': severity.value,
            'affected_components': affected_components,
            'status': 'open',
            'created_at': datetime.utcnow().isoformat(),
            'updates': []
        }
        
        self.incidents[incident_id] = incident
        self.notify_stakeholders(incident)
        return incident_id
    
    def update_incident(self, incident_id, update_text, status=None):
        """Update existing incident"""
        if incident_id in self.incidents:
            incident = self.incidents[incident_id]
            update = {
                'timestamp': datetime.utcnow().isoformat(),
                'text': update_text,
                'status': status or incident['status']
            }
            incident['updates'].append(update)
            
            if status:
                incident['status'] = status
                
            self.notify_stakeholders(incident)
    
    def resolve_incident(self, incident_id, resolution_text):
        """Resolve incident"""
        self.update_incident(incident_id, resolution_text, 'resolved')
        
        # Generate post-incident report
        self.generate_post_incident_report(incident_id)
    
    def notify_stakeholders(self, incident):
        """Notify stakeholders about incident"""
        # Send notifications via email, Slack, etc.
        pass
    
    def generate_post_incident_report(self, incident_id):
        """Generate post-incident report"""
        incident = self.incidents[incident_id]
        report = {
            'incident_id': incident_id,
            'title': incident['title'],
            'summary': incident['description'],
            'timeline': incident['updates'],
            'root_cause': '',  # To be filled
            'resolution': '',  # To be filled
            'lessons_learned': '',  # To be filled
            'action_items': []  # To be filled
        }
        
        # Save report
        with open(f'incident_reports/{incident_id}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
```

## Monitoring Automation

### Auto-scaling Based on Metrics
```python
# auto_scaling.py
import boto3
from prometheus_api_client import PrometheusConnect

class AutoScaler:
    def __init__(self):
        self.prometheus = PrometheusConnect(url="http://localhost:9090")
        self.ec2 = boto3.client('ec2')
        self.autoscaling = boto3.client('autoscaling')
    
    def check_scaling_conditions(self):
        """Check if scaling is needed"""
        # Get current metrics
        cpu_usage = self.get_cpu_usage()
        memory_usage = self.get_memory_usage()
        request_rate = self.get_request_rate()
        
        # Scale up conditions
        if cpu_usage > 80 or memory_usage > 80 or request_rate > 1000:
            return 'scale_up'
        
        # Scale down conditions
        if cpu_usage < 30 and memory_usage < 30 and request_rate < 100:
            return 'scale_down'
        
        return 'no_change'
    
    def scale_up(self):
        """Scale up the application"""
        # Increase auto-scaling group desired capacity
        response = self.autoscaling.set_desired_capacity(
            AutoScalingGroupName='gacetachat-asg',
            DesiredCapacity=self.get_current_capacity() + 1
        )
        
        logger.info("Scaled up application", extra={'scaling_action': 'up'})
    
    def scale_down(self):
        """Scale down the application"""
        # Decrease auto-scaling group desired capacity
        current_capacity = self.get_current_capacity()
        if current_capacity > 1:  # Don't scale below 1 instance
            response = self.autoscaling.set_desired_capacity(
                AutoScalingGroupName='gacetachat-asg',
                DesiredCapacity=current_capacity - 1
            )
            
            logger.info("Scaled down application", extra={'scaling_action': 'down'})
```

This comprehensive monitoring and observability setup ensures that GacetaChat maintains high availability, performance, and reliability while providing actionable insights for continuous improvement.
