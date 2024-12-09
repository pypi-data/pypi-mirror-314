from dataclasses import dataclass
from datetime import datetime

from .user import User


@dataclass
class Post:
    id: int

    author: User

    is_ignored: bool
    is_editable: bool

    html: str

    created_at: datetime
    last_modified_at: datetime
