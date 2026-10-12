from __future__ import annotations

import json
from typing import Any, List, Optional

import requests

from app.config import settings


INDEX_NAME = settings.index_name


def _headers(extra: Optional[dict] = None) -> dict:
    headers = {"Authorization": f"Bearer {settings.master_key}"}
    if extra:
        headers.update(extra)
    return headers


def ensure_index() -> None:
    url = f"{settings.meili_host}/indexes/{INDEX_NAME}"
    response = requests.get(url, headers=_headers())
    if response.status_code == 404:
        requests.post(
            f"{settings.meili_host}/indexes",
            headers=_headers({"Content-Type": "application/json"}),
            json={"uid": INDEX_NAME, "primaryKey": "id"},
        )


def index_documents(documents: List[dict[str, Any]]) -> dict:
    ensure_index()
    url = f"{settings.meili_host}/indexes/{INDEX_NAME}/documents"
    payload = documents
    response = requests.post(
        url,
        headers=_headers({"Content-Type": "application/json"}),
        json=payload,
    )
    if response.status_code not in (200, 202):
        raise RuntimeError(f"Failed to index documents: {response.status_code} {response.text}")
    return response.json()


def search_documents(query: str, limit: int = 10, site: Optional[str] = None) -> dict:
    ensure_index()
    params = {"q": query, "limit": limit}
    if site:
        params["filter"] = f"site = '{site}'"
    url = f"{settings.meili_host}/indexes/{INDEX_NAME}/search"
    response = requests.get(url, headers=_headers(), params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Search failed: {response.status_code} {response.text}")
    data = response.json()
    hits = data.get("hits", [])
    return {
        "hits": hits,
        "total": data.get("estimatedTotalHits", len(hits)),
        "query": query,
    }
