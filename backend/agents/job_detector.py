"""
Job Detector — monitors RSS feeds and LinkedIn for new job postings.
"""
import feedparser
import httpx
import logging
from datetime import datetime
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.job import Job

logger = logging.getLogger(__name__)

DEFAULT_RSS_FEEDS = [
    "https://www.linkedin.com/jobs/search/?keywords=software+engineer&f_TPR=r86400&format=rss",
    "https://feeds.feedburner.com/GithubBlog",
    "https://stackoverflow.com/jobs/feed",
    "https://remoteok.com/remote-jobs.rss",
    "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
]


class JobDetector:
    def __init__(self, db: AsyncSession, rss_feeds: list[str] | None = None):
        self.db = db
        self.rss_feeds = rss_feeds or DEFAULT_RSS_FEEDS

    async def run(self) -> list[Job]:
        detected: list[Job] = []
        for feed_url in self.rss_feeds:
            try:
                jobs = await self._parse_feed(feed_url)
                for job_data in jobs:
                    job = await self._save_if_new(job_data)
                    if job:
                        detected.append(job)
            except Exception as e:
                logger.error("Feed %s failed: %s", feed_url, e)
        logger.info("Detected %d new jobs", len(detected))
        return detected

    async def _parse_feed(self, url: str) -> list[dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        }
        async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
        feed = feedparser.parse(response.text)
        jobs = []
        for entry in feed.entries[:20]:
            jobs.append({
                "title": entry.get("title", ""),
                "company": entry.get("author", entry.get("company", "Unknown")),
                "location": entry.get("location", ""),
                "url": entry.get("link", ""),
                "source": "rss",
                "description": entry.get("summary", ""),
                "detected_at": datetime.utcnow(),
            })
        return jobs

    async def _save_if_new(self, data: dict[str, Any]) -> Job | None:
        if not data.get("url"):
            return None
        existing = await self.db.execute(select(Job).where(Job.url == data["url"]))
        if existing.scalar_one_or_none():
            return None
        job = Job(**data)
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job
