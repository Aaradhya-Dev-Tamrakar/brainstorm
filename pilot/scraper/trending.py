from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from pilot.scraper.engine import ScraperEngine

class TrendingRepo(BaseModel):
    name: str
    owner: str
    url: str
    description: Optional[str] = None
    language: Optional[str] = None
    total_stars: Optional[str] = None
    stars_today: Optional[str] = None


class TrendingParser:
    def __init__(self, engine: Optional[ScraperEngine] = None):
        self.engine = engine or ScraperEngine()

    async def get_trending(self, language: Optional[str] = None, since: str = "daily") -> List[TrendingRepo]:
        url = "https://github.com/trending"
        if language:
            url += f"/{language}"
        url += f"?since={since}"

        parser = await self.engine.parse_url(url)
        repos: List[TrendingRepo] = []

        articles = parser.css("article.Box-row")
        for article in articles:
            h2 = article.css_first("h2 a")
            if not h2:
                continue

            repo_path = h2.attributes.get("href", "").strip().lstrip("/")
            parts = repo_path.split("/")
            if len(parts) < 2:
                continue

            owner, name = parts[0], parts[1]
            repo_url = f"https://github.com/{owner}/{name}"

            p_desc = article.css_first("p")
            description = p_desc.text().strip() if p_desc else None

            lang_node = article.css_first("[itemprop='programmingLanguage']")
            lang = lang_node.text().strip() if lang_node else None

            # Stars today / period
            stars_today_node = article.css_first("span.d-inline-block.float-sm-right")
            stars_today = stars_today_node.text().strip() if stars_today_node else None

            repos.append(
                TrendingRepo(
                    name=name,
                    owner=owner,
                    url=repo_url,
                    description=description,
                    language=lang,
                    stars_today=stars_today
                )
            )

        return repos
