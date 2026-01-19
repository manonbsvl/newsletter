from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Article:
    source: str          # média (Reuters, Le Monde…)
    title: str
    summary: str
    url: str
    published_at: Optional[datetime]
    tags: List[str] = field(default_factory=list)
    score: int = 0
    image_url: Optional[str] = None
