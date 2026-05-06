"""
Recruiter Scraper — discovers hiring managers via Apollo and Hunter APIs.
"""
import httpx
import logging
from config.settings import get_settings

logger = logging.getLogger(__name__)


class RecruiterScraper:
    def __init__(self):
        self.settings = get_settings()

    async def find_recruiters(self, company: str, job_title: str) -> list[dict]:
        results = []
        if self.settings.apollo_api_key:
            apollo_results = await self._search_apollo(company, job_title)
            results.extend(apollo_results)
        if self.settings.hunter_api_key and not results:
            hunter_results = await self._search_hunter(company)
            results.extend(hunter_results)
        if not results:
            results = self._fallback_guess(company)
        return results

    async def _search_apollo(self, company: str, job_title: str) -> list[dict]:
        url = "https://api.apollo.io/v1/mixed_people/search"
        payload = {
            "api_key": self.settings.apollo_api_key,
            "q_organization_name": company,
            "person_titles": ["recruiter", "talent acquisition", "hiring manager", "engineering manager"],
            "per_page": 5,
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
            people = data.get("people", [])
            return [
                {
                    "name": p.get("name"),
                    "title": p.get("title"),
                    "company": company,
                    "email": p.get("email"),
                    "linkedin_url": p.get("linkedin_url"),
                    "email_confidence": p.get("email_status_cd", 0),
                    "source": "apollo",
                }
                for p in people
            ]
        except Exception as e:
            logger.warning("Apollo search failed for %s: %s", company, e)
            return []

    async def _search_hunter(self, company: str) -> list[dict]:
        domain = self._guess_domain(company)
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={self.settings.hunter_api_key}&limit=5"
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
            emails = data.get("data", {}).get("emails", [])
            return [
                {
                    "name": f"{e.get('first_name', '')} {e.get('last_name', '')}".strip(),
                    "title": e.get("position"),
                    "company": company,
                    "email": e.get("value"),
                    "linkedin_url": e.get("linkedin"),
                    "email_confidence": e.get("confidence", 0) / 100,
                    "source": "hunter",
                }
                for e in emails
                if e.get("value")
            ]
        except Exception as e:
            logger.warning("Hunter search failed for %s: %s", company, e)
            return []

    def _guess_domain(self, company: str) -> str:
        clean = company.lower().replace(" ", "").replace(",", "").replace(".", "")
        return f"{clean}.com"

    def _fallback_guess(self, company: str) -> list[dict]:
        domain = self._guess_domain(company)
        return [
            {
                "name": None,
                "title": "Recruiter",
                "company": company,
                "email": f"careers@{domain}",
                "linkedin_url": None,
                "email_confidence": 0.3,
                "source": "guess",
            }
        ]
