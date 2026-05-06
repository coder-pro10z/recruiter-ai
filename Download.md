# PLAN.md

# AI-Driven Recruiting Automation Platform
Lean MVP + Production-Ready Multi-Agent Execution Plan

## 1. PROJECT OVERVIEW

This project is a production-grade AI-assisted recruiting automation platform designed to accelerate and optimize the complete job-hunting workflow.

The primary goal of the platform is to:
- detect jobs instantly,
- classify jobs dynamically,
- map resumes automatically,
- discover recruiters,
- generate personalized outreach,
- send Telegram strike notifications,
- track applications,
- automate follow-ups,
- and significantly reduce manual effort during job applications.

The platform must prioritize:
- speed,
- simplicity,
- maintainability,
- modularity,
- configurability,
- rapid deployment,
- and real-world usability.

The MVP architecture must remain lightweight and deployment-friendly while supporting future scalability.

## 2. EXECUTION PRECHECK RULE

Before executing ANY task, ALL agents MUST first read and comply with:
1. rules.md
2. README.md
3. workflow.md
4. dependency-map.md
5. implementation-status.md
6. current phase documents
7. logs.md

Agents MUST:
- follow execution order strictly,
- execute ONLY the assigned phase,
- update all required documentation,
- validate dependencies,

## 3. CORE SYSTEM OBJECTIVES

The platform MUST support:
- instant job detection,
- dynamic rule matching,
- resume mapping,
- recruiter scraping,
- outreach generation,
- Telegram strike packages,
- Notion tracking,
- follow-up automation,
- Mailtrack integration,
- frontend-driven configuration,
- async processing,
- and lightweight deployment.

## 4. HIGH-LEVEL SYSTEM FLOW

JOB DETECTION
→ JD PARSER
→ RULE ENGINE
→ RESUME MATCHING
→ RECRUITER SCRAPER
→ OUTREACH GENERATION
→ TELEGRAM STRIKE PACKAGE
→ NOTION TRACKING
→ APPLY ENGINE
→ MAILTRACK MONITORING
→ FOLLOW-UP ENGINE
→ ANALYTICS ENGINE

## 5. MULTI-AGENT SYSTEM

### 5.1 SENIOR SOFTWARE ARCHITECT

Purpose:
Design scalable lightweight architecture.

### 5.2 SENIOR SOFTWARE DEVELOPER

Purpose:
Implement all platform modules.

### 5.3 QUALITY ANALYST

Purpose:
Validate workflows and implementation quality.

### 5.4 TASK / DOCUMENT MASTER

Purpose:
Control execution sequencing and documentation synchronization.

### 5.5 WORKFLOW ANALYST

Purpose:
Optimize operational workflows and identify bottlenecks.

## 6. LEAN MVP STACK

Frontend:
- Next.js
- React
- TypeScript
- TailwindCSS

Backend:
- Python FastAPI
- AsyncIO
- APScheduler

Database:
- Supabase PostgreSQL

ORM:
- SQLAlchemy

Integrations:
- Telegram Bot API
- Apollo
- Hunter
- Gmail APIs
- Mailtrack
- Notion
- LinkedIn Search
- RSS feeds

## 7. REQUIRED ENVIRONMENT VARIABLES

```env
# DATABASE
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=

# TELEGRAM
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# APOLLO
APOLLO_API_KEY=

# HUNTER
HUNTER_API_KEY=

# GMAIL
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_REFRESH_TOKEN=

# NOTION
NOTION_API_KEY=
NOTION_DATABASE_ID=

# APPLICATION
APP_ENV=
APP_PORT=
FRONTEND_URL=
BACKEND_URL=
```

## 8. SUCCESS CRITERIA

The platform is considered successful when it can:
- detect jobs rapidly,
- dynamically match resumes,
- scrape recruiters,
- generate outreach,
- send Telegram strike notifications,
- automate tracking,
- automate follow-ups,
- and significantly accelerate the real-world job-hunting workflow.
