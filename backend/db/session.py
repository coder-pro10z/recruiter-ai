import sys
import asyncio
import ssl

# MUST be set before any asyncio event loop is created on Windows.
# uvicorn's --reload mode spawns a subprocess; this runs first in that subprocess.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config.settings import get_settings


class Base(DeclarativeBase):
    pass


def _build_engine():
    # Clear lru_cache so a fresh .env is always read after a reload
    get_settings.cache_clear()
    settings = get_settings()
    # Strip any query params; asyncpg SSL config is passed via connect_args
    url = settings.database_url.split("?")[0]

    # Supabase PgBouncer (transaction pooler) uses a self-signed certificate.
    # We still encrypt the connection but skip certificate chain verification.
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    return create_async_engine(
        url,
        echo=settings.app_env == "development",
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        # ssl_ctx → encrypted but no cert verification (required for PgBouncer)
        # statement_cache_size=0 → PgBouncer doesn't support prepared statements
        connect_args={"ssl": ssl_ctx, "statement_cache_size": 0},
    )


engine = _build_engine()
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
