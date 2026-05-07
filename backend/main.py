import sys
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings
from db.session import init_db
from scheduler.tasks import create_scheduler
from api.routes import jobs, applications, recruiters, outreach, analytics, settings as settings_router

# Fix asyncio DNS resolution on Windows (getaddrinfo fails with IocpProactor)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

settings = get_settings()
scheduler = create_scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="AI Recruiting Automation Platform",
    version="1.0.0",
    description="Multi-agent platform for automated job hunting",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")
app.include_router(recruiters.router, prefix="/api/v1")
app.include_router(outreach.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(settings_router.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0", "env": settings.app_env}
