from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ResearchItem:
    """Data model for research items"""
    id: str
    title: str
    authors: List[str]
    abstract: str
    url: str
    published_date: datetime
    source: str
    tags: List[str]
    citation_count: Optional[int] = None
    references: Optional[List[str]] = None