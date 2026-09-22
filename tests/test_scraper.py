import pytest
from selectolax.parser import HTMLParser
from pilot.scraper.trending import TrendingParser

SAMPLE_TRENDING_HTML = """
<html>
  <body>
    <article class="Box-row">
      <h2>
        <a href="/octocat/Hello-World">octocat / Hello-World</a>
      </h2>
      <p>My first repository</p>
      <span itemprop="programmingLanguage">Python</span>
      <span class="d-inline-block float-sm-right">120 stars today</span>
    </article>
  </body>
</html>
"""

class MockScraperEngine:
    async def parse_url(self, url: str, force_refresh: bool = False):
        return HTMLParser(SAMPLE_TRENDING_HTML)

@pytest.mark.asyncio
async def test_trending_parser_mock():
    mock_engine = MockScraperEngine()
    parser = TrendingParser(engine=mock_engine)
    repos = await parser.get_trending()

    assert len(repos) == 1
    repo = repos[0]
    assert repo.owner == "octocat"
    assert repo.name == "Hello-World"
    assert repo.language == "Python"
    assert repo.description == "My first repository"
    assert repo.stars_today == "120 stars today"
