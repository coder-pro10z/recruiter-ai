"""
JD Parser — extracts structured data from raw job descriptions.
"""
import re
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

SKILL_KEYWORDS = [
    "python", "javascript", "typescript", "java", "go", "rust", "c++", "c#",
    "react", "next.js", "vue", "angular", "node.js", "fastapi", "django", "flask",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "docker", "kubernetes", "aws", "gcp", "azure", "terraform",
    "machine learning", "deep learning", "pytorch", "tensorflow", "llm",
    "sql", "graphql", "rest", "grpc", "kafka", "rabbitmq",
    "git", "ci/cd", "agile", "scrum",
]

LEVEL_PATTERNS = {
    "intern": r"\b(intern|internship)\b",
    "junior": r"\b(junior|jr\.?|entry.?level|0.?2\s*years?)\b",
    "mid": r"\b(mid.?level|intermediate|2.?5\s*years?)\b",
    "senior": r"\b(senior|sr\.?|5\+?\s*years?)\b",
    "staff": r"\b(staff|principal|6\+?\s*years?)\b",
    "manager": r"\b(manager|lead|director|head of)\b",
}

EMPLOYMENT_PATTERNS = {
    "full-time": r"\b(full.?time|permanent)\b",
    "part-time": r"\b(part.?time)\b",
    "contract": r"\b(contract|freelance|consultant)\b",
    "remote": r"\b(remote|distributed|anywhere)\b",
    "hybrid": r"\b(hybrid)\b",
    "on-site": r"\b(on.?site|in.?office|in.?person)\b",
}

SALARY_PATTERN = re.compile(r"\$\s*(\d{1,3}(?:,\d{3})*(?:k)?)\s*(?:[-–—]\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:k)?))?", re.IGNORECASE)


@dataclass
class ParsedJD:
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
    experience_level: str = ""
    employment_type: str = ""
    salary_range: dict = field(default_factory=dict)


class JDParser:
    def parse(self, description: str, extra_skills: list[str] | None = None) -> ParsedJD:
        if not description:
            return ParsedJD()

        text = description.lower()
        all_skills = list(set(SKILL_KEYWORDS + [s.lower() for s in (extra_skills or [])]))
        
        required_skills = self._extract_skills(self._extract_required_section(text), all_skills)
        preferred_skills = self._extract_skills(self._extract_preferred_section(text), all_skills)
        preferred_skills = [s for s in preferred_skills if s not in required_skills]

        return ParsedJD(
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            experience_level=self._detect_level(text),
            employment_type=self._detect_employment(text),
            salary_range=self._extract_salary(description),
        )

    def _extract_required_section(self, text: str) -> str:
        patterns = [
            r"required[^:]*:(.*?)(?=preferred|nice.to.have|bonus|$)",
            r"must have[^:]*:(.*?)(?=preferred|nice.to.have|bonus|$)",
        ]
        for pat in patterns:
            m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
            if m:
                return m.group(1)
        return text

    def _extract_preferred_section(self, text: str) -> str:
        patterns = [
            r"preferred[^:]*:(.*?)(?=required|must have|$)",
            r"nice.to.have[^:]*:(.*?)(?=required|must have|$)",
            r"bonus[^:]*:(.*?)(?=required|must have|$)",
        ]
        for pat in patterns:
            m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
            if m:
                return m.group(1)
        return ""

    def _extract_skills(self, text: str, skill_list: list[str]) -> list[str]:
        found = []
        for skill in skill_list:
            # Escape regex characters except for . and # which are common in C#, .NET
            safe_skill = re.escape(skill)
            # Use negative lookbehind and lookahead to avoid partial word matches
            # but handle special characters like C# and .NET
            if re.search(r"(?<![a-zA-Z0-9])" + safe_skill + r"(?![a-zA-Z0-9])", text, re.IGNORECASE):
                found.append(skill)
        return found

    def _detect_level(self, text: str) -> str:
        for level, pattern in LEVEL_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                return level
        return "mid"

    def _detect_employment(self, text: str) -> str:
        detected = []
        for etype, pattern in EMPLOYMENT_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(etype)
        return ", ".join(detected) if detected else "full-time"

    def _extract_salary(self, text: str) -> dict:
        m = SALARY_PATTERN.search(text)
        if not m:
            return {}
        low_raw, high_raw = m.group(1), m.group(2)

        def normalize(val: str) -> int | None:
            if not val:
                return None
            val = val.replace(",", "")
            if val.lower().endswith("k"):
                return int(val[:-1]) * 1000
            n = int(val)
            return n * 1000 if n < 1000 else n

        return {"low": normalize(low_raw), "high": normalize(high_raw), "currency": "USD"}
