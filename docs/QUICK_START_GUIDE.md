# GacetaChat 2.0 - Quick Start Implementation Guide

> **From Zero to MVP in 10 Weeks**

This guide provides step-by-step instructions for implementing the complete rewrite of GacetaChat as outlined in [ARCHITECTURAL_OVERHAUL.md](./ARCHITECTURAL_OVERHAUL.md).

---

## Prerequisites

### Required Accounts
- [ ] GitHub account (for version control)
- [ ] Vercel account (frontend hosting) - [vercel.com](https://vercel.com)
- [ ] Railway account (backend hosting) - [railway.app](https://railway.app)
- [ ] Supabase account (database) - [supabase.com](https://supabase.com)
- [ ] Upstash account (Redis) - [upstash.com](https://upstash.com)
- [ ] Cloudflare account (R2 storage) - [cloudflare.com](https://cloudflare.com)
- [ ] OpenAI account (AI API) - [platform.openai.com](https://platform.openai.com)

### Required Software
- [ ] Node.js 20+ ([nodejs.org](https://nodejs.org))
- [ ] Python 3.11+ ([python.org](https://python.org))
- [ ] Git ([git-scm.com](https://git-scm.com))
- [ ] VS Code or preferred IDE
- [ ] Docker Desktop (optional, for local development)

### Estimated Costs
- **Development**: Free tiers sufficient
- **Production**: ~$100/month (see [GRANT_STRATEGY.md](./GRANT_STRATEGY.md))

---

## Phase 0: Setup (Week 0)

### Step 1: Create GitHub Repository

```bash
# Create new repository on GitHub
# Name: gacetachat-v2
# Description: AI-powered official gazette summaries for Costa Rica
# License: MIT
# Initialize with README

# Clone to local machine
git clone https://github.com/YOUR-USERNAME/gacetachat-v2.git
cd gacetachat-v2

# Create project structure
mkdir -p frontend backend docs scripts
touch .gitignore README.md
```

### Step 2: Set Up Project Management

**Create GitHub Project Board**:
- [ ] Column: To Do
- [ ] Column: In Progress
- [ ] Column: In Review
- [ ] Column: Done

**Create Issues for Each Phase**:
- [ ] Phase 1: Backend Foundation
- [ ] Phase 2: Frontend Foundation
- [ ] Phase 3: Automation
- [ ] Phase 4: Features & Polish
- [ ] Phase 5: Launch Preparation

### Step 3: Environment Setup

```bash
# Create .env.example files
cat > backend/.env.example << EOF
# Database
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://default:password@host:port

# OpenAI
OPENAI_API_KEY=sk-xxx

# Storage
S3_BUCKET_NAME=gacetachat-pdfs
S3_ACCESS_KEY=xxx
S3_SECRET_KEY=xxx
S3_ENDPOINT=https://xxx.r2.cloudflarestorage.com

# Application
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000

# Celery
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672
EOF

cat > frontend/.env.local.example << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000
EOF
```

---

## Phase 1: Backend Foundation (Weeks 1-2)

### Week 1: Database & API Setup

#### Day 1-2: Database Setup

**Create Supabase Project**:

1. Go to [supabase.com](https://supabase.com) → New Project
2. Name: `gacetachat-prod`
3. Database Password: Generate strong password
4. Region: Choose closest to Costa Rica (US East recommended)
5. Copy connection string from Settings → Database

**Create Database Schema**:

```bash
cd backend

# Create project structure
mkdir -p app/{api,core,models,schemas,services,tasks,utils}
touch app/__init__.py
touch app/{api,core,models,schemas,services,tasks,utils}/__init__.py

# Create database migration directory
pip install alembic
alembic init alembic

# Edit alembic.ini
# sqlalchemy.url = postgresql://user:password@host:port/dbname
```

**Create initial migration**:

```bash
# Create migration for core tables
alembic revision -m "create_core_tables"
```

Edit `alembic/versions/xxx_create_core_tables.py`:

```python
"""create core tables

Revision ID: xxx
Revises:
Create Date: 2025-01-15
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

def upgrade():
    # Gazettes table
    op.create_table(
        'gazettes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('publication_date', sa.Date, nullable=False, unique=True),
        sa.Column('source_url', sa.Text, nullable=False),
        sa.Column('pdf_url', sa.Text),
        sa.Column('raw_text', sa.Text),
        sa.Column('text_hash', sa.String(64)),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_gazettes_date', 'gazettes', ['publication_date'], postgresql_using='btree', postgresql_ops={'publication_date': 'DESC'})
    op.create_index('idx_gazettes_status', 'gazettes', ['status'])

    # Summaries table
    op.create_table(
        'summaries',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('gazette_id', UUID(as_uuid=True), sa.ForeignKey('gazettes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('summary_text', sa.Text, nullable=False),
        sa.Column('bullet_points', JSONB, nullable=False),
        sa.Column('key_topics', JSONB),
        sa.Column('metadata', JSONB),
        sa.Column('language', sa.String(5), server_default='es'),
        sa.Column('is_published', sa.Boolean, server_default='false'),
        sa.Column('published_at', sa.DateTime(timezone=True)),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_summaries_gazette', 'summaries', ['gazette_id'])
    op.create_index('idx_summaries_published', 'summaries', ['is_published', 'published_at'], postgresql_ops={'published_at': 'DESC'})

    # Add more tables as needed...

def downgrade():
    op.drop_table('summaries')
    op.drop_table('gazettes')
```

**Run migration**:

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:password@host:port/dbname"

# Run migration
alembic upgrade head
```

#### Day 3-5: FastAPI Application

**Create FastAPI app**:

```bash
# Install dependencies
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary pydantic pydantic-settings python-dotenv redis

# Create requirements.txt
pip freeze > requirements.txt
```

**Create `app/main.py`**:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="GacetaChat API",
    description="AI-powered official gazette summaries for Costa Rica",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "GacetaChat API v2.0",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers (add as we build them)
# from app.api.v1.router import api_router
# app.include_router(api_router, prefix="/api/v1")
```

**Create `app/core/config.py`**:

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    REDIS_URL: str

    # OpenAI
    OPENAI_API_KEY: str

    # Storage
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT: str

    # Application
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**Create `app/database.py`**:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Run locally**:

```bash
# Create .env file with your credentials
cp .env.example .env
# Edit .env with actual values

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Visit http://localhost:8000/docs to see API documentation
```

### Week 2: API Endpoints

#### Day 1-2: Models and Schemas

**Create `app/models/gazette.py`**:

```python
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Gazette(Base):
    __tablename__ = "gazettes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_date = Column(Date, nullable=False, unique=True, index=True)
    source_url = Column(Text, nullable=False)
    pdf_url = Column(Text)
    raw_text = Column(Text)
    text_hash = Column(String(64))
    status = Column(String(20), nullable=False, default="pending", index=True)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gazette_id = Column(UUID(as_uuid=True), ForeignKey("gazettes.id", ondelete="CASCADE"), nullable=False)
    summary_text = Column(Text, nullable=False)
    bullet_points = Column(JSONB, nullable=False)
    key_topics = Column(JSONB)
    metadata = Column(JSONB)
    language = Column(String(5), default="es")
    is_published = Column(Boolean, default=False, index=True)
    published_at = Column(DateTime(timezone=True))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
```

**Create `app/schemas/summary.py`**:

```python
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Dict, Optional
from uuid import UUID

class BulletPoint(BaseModel):
    icon: str = Field(..., description="Emoji icon")
    text: str = Field(..., description="Bullet point text")

class SummaryBase(BaseModel):
    summary_text: str
    bullet_points: List[BulletPoint]
    key_topics: Optional[List[str]] = None
    language: str = "es"

class SummaryResponse(SummaryBase):
    id: UUID
    publication_date: date
    source_url: str
    pdf_url: Optional[str] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SummaryListResponse(BaseModel):
    items: List[SummaryResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool
```

#### Day 3-5: API Routes

**Create `app/api/v1/summaries.py`**:

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models.gazette import Summary, Gazette
from app.schemas.summary import SummaryResponse, SummaryListResponse
from app.core.cache import get_redis, cache_response

router = APIRouter()

@router.get("/latest", response_model=SummaryResponse)
@cache_response(expire=3600)  # 1 hour cache
async def get_latest_summary(db: Session = Depends(get_db)):
    """Get the most recent published summary."""
    summary = db.query(Summary).join(Gazette).filter(
        Summary.is_published == True
    ).order_by(Gazette.publication_date.desc()).first()

    if not summary:
        raise HTTPException(status_code=404, detail="No summaries found")

    return summary

@router.get("/{date}", response_model=SummaryResponse)
@cache_response(expire=86400)  # 24 hours cache
async def get_summary_by_date(
    date: date,
    db: Session = Depends(get_db)
):
    """Get summary for a specific date (YYYY-MM-DD)."""
    summary = db.query(Summary).join(Gazette).filter(
        Gazette.publication_date == date,
        Summary.is_published == True
    ).first()

    if not summary:
        raise HTTPException(
            status_code=404,
            detail=f"No summary found for date {date}"
        )

    return summary

@router.get("/", response_model=SummaryListResponse)
async def list_summaries(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """List summaries with pagination and optional date filtering."""
    query = db.query(Summary).join(Gazette).filter(
        Summary.is_published == True
    )

    if start_date:
        query = query.filter(Gazette.publication_date >= start_date)
    if end_date:
        query = query.filter(Gazette.publication_date <= end_date)

    total = query.count()
    items = query.order_by(
        Gazette.publication_date.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()

    return SummaryListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=total > page * page_size,
        has_prev=page > 1
    )
```

**Create router and include in main app**:

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1 import summaries

api_router = APIRouter()
api_router.include_router(summaries.router, prefix="/summaries", tags=["summaries"])

# Add to app/main.py
from app.api.v1.router import api_router
app.include_router(api_router, prefix="/api/v1")
```

**Test endpoints**:

```bash
# Visit http://localhost:8000/docs
# Test GET /api/v1/summaries/latest
# Test GET /api/v1/summaries/{date}
# Test GET /api/v1/summaries
```

---

## Phase 2: Frontend Foundation (Weeks 3-4)

### Week 3: Next.js Setup

#### Day 1: Create Next.js Project

```bash
cd frontend

# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest . --typescript --tailwind --app --use-npm

# Install dependencies
npm install @tanstack/react-query zustand date-fns axios
npm install -D @types/node

# Install shadcn/ui
npx shadcn-ui@latest init

# Add components
npx shadcn-ui@latest add button card calendar badge
```

#### Day 2-3: Project Structure

```bash
# Create directory structure
mkdir -p app/(main)
mkdir -p components/{ui,features,layout}
mkdir -p lib/{api,hooks,utils}
mkdir -p types
mkdir -p stores

# Move app/page.tsx to app/(main)/page.tsx
```

**Create `lib/api/client.ts`**:

```typescript
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

**Create `lib/api/endpoints.ts`**:

```typescript
import { apiClient } from './client';
import type { SummaryResponse, SummaryListResponse } from '@/types/api';

export const summariesApi = {
  getLatest: async (): Promise<SummaryResponse> => {
    const { data } = await apiClient.get('/summaries/latest');
    return data;
  },

  getByDate: async (date: string): Promise<SummaryResponse> => {
    const { data } = await apiClient.get(`/summaries/${date}`);
    return data;
  },

  list: async (params?: {
    page?: number;
    page_size?: number;
    start_date?: string;
    end_date?: string;
  }): Promise<SummaryListResponse> => {
    const { data } = await apiClient.get('/summaries', { params });
    return data;
  },
};
```

**Create `types/api.ts`**:

```typescript
export interface BulletPoint {
  icon: string;
  text: string;
}

export interface SummaryResponse {
  id: string;
  publication_date: string;
  summary_text: string;
  bullet_points: BulletPoint[];
  key_topics?: string[];
  source_url: string;
  pdf_url?: string;
  published_at?: string;
}

export interface SummaryListResponse {
  items: SummaryResponse[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_prev: boolean;
}
```

#### Day 4-5: Core Components

**Create `components/features/summary/SummaryCard.tsx`**:

```typescript
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ExternalLink, FileText } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import type { SummaryResponse } from '@/types/api';

interface SummaryCardProps {
  summary: SummaryResponse;
}

export function SummaryCard({ summary }: SummaryCardProps) {
  const formattedDate = format(
    new Date(summary.publication_date),
    "EEEE, d 'de' MMMM 'de' yyyy",
    { locale: es }
  );

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-start gap-4">
          <div>
            <CardTitle className="text-2xl font-bold">
              La Gaceta Oficial
            </CardTitle>
            <CardDescription className="text-lg capitalize">
              {formattedDate}
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        <p className="text-lg leading-relaxed">
          {summary.summary_text}
        </p>

        <div className="space-y-3">
          {summary.bullet_points.map((point, index) => (
            <div
              key={index}
              className="flex gap-3 p-3 rounded-lg bg-muted/50"
            >
              <span className="text-2xl flex-shrink-0">
                {point.icon}
              </span>
              <p className="flex-1">{point.text}</p>
            </div>
          ))}
        </div>

        {summary.key_topics && summary.key_topics.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {summary.key_topics.map((topic) => (
              <Badge key={topic} variant="secondary">
                {topic}
              </Badge>
            ))}
          </div>
        )}
      </CardContent>

      <CardFooter className="flex gap-2">
        <Button asChild variant="outline">
          <a href={summary.source_url} target="_blank" rel="noopener noreferrer">
            <ExternalLink className="mr-2 h-4 w-4" />
            Ver en sitio oficial
          </a>
        </Button>
        {summary.pdf_url && (
          <Button asChild variant="outline">
            <a href={summary.pdf_url} target="_blank" rel="noopener noreferrer">
              <FileText className="mr-2 h-4 w-4" />
              Descargar PDF
            </a>
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
```

**Create `lib/hooks/useSummary.ts`**:

```typescript
import { useQuery } from '@tanstack/react-query';
import { summariesApi } from '@/lib/api/endpoints';

export function useLatestSummary() {
  return useQuery({
    queryKey: ['summary', 'latest'],
    queryFn: summariesApi.getLatest,
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}

export function useSummaryByDate(date: string) {
  return useQuery({
    queryKey: ['summary', date],
    queryFn: () => summariesApi.getByDate(date),
    enabled: !!date,
    staleTime: 1000 * 60 * 60 * 24, // 24 hours
  });
}
```

### Week 4: Pages and Layout

**Create `app/layout.tsx`**:

```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'GacetaChat - Resúmenes de La Gaceta Oficial de Costa Rica',
  description: 'Resúmenes diarios generados con IA de la Gaceta Oficial de Costa Rica',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

**Create `app/providers.tsx`**:

```typescript
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

**Create `app/(main)/page.tsx`**:

```typescript
'use client';

import { SummaryCard } from '@/components/features/summary/SummaryCard';
import { useLatestSummary } from '@/lib/hooks/useSummary';
import { Loader2 } from 'lucide-react';

export default function HomePage() {
  const { data: summary, isLoading, error } = useLatestSummary();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-red-500">Error al cargar el resumen</p>
      </div>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold mb-2">GacetaChat</h1>
        <p className="text-muted-foreground">
          Resúmenes diarios de La Gaceta Oficial de Costa Rica
        </p>
      </div>

      {summary && <SummaryCard summary={summary} />}
    </main>
  );
}
```

**Run frontend**:

```bash
npm run dev
# Visit http://localhost:3000
```

---

## Next Steps

Continue with:
- **Weeks 5-6**: Automation (scraping, AI, background jobs) - See [ARCHITECTURAL_OVERHAUL.md](./ARCHITECTURAL_OVERHAUL.md#phase-2-automation-weeks-5-6)
- **Weeks 7-8**: Features & Polish (search, calendar, sharing)
- **Weeks 9-10**: Launch Preparation (testing, deployment, monitoring)

---

## Deployment

### Deploy Backend to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init

# Add PostgreSQL
railway add

# Set environment variables
railway variables set OPENAI_API_KEY=sk-xxx
railway variables set SECRET_KEY=xxx
# ... (add all variables)

# Deploy
railway up
```

### Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Set production environment variable
vercel env add NEXT_PUBLIC_API_URL production
# Enter your Railway backend URL
```

---

## Troubleshooting

### Common Issues

**Database connection fails**:
- Check DATABASE_URL is correct
- Ensure Supabase project is not paused
- Check firewall rules allow connections

**CORS errors in frontend**:
- Add frontend URL to backend ALLOWED_ORIGINS
- Check API_URL is correct in frontend .env

**OpenAI API errors**:
- Verify API key is valid
- Check account has credits
- Monitor rate limits

### Getting Help

- GitHub Issues: [Create issue]
- Documentation: [docs/](./docs/)
- Community: [Discord/Slack link]

---

**Document Version**: 1.0
**Last Updated**: 2025-01-15
**Status**: Ready for Implementation
