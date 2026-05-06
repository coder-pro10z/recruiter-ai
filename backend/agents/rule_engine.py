"""
Rule Engine — scores jobs against configurable matching rules.
"""
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

DEFAULT_RULES = {
    "required_skills": ["python", "fastapi", "postgresql", "react", "typescript"],
    "preferred_skills": ["aws", "docker", "kubernetes", "machine learning"],
    "blocked_companies": [],
    "blocked_keywords": ["unpaid", "commission only", "no benefits"],
    "min_match_score": 0.4,
    "target_levels": ["mid", "senior", "staff"],
    "target_employment": ["full-time", "remote", "hybrid"],
}


@dataclass
class MatchResult:
    score: float
    is_match: bool
    reasons: list[str] = field(default_factory=list)


class RuleEngine:
    def __init__(self, rules: dict | None = None):
        self.rules = {**DEFAULT_RULES, **(rules or {})}

    def evaluate(
        self,
        title: str,
        company: str,
        description: str,
        required_skills: list[str],
        preferred_skills: list[str],
        experience_level: str,
        employment_type: str,
    ) -> MatchResult:
        reasons: list[str] = []
        score = 0.0
        text = (title + " " + description).lower()

        # Block check
        for blocked in self.rules["blocked_companies"]:
            if blocked.lower() in company.lower():
                return MatchResult(score=0.0, is_match=False, reasons=[f"Blocked company: {blocked}"])

        for kw in self.rules["blocked_keywords"]:
            if kw.lower() in text:
                return MatchResult(score=0.0, is_match=False, reasons=[f"Blocked keyword: {kw}"])

        # Required skill matching (up to 0.6 of score)
        my_required = self.rules["required_skills"]
        matched_required = [s for s in required_skills if s in my_required]
        if my_required:
            req_score = len(matched_required) / len(my_required) * 0.6
            score += req_score
            if matched_required:
                reasons.append(f"Matched required skills: {', '.join(matched_required)}")

        # Preferred skill matching (up to 0.2)
        my_preferred = self.rules["preferred_skills"]
        matched_preferred = [s for s in preferred_skills if s in my_preferred]
        if my_preferred:
            pref_score = len(matched_preferred) / len(my_preferred) * 0.2
            score += pref_score
            if matched_preferred:
                reasons.append(f"Matched preferred skills: {', '.join(matched_preferred)}")

        # Level match (0.1)
        target_levels = self.rules["target_levels"]
        if experience_level in target_levels:
            score += 0.1
            reasons.append(f"Level match: {experience_level}")
        elif experience_level:
            reasons.append(f"Level mismatch: {experience_level} not in {target_levels}")

        # Employment type match (0.1)
        target_employment = self.rules["target_employment"]
        if any(t in employment_type for t in target_employment):
            score += 0.1
            reasons.append(f"Employment match: {employment_type}")

        is_match = score >= self.rules["min_match_score"]
        return MatchResult(score=round(score, 3), is_match=is_match, reasons=reasons)
