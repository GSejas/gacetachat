# GacetaChat 2.0 🇨🇷

> Daily AI summaries of Costa Rica's official gazette. Simple. Fast. Open source.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Planning-yellow.svg)](IMPLEMENTATION_PLAN.md)

---

## What is this?

**The Problem:** Costa Rica publishes laws and regulations daily in La Gaceta, but it's 50-200 pages of dense legal text. Nobody reads it.

**Our Solution:** AI generates a 5-bullet summary every morning. Takes 30 seconds to read. Everyone understands what changed.

**Example:**
```
La Gaceta - 15 de enero, 2025

⚖️ Nueva ley de impuestos: Tasa de IVA aumenta del 13% al 13.5%
🏥 Reforma sanitaria: Nuevos requisitos para permisos de alimentos
🎓 Educación: Cambios en calendario escolar para 2025
💰 Presupuesto: Aumenta inversión en infraestructura vial
🌳 Ambiente: Nuevas regulaciones para protección de bosques
```

That's it. No chat. No login. No complexity.

---

## Status: Complete Rewrite

This is an **unreleased prototype**. We're doing a complete rewrite with modern tech:

- ❌ **Old Stack:** Streamlit + SQLite + messy prototype
- ✅ **New Stack:** Next.js + FastAPI + PostgreSQL + Vercel
- 🎯 **Goal:** Launch MVP in 4 weeks (AI-accelerated)
- 💰 **Funding:** Seeking $30k grant (52% cheaper with Claude Code Plus)

---

## Quick Links

📋 **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** ← **START HERE**
- Complete 10-week plan
- Tech stack decisions
- Budget breakdown
- Day 1 setup guide

💰 **[docs/GRANT_STRATEGY.md](docs/GRANT_STRATEGY.md)** ← For grant applications
- Funding strategy
- Target grant sources
- Sample applications
- $70k budget justification

🏗️ **[docs/ARCHITECTURAL_OVERHAUL.md](docs/ARCHITECTURAL_OVERHAUL.md)** ← Deep technical dive
- Complete system architecture
- Database schema
- API design
- Security considerations

🚀 **[docs/QUICK_START_GUIDE.md](docs/QUICK_START_GUIDE.md)** ← Step-by-step setup
- Week-by-week instructions
- Code examples
- Deployment guides

---

## Tech Stack (2.0 Rewrite)

### Frontend
- **Next.js 14** - React framework with App Router
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Accessible components
- **Vercel** - Hosting + CDN

### Backend
- **FastAPI** - Python REST API
- **PostgreSQL** - Database (Supabase)
- **Redis** - Caching (Upstash)
- **Celery** - Background jobs
- **Railway** - Hosting

### AI & Storage
- **OpenAI GPT-4o** - Summary generation
- **Cloudflare R2** - PDF storage

---

## MVP Features (10 Weeks)

### What We're Building
1. **Daily Summary** - Homepage shows today's gazette in 5 bullet points
2. **Archive** - Calendar to browse past 90 days
3. **Search** - Find summaries by keyword
4. **Public API** - Free REST API for developers

### What We're NOT Building (Yet)
- User accounts
- Comments/community
- Email notifications
- Twitter bot
- Chat interface
- Analytics
- Any complexity

---

## Budget

### Development (One-Time) - AI-Accelerated
- Developer (4 weeks): $20,000
- Claude Code Plus: $100
- Designer (1 week): $3,000
- DevOps: $2,000
- Security: $3,000
- Misc: $1,500
- **Total: $29,600**

**Savings from AI:** $33,000 (52% cheaper than traditional development)

### Operations (Monthly)
- Cloud hosting: $80
- OpenAI API: $50
- **Total: $130/month**

**Yearly:** ~$1,500 to run forever.

---

## See the Demo

### 🌐 Live Demo (Streamlit Cloud)
**Coming soon!** Deploy to Streamlit Cloud with one click.

### 💻 Run Locally

**With uv (recommended):**
```bash
# Install uv (super fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the demo (uv handles everything)
uv run demo_simple.py
```

**Or with pip:**
```bash
pip install -r requirements.txt
streamlit run demo_simple.py
```

### 📦 Deploy Your Own

**Streamlit Cloud (Free):**
1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `demo_simple.py`
5. Deploy!

**This is just a static mockup** - shows the UI concept, not the real functionality.

**Note:** V1 prototype code has been archived to `archive/v1/`. Read **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** for the v2.0 plan.

---

## Contributing

We're in planning phase. Here's how to help:

1. **Grant Writing** - Help apply for funding
2. **Design** - UI/UX mockups for the new version
3. **Development** - Once funded, we'll need React + Python devs
4. **Feedback** - Is this useful? Tell us why/why not

**Don't:**
- Add features to the old prototype
- Send PRs for the current code
- Build on the existing architecture

---

## Roadmap

### Phase 0: Planning (Now)
- [x] Complete architecture design
- [x] Grant strategy
- [x] Budget planning
- [ ] Apply for grants

### Phase 1: Development (4 Weeks - AI-Accelerated)
- [ ] Week 1: Backend API + database
- [ ] Week 2: Scraper + AI summarization
- [ ] Week 3: Frontend UI + features
- [ ] Week 4: Testing + public launch

### Phase 2: Growth (Months 2-6)
- [ ] Reach 10,000 monthly users
- [ ] 50+ media integrations
- [ ] Open source community
- [ ] Replication toolkit for other countries

---

## License

MIT License - See [LICENSE](LICENSE) file.

This is open-source civic infrastructure. Free forever.

---

## Contact

- **Grant Inquiries:** [Your email]
- **Partnership Opportunities:** [Your email]
- **Technical Questions:** [GitHub Issues](issues)

---

## Archive

### Documentation Archive
Old documentation (64 files) moved to `/docs/archive/`:
- Business plans → Archived (over-complicated)
- Commercialization → Archived (grant-funded, not commercial)
- Accountability framework → Archived (scope creep)
- Old architecture docs → Archived (complete rewrite)

### V1 Prototype Archive
Old prototype code moved to `/archive/v1/`:
- Streamlit multi-page app (app.py, streamlit_app.py, etc.)
- FastAPI backend (fastapp.py, crud.py, etc.)
- PDF processing (pdf_processor.py, faiss_helper.py)
- Database models (models.py, db.py)
- Twitter integration (twitter.py)
- All V1 dependencies and configs

**One truth:** [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)

---

**Status:** Planning → Funding → Building → Launching
**Timeline:** 4 weeks to launch (AI-accelerated with Claude Code Plus)
**Cost:** $30k to build, $1.5k/year to run
**Impact:** Democracy for 3.5M Costa Ricans
**Efficiency:** 52% cheaper, 60% faster than traditional development

Made with ❤️ for democratic transparency 🇨🇷
