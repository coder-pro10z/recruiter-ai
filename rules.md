# RULES.md — Execution Rules for All Agents

## 1. MANDATORY PRECHECK
Before executing ANY task, ALL agents MUST read:
1. rules.md (this file)
2. README.md
3. workflow.md
4. dependency-map.md
5. implementation-status.md
6. Current phase document
7. logs.md

## 2. EXECUTION DISCIPLINE
- Execute ONLY the assigned phase — no scope creep
- Follow execution order strictly per workflow.md
- Mark tasks complete in implementation-status.md immediately after completion
- Log every action in logs.md with timestamp, agent, action, and outcome

## 3. CODE STANDARDS
- Python: PEP8, async/await for all I/O, type hints everywhere
- TypeScript: strict mode, no `any`, explicit return types
- No hardcoded credentials — use environment variables only
- All secrets via .env (never committed)
- Fail fast with descriptive error messages

## 4. DOCUMENTATION SYNC
- Every file created or modified must be logged in logs.md
- implementation-status.md must reflect true current state
- dependency-map.md must be updated when new dependencies are added

## 5. DEPENDENCY RULES
- Backend: Python 3.11+, FastAPI, AsyncIO, APScheduler, SQLAlchemy, Supabase
- Frontend: Next.js 14+, React 18+, TypeScript 5+, TailwindCSS 3+
- No unused packages — every dependency must have a declared purpose

## 6. API CONTRACTS
- All backend routes: RESTful, versioned under /api/v1/
- Response format: { success: bool, data: T | null, error: string | null }
- All async endpoints — no blocking calls in request handlers

## 7. TESTING REQUIREMENTS
- Each agent module must have a test scaffold
- Integration tests for all API routes
- No untested modules shipped to production

## 8. SECURITY
- CORS restricted to FRONTEND_URL
- All input validated with Pydantic
- No SQL injection — use ORM only
- Rate limiting on all external API calls
