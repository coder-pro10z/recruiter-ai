"""
Resume Matcher — maps resume sections to JD requirements and generates a fit summary.
"""
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# In production: load from a resume file (PDF/DOCX) or Supabase storage
DEFAULT_RESUME = {
    "name": "Your Name",
    "title": "Senior Software Engineer",
    "skills": ["python", "fastapi", "postgresql", "react", "typescript", "docker", "aws"],
    "experience_years": 5,
    "experience": [
        {"company": "Company A", "role": "Senior SWE", "duration": "3 years", "skills": ["python", "fastapi", "postgresql"]},
        {"company": "Company B", "role": "SWE", "duration": "2 years", "skills": ["react", "typescript", "aws"]},
    ],
    "education": [{"degree": "BS Computer Science", "school": "State University"}],
    "highlights": ["Built distributed systems at scale", "Led teams of 5+ engineers"],
}


@dataclass
class ResumeMatch:
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    relevant_experience: list[dict] = field(default_factory=list)
    fit_summary: str = ""
    cover_angle: str = ""


class ResumeMatcher:
    def __init__(self, resume: dict | None = None):
        self.resume = resume or DEFAULT_RESUME

    def match(
        self,
        job_title: str,
        company: str,
        required_skills: list[str],
        preferred_skills: list[str],
        experience_level: str,
    ) -> ResumeMatch:
        my_skills = set(self.resume.get("skills", []))
        all_jd_skills = set(required_skills + preferred_skills)

        matched = list(my_skills & all_jd_skills)
        missing = [s for s in required_skills if s not in my_skills]
        relevant_exp = [
            exp for exp in self.resume.get("experience", [])
            if any(s in exp.get("skills", []) for s in required_skills)
        ]

        fit_summary = self._build_fit_summary(job_title, company, matched, missing, relevant_exp)
        cover_angle = self._build_cover_angle(job_title, company, matched, relevant_exp)

        return ResumeMatch(
            matched_skills=matched,
            missing_skills=missing,
            relevant_experience=relevant_exp,
            fit_summary=fit_summary,
            cover_angle=cover_angle,
        )

    def _build_fit_summary(
        self, title: str, company: str, matched: list, missing: list, exp: list
    ) -> str:
        match_pct = round(len(matched) / max(len(matched) + len(missing), 1) * 100)
        exp_str = f" from roles at {', '.join(e['company'] for e in exp[:2])}" if exp else ""
        return (
            f"{match_pct}% skill overlap with {title} at {company}. "
            f"Matched: {', '.join(matched[:5]) or 'none'}. "
            f"Gaps: {', '.join(missing[:3]) or 'none'}. "
            f"Relevant experience{exp_str}."
        )

    def _build_cover_angle(self, title: str, company: str, matched: list, exp: list) -> str:
        top_match = matched[0] if matched else "engineering"
        exp_ref = exp[0]["company"] if exp else "a previous role"
        return (
            f"Angle: Highlight {top_match} expertise developed at {exp_ref} "
            f"and connect it to the {title} role requirements at {company}."
        )
