# AI-Driven Recruiting Automation Platform

Production-grade multi-agent platform that automates the complete job-hunting workflow.

## What It Does

| Stage | Component | Action |
|-------|-----------|--------|
| 1 | Job Detector | Monitors RSS feeds + LinkedIn for new postings |
| 2 | JD Parser | Extracts skills, role, level, location, company |
| 3 | Rule Engine | Scores jobs against configurable matching rules |
| 4 | Resume Matcher | Maps resume sections to JD requirements |
| 5 | Recruiter Scraper | Finds hiring managers via Apollo + Hunter |
| 6 | Outreach Generator | Writes personalized emails + LinkedIn notes |
| 7 | Telegram Agent | Sends strike packages with one-click actions |
| 8 | Notion Tracker | Syncs application state to Notion database |
| 9 | Apply Engine | Automates or assists with job applications |
| 10 | Mailtrack Monitor | Watches email opens and link clicks |
| 11 | Follow-up Engine | Schedules and sends follow-up messages |
| 12 | Analytics Engine | Tracks funnel metrics and conversion rates |

## Stack

- **Frontend**: Next.js 14 · React 18 · TypeScript · TailwindCSS
- **Backend**: Python FastAPI · AsyncIO · APScheduler
- **Database**: Supabase (PostgreSQL) via SQLAlchemy ORM
- **Integrations**: Telegram · Apollo · Hunter · Gmail · Mailtrack · Notion · LinkedIn

### Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (Optional for containerized dev)
- Supabase project
- API keys for all integrations (see .env.example)

### Using Docker Compose (Recommended)
You can start both the frontend and backend using Docker Compose:
```bash
# First, setup your environment variables
cp .env.example .env
cd frontend
cp .env.local.example .env.local
cd ..

# Build and start the containers
docker-compose up --build
```
The backend will be available at http://localhost:8000 and the frontend at http://localhost:3000.

### Manual Setup (Backend)
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp ../.env.example .env      # fill in your keys
uvicorn main:app --reload --port 8000
```

### Manual Setup (Frontend)
```bash
cd frontend
npm install
cp .env.local.example .env.local   # fill in NEXT_PUBLIC_BACKEND_URL
npm run dev
```

## Project Structure

```
JOBFINDER/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt
│   ├── config/settings.py   # Pydantic settings
│   ├── db/                  # SQLAlchemy session + migrations
│   ├── models/              # ORM models
│   ├── agents/              # All intelligence modules
│   ├── api/routes/          # REST API endpoints
│   └── scheduler/           # APScheduler background tasks
└── frontend/
    ├── src/app/             # Next.js App Router pages
    ├── src/components/      # React components
    └── src/lib/             # API client + types
```

## Documentation
- `rules.md` — execution rules for all agents
- `workflow.md` — phase-by-phase execution plan
- `dependency-map.md` — module dependency graph
- `implementation-status.md` — live build status
- `logs.md` — execution log

---

## Build Summary — Phases 0–5 Complete

### Phase 0 — Documentation

| File | Purpose |
|------|---------|
| `rules.md` | Execution rules for all agents |
| `README.md` | Setup guide + architecture |
| `workflow.md` | Phase-by-phase execution plan |
| `dependency-map.md` | Module + package dependency graph |
| `implementation-status.md` | Live build tracker |
| `logs.md` | Execution audit trail |
| `.env.example` | All 18 required environment variables |

### Phase 1–4 — Backend (Python FastAPI)

- `config/settings.py` — Pydantic BaseSettings for all env vars
- `db/session.py` — Async SQLAlchemy engine + session factory
- `models/` — 4 ORM models: Job, Application, Recruiter, OutreachMessage
- **12 Agent Modules:**

| Agent | Capability |
|-------|-----------|
| `job_detector` | RSS feed polling for new job postings |
| `jd_parser` | Extracts skills, level, salary from job descriptions |
| `rule_engine` | Configurable scoring against your skill profile |
| `resume_matcher` | Maps resume sections to JD requirements |
| `recruiter_scraper` | Finds hiring managers via Apollo + Hunter APIs |
| `outreach_generator` | Personalized emails via Claude Haiku or templates |
| `telegram_agent` | Sends strike packages with one-click action links |
| `notion_tracker` | Syncs application state to Notion database |
| `apply_engine` | Sends application emails via Gmail API |
| `mailtrack_monitor` | Detects email opens and link clicks |
| `followup_engine` | Schedules follow-ups at 3 / 7 / 14 days |
| `analytics_engine` | Funnel metrics, open rates, response rates |

- 6 API route files under `/api/v1/` — all responses use `{ success, data, error }` envelope
- `scheduler/tasks.py` — APScheduler background tasks (job detection, follow-ups, Mailtrack checks)
- `main.py` — FastAPI app with CORS middleware + lifespan startup

### Phase 5 — Frontend (Next.js 14)

- `lib/types.ts` + `lib/api.ts` — fully typed API client
- 5 pages:

| Page | Features |
|------|---------|
| Dashboard | Funnel stats, matched jobs, open/response rates, detect + follow-up buttons |
| Jobs | Search, match filter, inline recruiter scraping + outreach generation |
| Applications | Status Kanban, timeline view, one-click status updates |
| Analytics | Visual funnel bars, top matched companies, conversion metrics |
| Settings | Skill tag editors, blocked company/keyword lists, RSS feed manager |

### Phases 6–7 — Remaining

- [ ] Unit tests + API integration tests
- [x] Docker Compose for local dev
- [ ] Rate limiting middleware
- [x] CI/CD pipeline
