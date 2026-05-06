# WORKFLOW.md — Phase Execution Plan

## Execution Model
Each phase is atomic. Complete and validate before moving to the next.
Update implementation-status.md and logs.md after every phase.

---

## PHASE 0 — Foundation & Documentation
**Owner**: Task/Document Master  
**Status**: IN PROGRESS

Tasks:
- [x] Create rules.md
- [x] Create README.md
- [x] Create workflow.md
- [x] Create dependency-map.md
- [x] Create implementation-status.md
- [x] Create logs.md
- [x] Create .env.example
- [ ] Initialize git repository

---

## PHASE 1 — Backend Core Infrastructure
**Owner**: Senior Software Developer  
**Status**: IN PROGRESS

Tasks:
- [x] Create backend/ directory structure
- [x] requirements.txt with all dependencies
- [x] config/settings.py (Pydantic BaseSettings)
- [x] db/session.py (SQLAlchemy async engine)
- [x] models/ (Job, Application, Recruiter, OutreachMessage)
- [x] main.py (FastAPI app with CORS, health check)

---

## PHASE 2 — Agent Modules
**Owner**: Senior Software Developer  
**Status**: PENDING

Tasks:
- [ ] agents/job_detector.py
- [ ] agents/jd_parser.py
- [ ] agents/rule_engine.py
- [ ] agents/resume_matcher.py
- [ ] agents/recruiter_scraper.py
- [ ] agents/outreach_generator.py
- [ ] agents/telegram_agent.py
- [ ] agents/notion_tracker.py
- [ ] agents/apply_engine.py
- [ ] agents/mailtrack_monitor.py
- [ ] agents/followup_engine.py
- [ ] agents/analytics_engine.py

---

## PHASE 3 — API Routes
**Owner**: Senior Software Developer  
**Status**: PENDING

Tasks:
- [ ] api/routes/jobs.py
- [ ] api/routes/applications.py
- [ ] api/routes/recruiters.py
- [ ] api/routes/outreach.py
- [ ] api/routes/analytics.py
- [ ] api/routes/settings.py

---

## PHASE 4 — Scheduler & Background Tasks
**Owner**: Senior Software Developer  
**Status**: PENDING

Tasks:
- [ ] scheduler/tasks.py (APScheduler job definitions)
- [ ] Integrate scheduler with FastAPI lifespan

---

## PHASE 5 — Frontend
**Owner**: Senior Software Developer  
**Status**: IN PROGRESS

Tasks:
- [x] Next.js 14 app scaffold
- [x] TailwindCSS configuration
- [x] lib/api.ts (typed API client)
- [x] lib/types.ts (shared TypeScript types)
- [x] Dashboard page
- [x] Jobs page
- [x] Applications page
- [x] Settings page
- [ ] Components: JobCard, ApplicationRow, RecruiterCard
- [ ] Telegram strike preview component

---

## PHASE 6 — Integration Testing
**Owner**: Quality Analyst  
**Status**: PENDING

Tasks:
- [ ] Test job detection end-to-end
- [ ] Test Telegram notification delivery
- [ ] Test Notion sync
- [ ] Test email open tracking
- [ ] Test follow-up scheduling

---

## PHASE 7 — Production Hardening
**Owner**: Senior Software Architect  
**Status**: PENDING

Tasks:
- [ ] Rate limiting middleware
- [ ] Error monitoring (Sentry or equivalent)
- [ ] Docker Compose for local dev
- [ ] CI/CD pipeline definition
- [ ] Environment validation on startup
