"""
APScheduler background task definitions.
All tasks are async and interact with the database via dedicated sessions.
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config.settings import get_settings
from db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def run_job_detection() -> None:
    logger.info("Scheduler: running job detection")
    async with AsyncSessionLocal() as db:
        from agents.job_detector import JobDetector, DEFAULT_RSS_FEEDS
        from agents.jd_parser import JDParser
        from agents.rule_engine import RuleEngine
        from models.settings import SearchProfile, RssFeed
        from sqlalchemy import select
        
        feeds_res = await db.execute(select(RssFeed).where(RssFeed.is_active == True))
        active_feeds = [f.url for f in feeds_res.scalars().all()] or DEFAULT_RSS_FEEDS

        profile_res = await db.execute(select(SearchProfile).where(SearchProfile.is_active == True))
        profile = profile_res.scalars().first()
        active_rules = None
        if profile:
            active_rules = {
                "required_skills": profile.required_skills,
                "preferred_skills": profile.preferred_skills,
                "blocked_companies": profile.blocked_companies,
                "blocked_keywords": profile.blocked_keywords,
                "min_match_score": profile.min_match_score,
                "target_levels": profile.target_levels,
                "target_employment": profile.target_employment,
            }
        
        detector = JobDetector(db, rss_feeds=active_feeds)
        parser = JDParser()
        engine = RuleEngine(rules=active_rules)
        jobs = await detector.run()
        
        dynamic_skills = []
        if active_rules:
            dynamic_skills.extend(active_rules.get("required_skills", []))
            dynamic_skills.extend(active_rules.get("preferred_skills", []))

        for job in jobs:
            parsed = parser.parse(job.description or "", extra_skills=dynamic_skills)
            result = engine.evaluate(
                title=job.title,
                company=job.company,
                description=job.description or "",
                required_skills=parsed.required_skills,
                preferred_skills=parsed.preferred_skills,
                experience_level=parsed.experience_level,
                employment_type=parsed.employment_type,
            )
            job.required_skills = parsed.required_skills
            job.preferred_skills = parsed.preferred_skills
            job.experience_level = parsed.experience_level
            job.employment_type = parsed.employment_type
            job.salary_range = parsed.salary_range
            job.match_score = result.score
            job.is_match = result.is_match
            job.match_reasons = result.reasons
        await db.commit()
        if jobs:
            await _send_match_notifications(jobs)


async def _send_match_notifications(jobs) -> None:
    from agents.resume_matcher import ResumeMatcher
    from agents.recruiter_scraper import RecruiterScraper
    from agents.outreach_generator import OutreachGenerator
    from agents.telegram_agent import TelegramAgent
    matcher = ResumeMatcher()
    scraper = RecruiterScraper()
    gen = OutreachGenerator()
    telegram = TelegramAgent()

    for job in jobs:
        if not job.is_match:
            continue
        try:
            resume_match = matcher.match(
                job_title=job.title,
                company=job.company,
                required_skills=job.required_skills or [],
                preferred_skills=job.preferred_skills or [],
                experience_level=job.experience_level or "mid",
            )
            recruiters = await scraper.find_recruiters(job.company, job.title)
            recruiter = recruiters[0] if recruiters else {}
            outreach = await gen.generate(
                job_title=job.title,
                company=job.company,
                recruiter_name=recruiter.get("name"),
                cover_angle=resume_match.cover_angle,
                matched_skills=resume_match.matched_skills,
                experience_years=5,
                highlight="scalable distributed systems",
                my_name="Your Name",
            )
            await telegram.send_strike_package(
                title=job.title,
                company=job.company,
                location=job.location or "",
                employment_type=job.employment_type or "",
                url=job.url,
                score=job.match_score or 0,
                matched_skills=resume_match.matched_skills,
                missing_skills=resume_match.missing_skills,
                recruiter_name=recruiter.get("name"),
                recruiter_email=recruiter.get("email"),
                email_subject=outreach["email_subject"],
                cover_angle=resume_match.cover_angle,
                reasons=job.match_reasons or [],
            )
        except Exception as e:
            logger.error("Notification failed for job %s: %s", job.id, e)


async def run_followup_check() -> None:
    logger.info("Scheduler: running follow-up check")
    async with AsyncSessionLocal() as db:
        from agents.followup_engine import FollowupEngine
        engine = FollowupEngine(db)
        await engine.run()


async def run_mailtrack_check() -> None:
    logger.info("Scheduler: running Mailtrack check")
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        from models.outreach import OutreachMessage
        from agents.mailtrack_monitor import MailtrackMonitor
        monitor = MailtrackMonitor()
        result = await db.execute(
            select(OutreachMessage).where(
                OutreachMessage.sent == True,
                OutreachMessage.opened == False,
                OutreachMessage.gmail_message_id.isnot(None),
            )
        )
        messages = result.scalars().all()
        msg_ids = [m.gmail_message_id for m in messages if m.gmail_message_id]
        if not msg_ids:
            return
        opens = await monitor.check_opens(msg_ids)
        for msg in messages:
            if msg.gmail_message_id and opens.get(msg.gmail_message_id, {}).get("opened"):
                msg.opened = True
                msg.opened_at = opens[msg.gmail_message_id]["opened_at"]
        await db.commit()


def create_scheduler() -> AsyncIOScheduler:
    settings = get_settings()
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        run_job_detection,
        trigger=IntervalTrigger(seconds=settings.job_detection_interval),
        id="job_detection",
        name="Job Detection",
        replace_existing=True,
    )
    scheduler.add_job(
        run_followup_check,
        trigger=IntervalTrigger(seconds=settings.followup_check_interval),
        id="followup_check",
        name="Follow-up Check",
        replace_existing=True,
    )
    scheduler.add_job(
        run_mailtrack_check,
        trigger=IntervalTrigger(seconds=settings.mailtrack_check_interval),
        id="mailtrack_check",
        name="Mailtrack Check",
        replace_existing=True,
    )
    return scheduler
