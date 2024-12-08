from dataclasses import dataclass
from datetime import datetime
from typing import Sequence


@dataclass
class Thread:
    id: int
    title: str


@dataclass
class ThreadMetadata(Thread):
    tags: Sequence[str]

    updated_at: datetime

    rating: float
    rating_count: int

    is_closed: bool
    is_sticky: bool

    is_unread: bool
    unread_count: int
