# GacetaChat 2.0 - Complete Architectural Overhaul Plan

> **From Research Prototype to Production-Ready Civic Engagement Platform**

**Status**: Planning Phase
**Target**: Grant-funded open data tool for democratic transparency
**Audience**: General public (primary), journalists, lawyers (secondary)
**Approach**: Complete rewrite, no migration from prototype

---

## Executive Summary

This document outlines a complete architectural overhaul to transform GacetaChat from an unreleased prototype into a production-grade civic engagement platform. The redesign focuses on:

1. **Simplified MVP**: Daily gazette summaries accessible to general public
2. **Modern Stack**: React + Tailwind + Next.js + Vercel
3. **Scalable Backend**: FastAPI + PostgreSQL + Redis + Celery
4. **Open Data Focus**: API-first design for transparency and reusability
5. **Grant Sustainability**: Architecture designed for civic tech funding opportunities

---

## Table of Contents

1. [Vision & Goals](#vision--goals)
2. [MVP Feature Set](#mvp-feature-set)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Database Design](#database-design)
6. [API Design](#api-design)
7. [Frontend Architecture](#frontend-architecture)
8. [Backend Architecture](#backend-architecture)
9. [DevOps & Deployment](#devops--deployment)
10. [Security & Compliance](#security--compliance)
11. [Performance & Scalability](#performance--scalability)
12. [Grant Positioning](#grant-positioning)
13. [Implementation Roadmap](#implementation-roadmap)
14. [Success Metrics](#success-metrics)

---

## Vision & Goals

### Mission Statement
**"Democratize access to Costa Rica's official gazette through AI-powered daily summaries, making government transparency accessible to every citizen."**

### Core Principles
1. **Public First**: Design for non-technical users, not experts
2. **Simplicity**: Daily summaries, no complex features
3. **Transparency**: Open-source code, open data APIs
4. **Sustainability**: Grant-funded, non-commercial model
5. **Accessibility**: Mobile-first, multilingual, inclusive design

### Success Criteria
- ✅ **Daily summaries** published automatically by 10 AM (Costa Rica time)
- ✅ **<3 second** page load times on mobile
- ✅ **10,000+ monthly** active users within 6 months
- ✅ **Open data API** with 100+ third-party integrations
- ✅ **99.5% uptime** SLA
- ✅ **Grant funding** secured within 12 months

---

## MVP Feature Set

### Phase 1: Core MVP (Weeks 1-8)

#### User-Facing Features
1. **Daily Summary View**
   - AI-generated summary of today's gazette (5-7 bullet points)
   - Key highlights with emoji icons
   - Publication date and source link
   - Mobile-responsive card layout

2. **Calendar Archive**
   - Browse summaries by date
   - Simple calendar picker
   - Last 90 days available (extend later)

3. **Search**
   - Basic keyword search across summaries
   - Filter by date range
   - Highlight matching terms

4. **Share**
   - Share individual summaries (Twitter, WhatsApp, email)
   - Copy link to clipboard
   - Embed code for websites

#### Backend Features
1. **Automated Scraper**
   - Daily PDF download (scheduled)
   - Text extraction and cleaning
   - Error handling and retry logic

2. **AI Summary Generation**
   - GPT-4o integration
   - Structured prompt engineering
   - Cost optimization (caching, token limits)

3. **Public API**
   - RESTful endpoints
   - No authentication required for read operations
   - Rate limiting (100 requests/hour per IP)

4. **Admin Dashboard**
   - Manual trigger for scraper
   - View generation logs
   - Edit/approve summaries before publication

### Out of Scope for MVP
- ❌ User accounts / authentication
- ❌ Comments / community features
- ❌ Advanced analytics / visualizations
- ❌ Email notifications
- ❌ Multi-language support (Spanish only for MVP)
- ❌ Chat/Q&A interface
- ❌ Twitter bot automation

---

## Technology Stack

### Frontend Stack

```
Next.js 14 (App Router)
├── React 18.2+              # UI framework
├── TypeScript 5.3+          # Type safety
├── Tailwind CSS 3.4+        # Utility-first styling
├── shadcn/ui                # Component library
├── TanStack Query v5        # Server state management
├── Zustand 4.4+             # Client state management
├── date-fns                 # Date utilities
├── Framer Motion 11+        # Animations
├── React Share              # Social sharing
└── Vercel Analytics         # Performance monitoring
```

**Why Next.js 14?**
- Server components for performance
- Built-in SEO optimization
- Edge runtime support
- Vercel deployment integration
- Great DX with TypeScript

**Why shadcn/ui?**
- Accessible by default (WCAG 2.1 AA)
- Copy-paste components (no dependency)
- Tailwind-based, fully customizable
- Production-ready patterns

### Backend Stack

```
FastAPI 0.109+
├── Python 3.11+             # Modern Python features
├── Pydantic 2.5+            # Data validation
├── SQLAlchemy 2.0+          # ORM
├── Alembic                  # Database migrations
├── PostgreSQL 15+           # Primary database
├── Redis 7+                 # Caching + rate limiting
├── Celery 5.3+              # Background tasks
├── RabbitMQ 3.12+           # Message broker
├── OpenAI Python SDK 1.x    # AI integration
├── LangChain 0.1+           # LLM orchestration
├── BeautifulSoup4           # Web scraping
├── PyPDF                    # PDF processing
├── Uvicorn + Gunicorn       # ASGI server
└── Sentry                   # Error tracking
```

**Why FastAPI?**
- Automatic OpenAPI documentation
- Native async support
- Best-in-class performance
- Excellent typing support
- Strong ecosystem

**Why PostgreSQL over SQLite?**
- Concurrent writes (critical for background jobs)
- Full-text search (for summaries)
- JSON/JSONB support
- Production-grade reliability
- Easy cloud hosting

### DevOps & Infrastructure

```
Hosting & Deployment
├── Vercel                   # Frontend hosting + CDN
├── Railway / Render         # Backend API hosting
├── Supabase / Neon          # Managed PostgreSQL
├── Upstash Redis            # Serverless Redis
├── GitHub Actions           # CI/CD pipelines
├── Docker                   # Containerization
└── Terraform                # Infrastructure as Code

Monitoring & Observability
├── Vercel Analytics         # Frontend performance
├── Sentry                   # Error tracking
├── Better Uptime            # Uptime monitoring
├── PostHog / Plausible      # Privacy-friendly analytics
└── Grafana + Prometheus     # Metrics (optional)
```

### Development Tools

```
Code Quality
├── ESLint + Prettier        # Linting + formatting (frontend)
├── Black + Ruff             # Formatting + linting (backend)
├── TypeScript strict mode   # Type checking
├── Husky + lint-staged      # Pre-commit hooks
└── Commitlint               # Conventional commits

Testing
├── Vitest                   # Unit tests (frontend)
├── Playwright               # E2E tests
├── Pytest                   # Unit tests (backend)
├── Pytest-cov               # Coverage reports
└── Locust                   # Load testing

Documentation
├── Storybook                # Component documentation
├── OpenAPI / Swagger        # API documentation
├── MkDocs Material          # User documentation
└── ADR (Architecture        # Decision records
    Decision Records)
```

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Mobile   │  │ Desktop  │  │ Tablet   │  │ Third-   │       │
│  │ Browser  │  │ Browser  │  │ Browser  │  │ Party    │       │
│  │          │  │          │  │          │  │ Apps     │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │            Next.js Frontend (Vercel)                    │    │
│  │  • Server Components (RSC)                             │    │
│  │  • Client Components (React)                           │    │
│  │  • Edge Middleware                                     │    │
│  │  • Static Generation (SSG) for archives               │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑ REST API
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         FastAPI Backend (Railway/Render)               │    │
│  │                                                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │  Public  │  │  Admin   │  │  Webhook │            │    │
│  │  │  API     │  │  API     │  │  API     │            │    │
│  │  └──────────┘  └──────────┘  └──────────┘            │    │
│  │                                                         │    │
│  │  Middleware: Rate Limiting, CORS, Auth, Logging       │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                                 │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Scraper    │  │  AI Summary  │  │   Search     │         │
│  │   Service    │  │  Service     │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ PostgreSQL   │  │    Redis     │  │   Object     │         │
│  │  (Supabase)  │  │  (Upstash)   │  │   Storage    │         │
│  │              │  │              │  │  (S3/R2)     │         │
│  │ • Summaries  │  │ • Cache      │  │ • PDF Files  │         │
│  │ • Metadata   │  │ • Sessions   │  │ • Backups    │         │
│  │ • Logs       │  │ • Rate Limit │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────────┐
│                 BACKGROUND JOBS LAYER                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │        Celery Workers + RabbitMQ                       │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │    │
│  │  │ Daily Scrape │  │ AI Summary   │  │ Cleanup     │ │    │
│  │  │ (9 AM daily) │  │ Generation   │  │ Old Files   │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐                   │    │
│  │  │ Health Check │  │ Retry Failed │                   │    │
│  │  │ (hourly)     │  │ Jobs         │                   │    │
│  │  └──────────────┘  └──────────────┘                   │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────────┐
│                 EXTERNAL SERVICES                                │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   OpenAI     │  │  Government  │  │   Sentry     │         │
│  │    API       │  │  Gazette     │  │  (Errors)    │         │
│  │  (GPT-4o)    │  │   Website    │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. DAILY AUTOMATED SCRAPING FLOW                                │
└─────────────────────────────────────────────────────────────────┘

Celery Beat Scheduler (9:00 AM CR Time)
    ↓
Trigger "scrape_daily_gazette" Task
    ↓
Celery Worker picks up task
    ↓
Scraper Service:
    1. HTTP GET → Government Website
    2. Parse HTML (BeautifulSoup)
    3. Download PDF → S3/R2
    4. Extract text (PyPDF)
    5. Store in PostgreSQL (status: "scraped")
    ↓
Trigger "generate_summary" Task
    ↓
AI Summary Service:
    1. Load PDF text from DB
    2. Chunk text (8k token limit)
    3. Call OpenAI API (GPT-4o)
    4. Parse structured summary
    5. Update DB (status: "summarized")
    ↓
Cache invalidation (Redis)
    ↓
Summary available at /api/summaries/latest

┌─────────────────────────────────────────────────────────────────┐
│ 2. USER REQUEST FLOW                                            │
└─────────────────────────────────────────────────────────────────┘

User visits homepage (/)
    ↓
Next.js Server Component
    ↓
Check Vercel Edge Cache (CDN)
    ├─ HIT → Return cached HTML (< 50ms)
    └─ MISS ↓
         API call: GET /api/summaries/latest
              ↓
         FastAPI Backend
              ↓
         Check Redis cache
              ├─ HIT → Return cached JSON (< 100ms)
              └─ MISS ↓
                   PostgreSQL query
                        ↓
                   Format response
                        ↓
                   Cache in Redis (TTL: 1 hour)
                        ↓
                   Return to Next.js
    ↓
Render React components
    ↓
Send HTML to browser
    ↓
Client hydration
    ↓
Interactive page ready

┌─────────────────────────────────────────────────────────────────┐
│ 3. SEARCH REQUEST FLOW                                          │
└─────────────────────────────────────────────────────────────────┘

User enters search query
    ↓
React component (client-side)
    ↓
Debounced API call: GET /api/search?q=impuestos
    ↓
Rate limiting check (Redis)
    ├─ Exceeded → 429 Too Many Requests
    └─ OK ↓
         PostgreSQL full-text search
              ↓
         Return results (with highlighting)
              ↓
         Cache in Redis (TTL: 10 min)
    ↓
Display results to user

┌─────────────────────────────────────────────────────────────────┐
│ 4. ADMIN MANUAL TRIGGER FLOW                                    │
└─────────────────────────────────────────────────────────────────┘

Admin clicks "Generate Summary" button
    ↓
POST /api/admin/trigger-summary
    ↓
JWT authentication check
    ├─ Invalid → 401 Unauthorized
    └─ Valid ↓
         Enqueue Celery task
              ↓
         Return task_id to admin
    ↓
Admin polls: GET /api/admin/tasks/{task_id}
    ↓
Task completes
    ↓
Admin sees result
```

---

## Database Design

### PostgreSQL Schema

```sql
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- CORE TABLES
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE gazettes (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    publication_date  DATE NOT NULL UNIQUE,
    source_url        TEXT NOT NULL,
    pdf_url           TEXT,  -- S3/R2 URL
    raw_text          TEXT,
    text_hash         VARCHAR(64),  -- SHA-256 for deduplication
    status            VARCHAR(20) NOT NULL DEFAULT 'pending',
                      -- pending, scraped, processing, summarized, failed
    error_message     TEXT,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Indexes
    INDEX idx_gazettes_date (publication_date DESC),
    INDEX idx_gazettes_status (status)
);

CREATE TABLE summaries (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gazette_id        UUID NOT NULL REFERENCES gazettes(id) ON DELETE CASCADE,
    summary_text      TEXT NOT NULL,
    bullet_points     JSONB NOT NULL,  -- Structured list
                      -- Example: [{"icon": "⚖️", "text": "New tax law..."}]
    key_topics        JSONB,  -- Array of topic tags
                      -- Example: ["taxation", "healthcare", "education"]
    metadata          JSONB,  -- AI generation metadata
                      -- Example: {"model": "gpt-4o", "tokens": 1234, "cost": 0.05}
    language          VARCHAR(5) DEFAULT 'es',
    is_published      BOOLEAN DEFAULT FALSE,
    published_at      TIMESTAMPTZ,
    generated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Full-text search
    search_vector     tsvector GENERATED ALWAYS AS (
                        to_tsvector('spanish', summary_text)
                      ) STORED,

    -- Indexes
    INDEX idx_summaries_gazette (gazette_id),
    INDEX idx_summaries_published (is_published, published_at DESC),
    INDEX idx_summaries_search USING GIN (search_vector)
);

CREATE TABLE summary_sections (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    summary_id        UUID NOT NULL REFERENCES summaries(id) ON DELETE CASCADE,
    section_type      VARCHAR(50) NOT NULL,
                      -- headline, economic, legal, health, education, other
    title             TEXT,
    content           TEXT NOT NULL,
    importance_score  INTEGER CHECK (importance_score BETWEEN 1 AND 10),
    order_index       INTEGER NOT NULL,

    INDEX idx_sections_summary (summary_id, order_index)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- ADMIN & MONITORING
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE admin_users (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email             VARCHAR(255) NOT NULL UNIQUE,
    hashed_password   VARCHAR(255) NOT NULL,
    full_name         VARCHAR(255),
    is_active         BOOLEAN DEFAULT TRUE,
    is_superuser      BOOLEAN DEFAULT FALSE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at     TIMESTAMPTZ,

    INDEX idx_admin_email (email)
);

CREATE TABLE scraping_logs (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gazette_id        UUID REFERENCES gazettes(id),
    task_type         VARCHAR(50) NOT NULL,  -- scrape, summarize, cleanup
    status            VARCHAR(20) NOT NULL,  -- pending, running, success, failed
    started_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at      TIMESTAMPTZ,
    duration_seconds  INTEGER,
    error_message     TEXT,
    metadata          JSONB,  -- Task-specific data

    INDEX idx_logs_gazette (gazette_id),
    INDEX idx_logs_status (status, started_at DESC)
);

CREATE TABLE api_usage (
    id                BIGSERIAL PRIMARY KEY,
    endpoint          VARCHAR(255) NOT NULL,
    method            VARCHAR(10) NOT NULL,
    ip_address        INET,
    user_agent        TEXT,
    response_status   INTEGER,
    response_time_ms  INTEGER,
    requested_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Partitioned by month for performance
    PARTITION BY RANGE (requested_at)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- ANALYTICS (FUTURE)
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE daily_stats (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date              DATE NOT NULL UNIQUE,
    page_views        INTEGER DEFAULT 0,
    unique_visitors   INTEGER DEFAULT 0,
    api_calls         INTEGER DEFAULT 0,
    shares            INTEGER DEFAULT 0,
    top_searches      JSONB,  -- Array of {query, count}

    INDEX idx_daily_stats_date (date DESC)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- FUNCTIONS & TRIGGERS
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_gazettes_updated_at
    BEFORE UPDATE ON gazettes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Auto-publish summary when marked as published
CREATE OR REPLACE FUNCTION auto_set_published_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_published = TRUE AND OLD.is_published = FALSE THEN
        NEW.published_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER auto_publish_summary
    BEFORE UPDATE ON summaries
    FOR EACH ROW
    EXECUTE FUNCTION auto_set_published_at();
```

### Redis Cache Strategy

```
# Cache Keys Structure

# Latest summary (TTL: 1 hour)
summary:latest → JSON {id, date, summary, bullets...}

# Summary by date (TTL: 24 hours for old, 1 hour for today)
summary:date:{YYYY-MM-DD} → JSON

# Search results (TTL: 10 minutes)
search:{query_hash} → JSON {results: [...], total: N}

# Rate limiting (TTL: 1 hour)
rate_limit:ip:{ip_address} → INTEGER (request count)
rate_limit:api_key:{key} → INTEGER (request count)

# API response cache (TTL: 5 minutes)
api_cache:{endpoint}:{params_hash} → JSON

# Session data (if adding auth later)
session:{session_id} → JSON {user_id, expires_at, ...}

# Background job status
celery:task:{task_id} → JSON {status, progress, result}
```

---

## API Design

### Public API Endpoints

```yaml
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PUBLIC API - No authentication required
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GET /api/v1/summaries/latest
  Description: Get today's summary (or most recent if today not available)
  Response: 200 OK
    {
      "id": "uuid",
      "publication_date": "2025-01-15",
      "summary": "Resumen general...",
      "bullet_points": [
        {"icon": "⚖️", "text": "Nueva ley de impuestos..."},
        {"icon": "🏥", "text": "Reforma al sistema de salud..."}
      ],
      "key_topics": ["taxation", "healthcare"],
      "source_url": "https://...",
      "pdf_url": "https://cdn.../2025-01-15.pdf",
      "published_at": "2025-01-15T10:00:00Z"
    }

GET /api/v1/summaries/{date}
  Description: Get summary for specific date (YYYY-MM-DD)
  Parameters:
    - date: string (path parameter)
  Response: 200 OK / 404 Not Found

GET /api/v1/summaries
  Description: List summaries with pagination
  Parameters:
    - page: integer (default: 1)
    - page_size: integer (default: 10, max: 100)
    - start_date: string (YYYY-MM-DD)
    - end_date: string (YYYY-MM-DD)
  Response: 200 OK
    {
      "items": [...],
      "total": 45,
      "page": 1,
      "page_size": 10,
      "has_next": true,
      "has_prev": false
    }

GET /api/v1/search
  Description: Full-text search across summaries
  Parameters:
    - q: string (required, min 3 chars)
    - page: integer (default: 1)
    - page_size: integer (default: 10)
  Rate Limit: 100 requests/hour per IP
  Response: 200 OK
    {
      "query": "impuestos",
      "results": [
        {
          "id": "uuid",
          "publication_date": "2025-01-15",
          "excerpt": "...nueva <mark>impuestos</mark> sobre...",
          "relevance_score": 0.92
        }
      ],
      "total": 12
    }

GET /api/v1/calendar
  Description: Get calendar view of available summaries
  Parameters:
    - year: integer (default: current year)
    - month: integer (default: current month)
  Response: 200 OK
    {
      "year": 2025,
      "month": 1,
      "days": [
        {"date": "2025-01-15", "has_summary": true},
        {"date": "2025-01-16", "has_summary": false}
      ]
    }

GET /api/v1/stats
  Description: Public statistics (for transparency)
  Response: 200 OK
    {
      "total_summaries": 245,
      "latest_date": "2025-01-15",
      "uptime_percentage": 99.8,
      "average_summary_time": "15 minutes"
    }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ADMIN API - JWT authentication required
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POST /api/v1/admin/login
  Description: Admin authentication
  Request:
    {
      "email": "admin@example.com",
      "password": "secure_password"
    }
  Response: 200 OK
    {
      "access_token": "jwt_token",
      "token_type": "bearer",
      "expires_in": 3600
    }

POST /api/v1/admin/scrape/trigger
  Description: Manually trigger scraping job
  Headers:
    Authorization: Bearer {jwt_token}
  Response: 202 Accepted
    {
      "task_id": "celery_task_id",
      "message": "Scraping job queued"
    }

GET /api/v1/admin/tasks/{task_id}
  Description: Check background task status
  Response: 200 OK
    {
      "task_id": "...",
      "status": "running",  // pending, running, success, failed
      "progress": 60,
      "result": null
    }

PATCH /api/v1/admin/summaries/{id}
  Description: Edit summary before publication
  Request:
    {
      "summary_text": "Edited text...",
      "bullet_points": [...],
      "is_published": true
    }
  Response: 200 OK

GET /api/v1/admin/logs
  Description: View scraping and processing logs
  Parameters:
    - page: integer
    - status: string (filter)
    - start_date: string
  Response: 200 OK

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# WEBHOOKS (Future)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POST /api/v1/webhooks/summary-published
  Description: Webhook triggered when new summary is published
  Payload:
    {
      "event": "summary.published",
      "data": { summary object }
    }
```

### API Response Standards

```typescript
// Success Response
{
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-01-15T10:00:00Z",
    "version": "v1"
  }
}

// Error Response
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "No summary found for date 2025-01-15",
    "details": {
      "date": "2025-01-15",
      "suggestion": "Try searching for a different date"
    }
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-01-15T10:00:00Z"
  }
}

// Rate Limit Headers
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705320000
```

---

## Frontend Architecture

### Next.js Project Structure

```
frontend/
├── app/                          # App Router (Next.js 14)
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Homepage (latest summary)
│   ├── archivo/                  # Archive pages
│   │   ├── page.tsx              # Calendar view
│   │   └── [date]/
│   │       └── page.tsx          # Summary by date
│   ├── buscar/                   # Search page
│   │   └── page.tsx
│   ├── api/                      # API routes (if needed)
│   │   └── revalidate/
│   │       └── route.ts
│   └── admin/                    # Admin dashboard
│       ├── layout.tsx
│       ├── page.tsx
│       └── [...routes]
│
├── components/                   # React components
│   ├── ui/                       # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── calendar.tsx
│   │   └── ...
│   ├── features/                 # Feature-specific components
│   │   ├── summary/
│   │   │   ├── SummaryCard.tsx
│   │   │   ├── BulletPoint.tsx
│   │   │   └── ShareButtons.tsx
│   │   ├── search/
│   │   │   ├── SearchBar.tsx
│   │   │   └── SearchResults.tsx
│   │   └── calendar/
│   │       ├── CalendarView.tsx
│   │       └── DayCell.tsx
│   └── layout/                   # Layout components
│       ├── Header.tsx
│       ├── Footer.tsx
│       └── Navigation.tsx
│
├── lib/                          # Utilities and configurations
│   ├── api/                      # API client
│   │   ├── client.ts             # Axios/Fetch wrapper
│   │   ├── endpoints.ts          # API endpoints
│   │   └── types.ts              # API response types
│   ├── hooks/                    # Custom React hooks
│   │   ├── useSummary.ts
│   │   ├── useSearch.ts
│   │   └── useCalendar.ts
│   ├── utils/                    # Helper functions
│   │   ├── date.ts
│   │   ├── text.ts
│   │   └── share.ts
│   └── constants.ts              # Constants
│
├── stores/                       # Zustand stores
│   ├── searchStore.ts
│   └── uiStore.ts
│
├── styles/                       # Global styles
│   └── globals.css
│
├── public/                       # Static assets
│   ├── images/
│   └── icons/
│
├── types/                        # TypeScript types
│   ├── summary.ts
│   └── api.ts
│
└── config files
    ├── next.config.js
    ├── tailwind.config.ts
    ├── tsconfig.json
    └── package.json
```

### Key Frontend Components

```typescript
// components/features/summary/SummaryCard.tsx
export interface SummaryCardProps {
  id: string;
  publicationDate: Date;
  summary: string;
  bulletPoints: BulletPoint[];
  keyTopics: string[];
  sourceUrl: string;
  pdfUrl?: string;
}

export function SummaryCard({ ... }: SummaryCardProps) {
  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="text-2xl font-bold">
              La Gaceta - {formatDate(publicationDate)}
            </CardTitle>
            <CardDescription>
              Resumen oficial del día
            </CardDescription>
          </div>
          <ShareButtons url={...} />
        </div>
      </CardHeader>

      <CardContent>
        <p className="text-lg mb-6">{summary}</p>

        <div className="space-y-4">
          {bulletPoints.map((point, i) => (
            <BulletPoint key={i} {...point} />
          ))}
        </div>

        <TopicTags topics={keyTopics} />
      </CardContent>

      <CardFooter>
        <Button asChild variant="outline">
          <a href={pdfUrl} target="_blank">
            Ver PDF original
          </a>
        </Button>
      </CardFooter>
    </Card>
  );
}
```

### State Management Strategy

```typescript
// stores/searchStore.ts (Zustand)
interface SearchState {
  query: string;
  results: SearchResult[];
  isLoading: boolean;
  error: string | null;
  setQuery: (query: string) => void;
  search: () => Promise<void>;
}

export const useSearchStore = create<SearchState>((set, get) => ({
  query: '',
  results: [],
  isLoading: false,
  error: null,

  setQuery: (query) => set({ query }),

  search: async () => {
    set({ isLoading: true, error: null });
    try {
      const results = await api.search(get().query);
      set({ results, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
}));

// lib/hooks/useSummary.ts (TanStack Query)
export function useSummary(date?: string) {
  return useQuery({
    queryKey: ['summary', date || 'latest'],
    queryFn: () => date
      ? api.getSummaryByDate(date)
      : api.getLatestSummary(),
    staleTime: 1000 * 60 * 60, // 1 hour
    gcTime: 1000 * 60 * 60 * 24, // 24 hours
  });
}
```

---

## Backend Architecture

### FastAPI Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app initialization
│   ├── config.py                 # Settings (Pydantic BaseSettings)
│   ├── database.py               # Database connection
│   │
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   ├── deps.py               # Dependencies (auth, db session)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py         # Main v1 router
│   │   │   ├── summaries.py      # Summary endpoints
│   │   │   ├── search.py         # Search endpoints
│   │   │   ├── admin.py          # Admin endpoints
│   │   │   └── webhooks.py       # Webhook handlers
│   │
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── security.py           # JWT, password hashing
│   │   ├── cache.py              # Redis client
│   │   └── rate_limit.py         # Rate limiting logic
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── gazette.py
│   │   ├── summary.py
│   │   ├── admin.py
│   │   └── logs.py
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── summary.py
│   │   ├── search.py
│   │   └── admin.py
│   │
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── scraper.py            # Web scraping service
│   │   ├── pdf_processor.py     # PDF text extraction
│   │   ├── ai_summary.py         # OpenAI integration
│   │   ├── search.py             # Full-text search
│   │   └── storage.py            # S3/R2 file storage
│   │
│   ├── tasks/                    # Celery tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py         # Celery configuration
│   │   ├── scraping.py           # Scraping tasks
│   │   ├── summarization.py      # AI summary tasks
│   │   └── cleanup.py            # Maintenance tasks
│   │
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── logging.py
│       └── exceptions.py
│
├── alembic/                      # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   ├── test_services/
│   └── test_tasks/
│
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml               # Poetry/Rye configuration
└── .env.example
```

### Key Backend Services

```python
# app/services/ai_summary.py
from openai import AsyncOpenAI
from typing import List, Dict

class AISummaryService:
    """
    Service for generating AI-powered summaries of gazette text.
    Uses GPT-4o with structured output for consistency.
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o"
        self.max_tokens = 2000

    async def generate_summary(
        self,
        gazette_text: str,
        date: str
    ) -> Dict:
        """
        Generate structured summary from gazette text.

        Returns:
            {
                "summary": "General overview...",
                "bullet_points": [
                    {"icon": "⚖️", "text": "..."},
                    ...
                ],
                "key_topics": ["taxation", "healthcare"],
                "metadata": {"tokens_used": 1234, "cost": 0.05}
            }
        """

        prompt = self._build_prompt(gazette_text, date)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=0.3,
            response_format={"type": "json_object"}  # Structured output
        )

        result = json.loads(response.choices[0].message.content)
        result["metadata"] = {
            "tokens_used": response.usage.total_tokens,
            "cost": self._calculate_cost(response.usage)
        }

        return result

    def _build_prompt(self, text: str, date: str) -> str:
        return f"""
        Analiza la siguiente Gaceta Oficial de Costa Rica del {date}.
        Genera un resumen en español para ciudadanos no expertos.

        TEXTO:
        {text[:8000]}  # Token limit

        FORMATO DE RESPUESTA (JSON):
        {{
            "summary": "Resumen general en 2-3 oraciones...",
            "bullet_points": [
                {{
                    "icon": "emoji apropiado",
                    "text": "Punto clave en lenguaje simple"
                }}
            ],
            "key_topics": ["tema1", "tema2", ...]
        }}

        INSTRUCCIONES:
        - 5-7 bullet points máximo
        - Lenguaje claro y accesible
        - Enfócate en cambios que afecten al ciudadano promedio
        - Usa emojis relevantes (⚖️ legal, 💰 económico, 🏥 salud, 🎓 educación)
        """

SYSTEM_PROMPT = """
Eres un asistente especializado en resumir documentos oficiales del
gobierno de Costa Rica para ciudadanos. Tu objetivo es hacer que la
información legal y gubernamental sea accesible para todos.

PRINCIPIOS:
1. Claridad sobre precisión técnica
2. Lenguaje simple, sin jerga legal
3. Resalta lo que afecta directamente a las personas
4. Sé neutral y objetivo
5. Usa formato estructurado y fácil de escanear
"""
```

### Celery Task Configuration

```python
# app/tasks/scraping.py
from celery import Task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery_app.task(bind=True, max_retries=3)
def scrape_daily_gazette(self: Task, date: str = None):
    """
    Scrape the official gazette for a given date.
    Scheduled daily at 9:00 AM Costa Rica time.

    Retries up to 3 times with exponential backoff.
    """
    try:
        date = date or get_today_cr_time()
        logger.info(f"Starting scrape for {date}")

        # Update status
        log = create_scraping_log(task_type="scrape", status="running")

        # Perform scraping
        scraper = GazetteScraper()
        result = scraper.scrape_date(date)

        # Save to database
        gazette = create_gazette(
            publication_date=date,
            source_url=result["source_url"],
            pdf_url=result["pdf_url"],
            raw_text=result["text"],
            status="scraped"
        )

        # Trigger summary generation
        generate_summary.delay(gazette.id)

        # Update log
        update_scraping_log(log.id, status="success")
        logger.info(f"Scrape completed for {date}")

        return {"gazette_id": str(gazette.id)}

    except Exception as exc:
        logger.error(f"Scrape failed: {exc}")
        update_scraping_log(log.id, status="failed", error=str(exc))

        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

@celery_app.task
def generate_summary(gazette_id: str):
    """Generate AI summary for a gazette."""
    logger.info(f"Generating summary for gazette {gazette_id}")

    gazette = get_gazette_by_id(gazette_id)

    # Call AI service
    ai_service = AISummaryService()
    summary_data = await ai_service.generate_summary(
        gazette.raw_text,
        str(gazette.publication_date)
    )

    # Save summary
    summary = create_summary(
        gazette_id=gazette_id,
        **summary_data
    )

    # Update gazette status
    update_gazette_status(gazette_id, "summarized")

    # Invalidate cache
    cache.delete(f"summary:latest")
    cache.delete(f"summary:date:{gazette.publication_date}")

    logger.info(f"Summary generated: {summary.id}")
    return {"summary_id": str(summary.id)}

# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    'scrape-daily-gazette': {
        'task': 'app.tasks.scraping.scrape_daily_gazette',
        'schedule': crontab(hour=9, minute=0),  # 9 AM daily
        'options': {'timezone': 'America/Costa_Rica'}
    },
    'cleanup-old-logs': {
        'task': 'app.tasks.cleanup.cleanup_old_logs',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    }
}
```

---

## DevOps & Deployment

### Infrastructure as Code (Terraform)

```hcl
# terraform/main.tf - Example configuration

terraform {
  required_providers {
    vercel = {
      source = "vercel/vercel"
      version = "~> 0.15"
    }
  }
}

# Frontend deployment (Vercel)
resource "vercel_project" "gacetachat_frontend" {
  name      = "gacetachat"
  framework = "nextjs"

  git_repository = {
    type = "github"
    repo = "your-org/gacetachat"
  }

  environment = [
    {
      key    = "NEXT_PUBLIC_API_URL"
      value  = var.backend_url
      target = ["production"]
    }
  ]
}

# Backend deployment (Railway/Render)
# Database (Supabase/Neon)
# Redis (Upstash)
# ... (more resources)
```

### Docker Configuration

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
```

```yaml
# docker-compose.yml - Local development
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: gacetachat
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/gacetachat
      REDIS_URL: redis://redis:6379
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --reload --host 0.0.0.0

  celery_worker:
    build: ./backend
    depends_on:
      - postgres
      - redis
      - rabbitmq
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/gacetachat
      REDIS_URL: redis://redis:6379
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    command: celery -A app.tasks.celery_app worker -l info

  celery_beat:
    build: ./backend
    depends_on:
      - redis
      - rabbitmq
    environment:
      REDIS_URL: redis://redis:6379
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672
    command: celery -A app.tasks.celery_app beat -l info

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app tests/

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run linting
        run: |
          cd frontend
          npm run lint

      - name: Run tests
        run: |
          cd frontend
          npm run test

      - name: Build
        run: |
          cd frontend
          npm run build

  deploy-frontend:
    needs: [test-frontend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'

  deploy-backend:
    needs: [test-backend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: gacetachat-backend
```

---

## Security & Compliance

### Security Checklist

```markdown
## Application Security

### Authentication & Authorization
- [ ] JWT tokens with short expiration (1 hour)
- [ ] Secure password hashing (bcrypt, argon2)
- [ ] HTTPS only (no HTTP allowed)
- [ ] CSRF protection for admin endpoints
- [ ] Rate limiting on all public endpoints
- [ ] API key rotation mechanism

### Data Protection
- [ ] Environment variables for secrets (no hardcoding)
- [ ] Database connection encryption (SSL/TLS)
- [ ] PDF storage encryption at rest (S3/R2)
- [ ] Sanitize all user inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS protection (CSP headers)

### Infrastructure Security
- [ ] Firewall rules (restrict DB access)
- [ ] DDoS protection (Cloudflare/Vercel)
- [ ] Regular security updates (Dependabot)
- [ ] Secrets scanning (GitHub)
- [ ] Vulnerability scanning (Snyk/Trivy)
- [ ] Backup encryption

### Compliance & Privacy
- [ ] GDPR compliance (if handling EU users)
- [ ] Privacy policy
- [ ] Terms of service
- [ ] Cookie consent (if using cookies)
- [ ] Data retention policy
- [ ] Right to deletion mechanism

### Monitoring & Incident Response
- [ ] Error tracking (Sentry)
- [ ] Security logging
- [ ] Anomaly detection
- [ ] Incident response plan
- [ ] Regular security audits
```

### Environment Variables Management

```bash
# .env.example
# Copy to .env and fill in values

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://user:password@host:port

# OpenAI
OPENAI_API_KEY=sk-xxx

# Storage (S3/R2)
S3_BUCKET_NAME=gacetachat-pdfs
S3_ACCESS_KEY=xxx
S3_SECRET_KEY=xxx
S3_REGION=auto

# Application
SECRET_KEY=xxx  # Generate with: openssl rand -hex 32
ENVIRONMENT=production  # development, staging, production
LOG_LEVEL=INFO
ALLOWED_ORIGINS=https://gacetachat.cr

# Monitoring
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# Rate Limiting
RATE_LIMIT_PER_HOUR=100
RATE_LIMIT_BURST=10
```

---

## Performance & Scalability

### Performance Targets

```markdown
## Performance SLAs

### Response Times (95th percentile)
- Homepage load: < 1 second
- API requests: < 300ms
- Search queries: < 500ms
- PDF download: < 2 seconds

### Availability
- Uptime: 99.5% (< 4 hours downtime/month)
- Error rate: < 0.1%

### Scalability
- Support 10,000 daily active users
- Handle 100 requests/second
- Store 10 years of gazette data (~3,650 documents)
```

### Optimization Strategies

```markdown
## Caching Strategy

### CDN Caching (Vercel Edge)
- Static assets: 1 year
- HTML pages: 1 hour
- API responses (public): 5 minutes

### Redis Caching
- Latest summary: 1 hour
- Historical summaries: 24 hours
- Search results: 10 minutes
- API metadata: 1 hour

### Database Optimization
- Indexes on: publication_date, is_published, search_vector
- Connection pooling (max 20 connections)
- Query result caching
- Materialized views for analytics

## Cost Optimization

### AI API Costs
- Use GPT-3.5-turbo for drafts, GPT-4o for final
- Implement aggressive token limiting
- Cache AI responses indefinitely
- Batch processing where possible
- Estimated cost: $20-50/month for daily summaries

### Infrastructure Costs (Estimated)
- Vercel (Frontend): $0-20/month (Hobby plan)
- Railway (Backend): $20/month (Starter plan)
- Supabase (Database): $25/month (Pro plan)
- Upstash Redis: $10/month (Pay-as-you-go)
- Cloudflare R2 (Storage): $5/month (1000 PDFs)
- **Total: ~$80-100/month**
```

---

## Grant Positioning

### Why Funders Should Support GacetaChat

```markdown
## Value Proposition for Grant Funders

### Democratic Impact
1. **Transparency**: Makes government documents accessible to all citizens
2. **Civic Engagement**: Empowers informed participation in democracy
3. **Digital Divide**: Bridges gap between legal experts and general public
4. **Open Data**: Creates reusable public infrastructure

### Technical Excellence
1. **Modern Stack**: Production-ready, scalable architecture
2. **Open Source**: Fully transparent, community-driven development
3. **API-First**: Enables third-party innovation and integration
4. **Cost-Effective**: Lean architecture, minimal operational costs

### Sustainability Model
1. **Grant Funding**: Initial development and launch
2. **Institutional Partnerships**: Journalism schools, NGOs, legal aid
3. **API Licensing**: Premium features for commercial users
4. **Cloud Credits**: Apply for cloud provider civic tech programs

### Measurable Outcomes
1. **User Growth**: Track monthly active users
2. **API Usage**: Monitor third-party integrations
3. **Media Coverage**: Track citations in news articles
4. **Cost Savings**: Measure time saved for researchers/journalists
5. **Civic Impact**: Survey user understanding of government
```

### Target Funding Sources

```markdown
## Potential Grant Opportunities

### Civic Tech Grants
- [ ] Knight Foundation (Media Innovation)
- [ ] Mozilla Foundation (Trustworthy AI)
- [ ] Open Society Foundations (Democracy & Rights)
- [ ] Omidyar Network (Governance & Citizen Engagement)
- [ ] Fast Forward (Tech Nonprofits)

### Regional/Latin America
- [ ] IDB Lab (Innovation in Latin America)
- [ ] CAF (Development Bank of Latin America)
- [ ] Costa Rican government innovation funds
- [ ] USAID Central America programs

### Tech Company Programs
- [ ] Google.org AI for Social Good
- [ ] AWS Imagine Grant
- [ ] Microsoft AI for Good
- [ ] GitHub Sponsors (for open source)
- [ ] Vercel Sponsorship Program

### Academic/Research
- [ ] University partnerships (journalism, law schools)
- [ ] Research grants (digital democracy studies)
- [ ] Student capstone projects

## Grant Application Materials Needed

1. **Project Brief** (2 pages)
   - Problem statement
   - Solution overview
   - Impact metrics
   - Budget breakdown

2. **Technical Architecture** (this document)
   - System design
   - Scalability plan
   - Security measures

3. **Team Bios**
   - Developer profiles
   - Advisory board (if any)
   - Partner organizations

4. **Budget & Timeline**
   - Development phases
   - Operational costs
   - Milestone deliverables

5. **Impact Measurement Plan**
   - User growth targets
   - Engagement metrics
   - Civic impact assessment
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Week 1-2: Backend Setup**
- [ ] Set up PostgreSQL database (Supabase)
- [ ] Create database schema and migrations
- [ ] Set up FastAPI project structure
- [ ] Implement core API endpoints (summaries CRUD)
- [ ] Set up Redis caching
- [ ] Configure error tracking (Sentry)

**Week 3-4: Frontend Setup**
- [ ] Create Next.js project with TypeScript
- [ ] Set up Tailwind + shadcn/ui
- [ ] Build core components (SummaryCard, Layout)
- [ ] Implement homepage (latest summary)
- [ ] Set up API client with React Query
- [ ] Deploy to Vercel (staging)

**Deliverable**: Basic working prototype (manual data entry)

### Phase 2: Automation (Weeks 5-6)

**Week 5: Scraping & Processing**
- [ ] Implement web scraper for official gazette
- [ ] Build PDF text extraction service
- [ ] Set up S3/R2 storage for PDFs
- [ ] Create Celery task structure
- [ ] Implement daily scraping schedule

**Week 6: AI Integration**
- [ ] Integrate OpenAI API
- [ ] Develop prompt engineering for summaries
- [ ] Test summary quality
- [ ] Implement cost optimization (caching, token limits)
- [ ] Add admin review workflow

**Deliverable**: Fully automated daily pipeline

### Phase 3: Core Features (Weeks 7-8)

**Week 7: Search & Archive**
- [ ] Implement full-text search (PostgreSQL)
- [ ] Build calendar archive view
- [ ] Add search UI components
- [ ] Optimize search performance

**Week 8: Polish & Testing**
- [ ] Add social sharing functionality
- [ ] Implement responsive design
- [ ] Write E2E tests (Playwright)
- [ ] Performance optimization
- [ ] SEO optimization

**Deliverable**: Production-ready MVP

### Phase 4: Launch (Week 9-10)

**Week 9: Pre-Launch**
- [ ] Security audit
- [ ] Load testing
- [ ] Set up monitoring dashboards
- [ ] Write user documentation
- [ ] Prepare launch communications

**Week 10: Launch**
- [ ] Deploy to production
- [ ] Soft launch (beta users)
- [ ] Monitor errors and performance
- [ ] Gather user feedback
- [ ] Public announcement

**Deliverable**: Live public platform

### Phase 5: Post-Launch (Ongoing)

**Month 2-3: Growth & Iteration**
- [ ] Analyze user behavior
- [ ] Improve AI summaries based on feedback
- [ ] Add requested features
- [ ] Build API documentation portal
- [ ] Onboard third-party developers

**Month 4-6: Sustainability**
- [ ] Apply for grants
- [ ] Establish partnerships
- [ ] Build community
- [ ] Open source repository
- [ ] Plan Phase 2 features

---

## Success Metrics

### KPIs to Track

```markdown
## User Metrics
- Monthly Active Users (MAU)
  - Target: 10,000 by Month 6
- Daily Active Users (DAU)
  - Target: 1,000 by Month 6
- User Retention (7-day, 30-day)
  - Target: 40% (7-day), 20% (30-day)
- Average Session Duration
  - Target: 3+ minutes

## Engagement Metrics
- Summaries viewed per user
  - Target: 5+ per month
- Search queries per user
  - Target: 2+ per month
- Share button clicks
  - Target: 5% of page views
- PDF downloads
  - Target: 10% of page views

## Technical Metrics
- API Response Time (p95)
  - Target: < 300ms
- Error Rate
  - Target: < 0.1%
- Uptime
  - Target: 99.5%
- Page Load Time (mobile)
  - Target: < 3 seconds

## Business Metrics
- API Usage (third-party)
  - Target: 10+ integrations by Month 6
- Media Citations
  - Target: 50+ by Month 6
- Grant Funding Secured
  - Target: $50,000+ by Month 12
- Monthly Operating Cost
  - Target: < $100/month
```

### Analytics Implementation

```typescript
// lib/analytics.ts
import { track } from '@vercel/analytics';

export const analytics = {
  // Page views
  pageView: (path: string) => {
    track('page_view', { path });
  },

  // User actions
  summaryViewed: (date: string) => {
    track('summary_viewed', { date });
  },

  searchPerformed: (query: string, resultCount: number) => {
    track('search', { query, result_count: resultCount });
  },

  pdfDownloaded: (date: string) => {
    track('pdf_download', { date });
  },

  shareClicked: (platform: string, date: string) => {
    track('share', { platform, date });
  },
};
```

---

## Appendix

### Technology Alternatives Considered

```markdown
## Frontend Framework
✅ **Chosen: Next.js 14**
- Excellent DX, Vercel integration, React ecosystem
- Alternatives considered:
  - Remix: Good SSR, but smaller ecosystem
  - SvelteKit: Great performance, but smaller talent pool
  - Astro: Excellent for content sites, but less interactive

## Backend Framework
✅ **Chosen: FastAPI**
- Modern Python, excellent performance, automatic docs
- Alternatives considered:
  - Django: More batteries included, but heavier
  - Flask: Lighter, but less structure
  - Node.js (NestJS): Good, but team prefers Python

## Database
✅ **Chosen: PostgreSQL**
- Robust, full-text search, JSON support
- Alternatives considered:
  - MySQL: Good, but lacks some features
  - MongoDB: Flexible schema, but less suited for structured data
  - SQLite: Simple, but limited concurrency

## Hosting
✅ **Chosen: Vercel + Railway**
- Great DX, affordable, integrated
- Alternatives considered:
  - AWS: More complex, higher costs
  - Google Cloud: Good, but similar complexity
  - Netlify + Render: Similar to Vercel + Railway
```

### Open Questions & Future Decisions

```markdown
## To Be Decided

1. **Multi-language Support**
   - When to add English translation?
   - Use human translators or AI?

2. **Mobile Apps**
   - Build native apps or PWA sufficient?
   - React Native vs. Flutter?

3. **Email Notifications**
   - Which email service? (SendGrid, Resend, AWS SES)
   - Opt-in or opt-out?

4. **Community Features**
   - Comments system (in-house or Disqus)?
   - User-generated content moderation?

5. **Monetization**
   - Free API tier limits?
   - Premium features for commercial users?
```

---

## Conclusion

This architectural overhaul transforms GacetaChat from a research prototype into a production-ready civic engagement platform. The design prioritizes:

1. **Simplicity**: MVP focuses on core value (daily summaries)
2. **Scalability**: Modern stack handles growth
3. **Sustainability**: Grant-friendly, low operational costs
4. **Transparency**: Open source, public APIs
5. **Impact**: Measurable democratic outcomes

**Next Steps:**
1. Review and approve this architecture plan
2. Set up development environment
3. Begin Phase 1 implementation
4. Prepare grant applications

**Estimated Timeline**: 10 weeks to public launch
**Estimated Budget**: $5,000-10,000 development + $100/month operations

---

**Document Version**: 1.0
**Last Updated**: 2025-01-15
**Authors**: GacetaChat Development Team
**Status**: Ready for Implementation
