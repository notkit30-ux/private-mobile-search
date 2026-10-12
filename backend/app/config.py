from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    meili_host: str = os.getenv("MEILI_HOST", "http://localhost:7700")
    master_key: str = os.getenv("MEILI_MASTER_KEY", "change-me")
    api_key: str = os.getenv("API_KEY", "change-me")
    index_name: str = "private_search"


settings = Settings()
