from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from .forum import Forum
from .thread import ThreadMetadata


class ThreadSortField(Enum):
    CREATED_AT = "threadcreate"
    UPDATED_AT = "lastpost"
    REPLY_COUNT = "replycount"
    RATING = "voteavg"


@dataclass
class ThreadList:
    forum: Forum
    threads: Sequence[ThreadMetadata]

    is_locked: bool

    current_page: int
    last_page: int
    sort_field: ThreadSortField
    sort_inverted: bool
