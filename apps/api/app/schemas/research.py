from pydantic import BaseModel


class Source(BaseModel):
    title: str
    url: str
    domain: str
    snippet: str = ""
    score: float = 0.0


class ResearchResult(BaseModel):
    query: str
    sources: list[Source]
    synthesis: str
