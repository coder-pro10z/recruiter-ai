"""
start.py — Windows-compatible uvicorn launcher.
Sets WindowsSelectorEventLoopPolicy before uvicorn starts so that
asyncio DNS resolution (getaddrinfo) works correctly on Windows.
"""
import sys
import asyncio

if sys.platform == "win32":
    # Fix: asyncio on Windows with IocpProactor fails getaddrinfo for some DNS entries.
    # WindowsSelectorEventLoopPolicy uses the older selector-based loop which works correctly.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
