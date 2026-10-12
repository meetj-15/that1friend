from urllib.parse import urlparse

from tavily import AsyncTavilyClient

from app.core.config import settings
from app.schemas.research import Source


class WebSearchService:
    def __init__(self) -> None:
        if not settings.tavily_api_key:
            raise RuntimeError("TAVILY_API_KEY is not configured")
        self.client = AsyncTavilyClient(api_key=settings.tavily_api_key)

    async def search(self, query: str, max_results: int = 5) -> list[Source]:
        result = await self.client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=False,
        )

        sources: list[Source] = []
        seen: set[str] = set()
        for item in result.get("results", []):
            url = item.get("url", "")
            if not url or url in seen:
                continue
            seen.add(url)
            sources.append(Source(
                title=item.get("title", "Untitled"),
                url=url,
                domain=urlparse(url).netloc,
                snippet=item.get("content", "")[:800],
                score=float(item.get("score", 0.0)),
            ))
        return sources
