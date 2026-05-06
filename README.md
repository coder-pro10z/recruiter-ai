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

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Supabase project
- API keys for all integrations (see .env.example)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp ../.env.example .env      # fill in your keys
uvicorn main:app --reload --port 8000
```

### Frontend
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
