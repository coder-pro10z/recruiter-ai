# DEPENDENCY-MAP.md — Module Dependency Graph

## Data Flow Dependencies

```
job_detector
    └── jd_parser
            └── rule_engine
                    └── resume_matcher
                            └── recruiter_scraper
                                    └── outreach_generator
                                            ├── telegram_agent
                                            └── notion_tracker (parallel)
                                                    └── apply_engine
                                                            └── mailtrack_monitor
                                                                    └── followup_engine
                                                                            └── analytics_engine
```

## Shared Infrastructure Dependencies

```
ALL agents
    ├── config/settings.py     (env config)
    ├── db/session.py          (database access)
    └── models/                (ORM models)
```

## External API Dependencies

| Module | External APIs | Required Keys |
|--------|--------------|---------------|
| job_detector | LinkedIn Search, RSS feeds | None (scraping) |
| recruiter_scraper | Apollo, Hunter | APOLLO_API_KEY, HUNTER_API_KEY |
| outreach_generator | Claude/OpenAI | ANTHROPIC_API_KEY (optional) |
| telegram_agent | Telegram Bot API | TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID |
| notion_tracker | Notion API | NOTION_API_KEY, NOTION_DATABASE_ID |
| apply_engine | Gmail API | GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN |
| mailtrack_monitor | Mailtrack, Gmail | (Gmail creds reused) |
| followup_engine | Gmail API | (Gmail creds reused) |

## Python Package Dependencies

| Package | Used By | Purpose |
|---------|---------|---------|
| fastapi | main, api/* | HTTP framework |
| uvicorn | main | ASGI server |
| pydantic | config, models, api | Validation + settings |
| sqlalchemy | db, models | ORM |
| asyncpg | db | Async PostgreSQL driver |
| httpx | all agents | Async HTTP client |
| apscheduler | scheduler | Background task scheduling |
| python-telegram-bot | telegram_agent | Telegram Bot API |
| feedparser | job_detector | RSS feed parsing |
| beautifulsoup4 | job_detector, recruiter_scraper | HTML scraping |
| notion-client | notion_tracker | Notion API SDK |
| google-auth | apply_engine | Gmail OAuth |
| google-api-python-client | apply_engine, mailtrack | Gmail API |
| python-dotenv | config | .env loading |

## Frontend Package Dependencies

| Package | Used By | Purpose |
|---------|---------|---------|
| next | app | Framework |
| react | all | UI library |
| typescript | all | Type safety |
| tailwindcss | all | Styling |
| @tanstack/react-query | pages | Server state management |
| axios | lib/api | HTTP client |
| lucide-react | components | Icons |
| date-fns | components | Date formatting |
