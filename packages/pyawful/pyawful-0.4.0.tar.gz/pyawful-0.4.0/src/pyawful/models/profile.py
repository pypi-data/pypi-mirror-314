from dataclasses import dataclass
from datetime import datetime

from .user import User


@dataclass
class Profile:
    user: User

    homepage_url: str | None
    aim_username: str | None
    icq_name: str | None
    yahoo_name: str | None

    registered_at: datetime
    last_posted_at: datetime

    post_rate: float
    post_count: int
