# GacetaChat 2.0 - Complete Rewrite Implementation Plan

> **One Document. One Plan. Zero Bloat.**

**Goal**: Daily AI summaries of Costa Rica's official gazette, accessible to everyone.
**Timeline**: 4 weeks to launch (AI-accelerated with Claude Code Plus)
**Budget**: $32k dev + $130/month operations
**Stack**: Next.js + FastAPI + PostgreSQL + OpenAI

---

## What We're Building (MVP Only)

### User Story
"Maria opens her phone, sees today's gazette summarized in 5 bullet points with emojis. She understands what changed. Takes 30 seconds. That's it."

### Features (Week 1-10)
1. **Daily Summary** - Homepage shows today's summary (auto-generated)
2. **Archive** - Calendar to browse past 90 days
3. **Search** - Find summaries by keyword
4. **API** - Public REST API (no auth required)

### NOT Building (Phase 2+ or Never)
- ❌ User accounts
- ❌ Comments/community
- ❌ Email notifications
- ❌ Twitter bot
- ❌ Chat/Q&A interface
- ❌ Analytics dashboards
- ❌ Commitment tracking
- ❌ Any of the 60+ bloated docs in /docs

---

## Tech Stack

### Frontend
```
Next.js 14 (App Router) + React 18 + TypeScript
Tailwind CSS + shadcn/ui
Vercel (hosting)
```

### Backend
```
FastAPI + Python 3.11
PostgreSQL (Supabase)
Redis (Upstash)
Celery + RabbitMQ (background jobs)
Railway (hosting)
```

### AI & Storage
```
OpenAI GPT-4o (summaries)
Cloudflare R2 (PDF storage)
```

---

## Architecture (One Diagram)

```
┌─────────────────────────────────────────────────┐
│ USER                                             │
│ Opens phone → sees summary → done               │
└─────────────────────────────────────────────────┘
                    ↓↑ HTTPS
┌─────────────────────────────────────────────────┐
│ FRONTEND (Vercel)                                │
│ Next.js 14 - Server components + React          │
└─────────────────────────────────────────────────┘
                    ↓↑ REST API
┌─────────────────────────────────────────────────┐
│ BACKEND (Railway)                                │
│ FastAPI - Returns summaries from DB             │
└─────────────────────────────────────────────────┘
                    ↓↑ SQL
┌─────────────────────────────────────────────────┐
│ DATABASE (Supabase PostgreSQL)                   │
│ Tables: gazettes, summaries                     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ BACKGROUND JOB (Celery Worker)                   │
│ 9 AM daily: Scrape → Process → AI → DB          │
└─────────────────────────────────────────────────┘
```

---

## Database Schema (2 Tables)

```sql
CREATE TABLE gazettes (
    id UUID PRIMARY KEY,
    publication_date DATE UNIQUE NOT NULL,
    pdf_url TEXT,
    raw_text TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE summaries (
    id UUID PRIMARY KEY,
    gazette_id UUID REFERENCES gazettes(id),
    summary_text TEXT NOT NULL,
    bullet_points JSONB NOT NULL,  -- [{icon: "⚖️", text: "..."}]
    key_topics JSONB,               -- ["legal", "economic"]
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP
);

CREATE INDEX idx_summaries_published
ON summaries(is_published, published_at DESC);
```

---

## API Endpoints (4 Routes)

```
GET  /api/v1/summaries/latest      → Today's summary
GET  /api/v1/summaries/{date}      → Specific date (YYYY-MM-DD)
GET  /api/v1/summaries             → List with pagination
GET  /api/v1/search?q=impuestos    → Search summaries
```

---

## 4-Week Timeline (AI-Accelerated)

**Why only 4 weeks?** Claude Code Plus accelerates development 2.5x:
- Auto-generates boilerplate and models
- AI-assisted debugging and testing
- Faster iteration with pair programming
- Automated documentation

### Week 1: Foundation
- **Day 1-2**: Database schema + FastAPI setup (Claude generates)
- **Day 3-4**: Next.js + core components (AI scaffolding)
- **Day 5**: API endpoints + integration
- **Deliverable**: Homepage with hardcoded summary

### Week 2: Core Features
- **Day 1-2**: Web scraper + PDF extraction
- **Day 3-4**: OpenAI integration + summary generation
- **Day 5**: Celery background jobs
- **Deliverable**: First automated summary

### Week 3: Polish & Features
- **Day 1-2**: Search + calendar view
- **Day 3**: Social sharing + mobile
- **Day 4**: Performance + caching
- **Day 5**: E2E testing (Claude writes tests)
- **Deliverable**: Feature-complete MVP

