from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class SearchDocument(BaseModel):
    id: str
    title: str
    url: str
    content: str
    site: Optional[str] = None
    source: Optional[str] = None


class SearchRequest(BaseModel):
    q: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=30)
    site: Optional[str] = None


class SearchResponseItem(BaseModel):
    id: str
    title: str
    url: str
    content: str
    site: Optional[str]
    source: Optional[str]
    score: Optional[float] = None


class SearchResponse(BaseModel):
    hits: List[SearchResponseItem]
    total: int
    query: str
