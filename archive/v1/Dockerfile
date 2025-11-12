# 🔥 ROBO-ACTIVIST DEMOCRATIC TRANSPARENCY CONTAINER 🔥
# Multi-stage build for production-ready GacetaChat deployment

FROM python:3.10-slim as base

# System dependencies for PDF processing and FAISS
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p gaceta_pdfs logs

# Environment setup
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8050/health || exit 1

# Expose ports
EXPOSE 8050 8512

# Production entrypoint
CMD ["python", "startup.py"]
