import json
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import httpx
from pilot.config import get_config, PilotConfig

class RepoAuditResult(BaseModel):
    name: str
    owner: str
    full_name: str
    is_private: bool
    description: Optional[str] = None
    language: Optional[str] = None
    license_key: Optional[str] = None
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    topics: List[str] = Field(default_factory=list)
    has_description: bool = False
    has_license: bool = False
    has_topics: bool = False
    health_score: int = 0
    anomalies: List[str] = Field(default_factory=list)
    ci_status: Optional[str] = None


class FleetAuditSummary(BaseModel):
    total_repos_scanned: int = 0
    total_stars: int = 0
    total_forks: int = 0
    average_health_score: float = 0.0
    critical_anomalies_count: int = 0
    repos: List[RepoAuditResult] = Field(default_factory=list)


class FleetAuditor:
    def __init__(self, config: Optional[PilotConfig] = None):
        self.config = config or get_config()

    def _parse_repo_payload(self, r: Dict[str, Any]) -> RepoAuditResult:
        license_obj = r.get("license") or {}
        license_key = license_obj.get("spdx_id") or license_obj.get("key")
        topics = r.get("topics", [])
        has_desc = bool(r.get("description"))
        has_lic = bool(license_key and license_key.upper() != "NONE")
        has_top = bool(topics and len(topics) > 0)

        owner_login = r.get("owner", {}).get("login", "unknown")
        repo_name = r.get("name", "unknown")

        anomalies = []
        score = 100
        if not has_desc:
            anomalies.append("Missing description")
            score -= 25
        if not has_lic:
            anomalies.append("Missing license")
            score -= 30
        if not has_top:
            anomalies.append("No topics configured")
            score -= 20
        if r.get("open_issues_count", 0) > 10:
            anomalies.append(f"High open issue count ({r.get('open_issues_count')})")
            score -= 10

        return RepoAuditResult(
            name=repo_name,
            owner=owner_login,
            full_name=r.get("full_name", f"{owner_login}/{repo_name}"),
            is_private=r.get("private", False),
            description=r.get("description"),
            language=r.get("language"),
            license_key=license_key,
            stars=r.get("stargazers_count", 0),
            forks=r.get("forks_count", 0),
            open_issues=r.get("open_issues_count", 0),
            topics=topics,
            has_description=has_desc,
            has_license=has_lic,
            has_topics=has_top,
            health_score=max(0, score),
            anomalies=anomalies
        )

    async def audit_fleet(self, max_repos: int = 100) -> FleetAuditSummary:
        headers = self.config.get_auth_headers()
        seen_repos: Dict[str, RepoAuditResult] = {}

        async with httpx.AsyncClient(timeout=20.0, headers=headers) as client:
            if self.config.has_auth:
                # Authenticated scan: fetch personal and organization member repos
                try:
                    url = f"https://api.github.com/user/repos?per_page={max_repos}&sort=updated&affiliation=owner,organization_member"
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        for item in resp.json():
                            res = self._parse_repo_payload(item)
                            seen_repos[res.full_name] = res
                except Exception:
                    pass

            # Also fetch org and user targets if needed (or fallback if unauthenticated)
            for org in self.config.orgs:
                try:
                    url = f"https://api.github.com/orgs/{org}/repos?per_page={max_repos}&sort=updated"
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        for item in resp.json():
                            res = self._parse_repo_payload(item)
                            seen_repos[res.full_name] = res
                except Exception:
                    pass

            for user in self.config.users:
                try:
                    url = f"https://api.github.com/users/{user}/repos?per_page={max_repos}&sort=updated"
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        for item in resp.json():
                            res = self._parse_repo_payload(item)
                            seen_repos[res.full_name] = res
                except Exception:
                    pass

        all_repos = list(seen_repos.values())
        total_scanned = len(all_repos)
        if total_scanned == 0:
            return FleetAuditSummary()

        total_stars = sum(r.stars for r in all_repos)
        total_forks = sum(r.forks for r in all_repos)
        avg_score = sum(r.health_score for r in all_repos) / total_scanned
        critical_count = sum(len(r.anomalies) for r in all_repos)

        return FleetAuditSummary(
            total_repos_scanned=total_scanned,
            total_stars=total_stars,
            total_forks=total_forks,
            average_health_score=round(avg_score, 1),
            critical_anomalies_count=critical_count,
            repos=all_repos
        )
