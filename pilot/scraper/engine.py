import hashlib
import time
from pathlib import Path
from typing import Optional
import httpx
from selectolax.parser import HTMLParser
from pilot.config import get_config

class ScraperEngine:
    def __init__(self, config=None):
        self.config = config or get_config()
        self.cache_dir = self.config.cache_dir / "scraper"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, url: str) -> Path:
        url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return self.cache_dir / f"{url_hash}.html"

    def _is_cache_valid(self, cache_file: Path) -> bool:
        if not cache_file.exists():
            return False
        age = time.time() - cache_file.stat().st_mtime
        return age < self.config.cache_ttl_seconds

    async def fetch_html(self, url: str, force_refresh: bool = False) -> str:
        cache_file = self._get_cache_path(url)
        if not force_refresh and self._is_cache_valid(cache_file):
            return cache_file.read_text(encoding="utf-8")

        headers = {
            "User-Agent": self.config.scraper_user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        async with httpx.AsyncClient(http2=True, timeout=20.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            html = resp.text
            cache_file.write_text(html, encoding="utf-8")
            return html

    async def parse_url(self, url: str, force_refresh: bool = False) -> HTMLParser:
        html = await self.fetch_html(url, force_refresh=force_refresh)
        return HTMLParser(html)