### Week 4: Launch
- **Day 1-2**: Security audit + load testing
- **Day 3**: API docs (auto-generated)
- **Day 4**: Beta testing (10 users)
- **Day 5**: Production deployment + launch
- **Deliverable**: Live public platform

---

## Costs

### One-Time (Development)
- Developer (4 weeks @ $5k): **$20,000**
- Claude Code Plus: **$100**
- Designer (1 week @ $3k): **$3,000**
- DevOps setup: **$2,000**
- Security audit: **$3,000**
- Misc (domain, tools): **$1,500**
- **TOTAL: $29,600**

**Budget savings from AI acceleration:**
- 6 weeks saved × $5k = $30,000 saved
- Faster designer time = $3,000 saved
- **Total saved: $33,000** (52% reduction)

### Monthly (Operations)
- Vercel: $20
- Railway: $20
- Supabase: $25
- Upstash Redis: $10
- Cloudflare R2: $5
- OpenAI API: $50
- **TOTAL: $130/month**

---

## Grant Strategy

### Target: $30,000-35,000 from one grant

**Best Fits:**
1. **Knight Foundation** - Media innovation
2. **Mozilla Foundation** - Trustworthy AI
3. **Google.org** - AI for Social Good
4. **Fast Forward** - Tech nonprofits (smaller grants)

**Pitch:**
"AI-powered daily summaries make Costa Rica's official gazette accessible to 3.5M citizens. Open source. Public API. **$30k to launch in 4 weeks** using AI-accelerated development (Claude Code Plus). $1,500/year to run. 10,000 users in 6 months. Replicable across Latin America."

**Grant Advantage:**
- **52% lower budget** than traditional development ($30k vs $66k)
- **60% faster timeline** (4 weeks vs 10 weeks)
- More fundable for smaller grant programs
- Faster time-to-impact for funders

### Application Materials
- Problem: Complex legal docs exclude citizens
- Solution: GPT-4 daily summaries with AI-accelerated development
- Impact: 10k users, 50+ media citations, 100% open source
- Budget: $30k development + $1.5k/year operations
- Timeline: 4 weeks to launch
- Team: [Your credentials] + Claude Code Plus

---

## Day 1 Setup Checklist

**Create Accounts:**
- [ ] GitHub (code)
- [ ] Vercel (frontend hosting)
- [ ] Railway (backend hosting)
- [ ] Supabase (database)
- [ ] Upstash (Redis)
- [ ] Cloudflare (R2 storage)
- [ ] OpenAI (API key)

**Install Software:**
- [ ] Node.js 20+
- [ ] Python 3.11+
- [ ] **uv** (Python package manager) - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Git
- [ ] VS Code

**Create Project:**
```bash
git clone https://github.com/YOU/gacetachat-v2
cd gacetachat-v2
mkdir frontend backend

# Backend (using uv - super fast!)
cd backend
uv init
uv add fastapi uvicorn sqlalchemy psycopg2-binary pydantic-settings
uv run uvicorn main:app --reload

# Frontend
cd ../frontend
npx create-next-app@latest . --typescript --tailwind --app
npm run dev
```

---

## Success Metrics (Year 1)

- 🎯 10,000 monthly active users
- 🎯 99.5% uptime
- 🎯 <3 second page loads
- 🎯 50+ media citations
- 🎯 10+ API integrations
- 🎯 100% open source

---

## What Happens to Old Docs?

**DELETED:**
- All 60+ files in `/docs/business`, `/docs/architecture`, etc.
- Outdated prototype documentation
- Bloated accountability frameworks
- Complex commercialization plans

**KEPT:**
- This file (IMPLEMENTATION_PLAN.md)
- README.md
- .claudefile (repo reference)

**ARCHIVED:**
- Old docs moved to `/archive` for historical reference

---

## Rules for This Project

1. **No feature creep** - If it's not in the MVP list, it doesn't exist
2. **No premature optimization** - Ship first, optimize later
3. **No complex architecture** - Simple > clever
4. **No bloated docs** - One plan, one truth
5. **Ship in 10 weeks** - Or it doesn't matter

---

## Questions? Start Here

1. Read this document top to bottom (5 minutes)
2. Run Day 1 setup checklist
3. Follow Week 1-2 tasks from timeline
4. Deploy something by end of Week 1

**Don't:**
- Read the 64 other docs
- Add features to MVP
- Over-architect
- Wait for perfect

**Do:**
- Build
- Ship
- Iterate
- Repeat

---

**Last Updated**: 2025-01-15
**Status**: Ready to build
**Bloat Level**: Zero
