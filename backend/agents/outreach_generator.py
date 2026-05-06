"""
Outreach Generator — writes personalized cold emails and LinkedIn notes.
Uses Claude API if key is available; falls back to template-based generation.
"""
import logging
from config.settings import get_settings

logger = logging.getLogger(__name__)

EMAIL_TEMPLATE = """\
Subject: {subject}

Hi {recruiter_name},

I came across the {job_title} role at {company} and wanted to reach out directly.

{cover_angle}

I bring {experience_years}+ years of experience with {top_skills}, having built {highlight} at scale.

I'd love to learn more about the team and the role. Would you be open to a brief 20-minute call?

Best,
{my_name}
"""

LINKEDIN_TEMPLATE = """\
Hi {recruiter_name}, I noticed the {job_title} opening at {company}. \
I have {experience_years}+ years with {top_skills} and would love to connect to learn more. \
Happy to share my resume if helpful!
"""


class OutreachGenerator:
    def __init__(self):
        self.settings = get_settings()

    async def generate(
        self,
        job_title: str,
        company: str,
        recruiter_name: str | None,
        cover_angle: str,
        matched_skills: list[str],
        experience_years: int,
        highlight: str,
        my_name: str,
    ) -> dict[str, str]:
        name = recruiter_name or "Hiring Team"
        top_skills = ", ".join(matched_skills[:4]) if matched_skills else "software engineering"
        subject = f"Interest in {job_title} at {company} — {my_name}"

        if self.settings.anthropic_api_key:
            return await self._generate_with_claude(
                job_title, company, name, cover_angle, top_skills, experience_years, highlight, my_name, subject
            )

        email_body = EMAIL_TEMPLATE.format(
            subject=subject,
            recruiter_name=name,
            job_title=job_title,
            company=company,
            cover_angle=cover_angle,
            experience_years=experience_years,
            top_skills=top_skills,
            highlight=highlight,
            my_name=my_name,
        )
        linkedin_note = LINKEDIN_TEMPLATE.format(
            recruiter_name=name,
            job_title=job_title,
            company=company,
            experience_years=experience_years,
            top_skills=top_skills,
        )
        return {"email_subject": subject, "email_body": email_body, "linkedin_note": linkedin_note}

    async def _generate_with_claude(
        self, job_title, company, recruiter_name, cover_angle,
        top_skills, experience_years, highlight, my_name, subject
    ) -> dict[str, str]:
        try:
            import anthropic
            client = anthropic.AsyncAnthropic(api_key=self.settings.anthropic_api_key)
            prompt = (
                f"Write a concise, personalized cold email for a job application.\n"
                f"Role: {job_title} at {company}\n"
                f"Recipient: {recruiter_name}\n"
                f"Applicant: {my_name}, {experience_years}+ years experience with {top_skills}\n"
                f"Angle: {cover_angle}\n"
                f"Notable: {highlight}\n\n"
                f"Format: subject line on first line, blank line, then email body. Keep under 150 words."
            )
            message = await client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = message.content[0].text
            lines = raw.split("\n", 2)
            ai_subject = lines[0].replace("Subject:", "").strip() if lines else subject
            ai_body = "\n".join(lines[2:]).strip() if len(lines) > 2 else raw

            linkedin_prompt = (
                f"Write a 2-sentence LinkedIn connection note for {my_name} applying for {job_title} at {company}. "
                f"Skills: {top_skills}. Under 300 characters."
            )
            li_message = await client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=100,
                messages=[{"role": "user", "content": linkedin_prompt}],
            )
            return {
                "email_subject": ai_subject,
                "email_body": ai_body,
                "linkedin_note": li_message.content[0].text.strip(),
            }
        except Exception as e:
            logger.warning("Claude generation failed, falling back to template: %s", e)
            return await self.generate(
                job_title, company, recruiter_name, cover_angle,
                [], experience_years, highlight, my_name
            )
