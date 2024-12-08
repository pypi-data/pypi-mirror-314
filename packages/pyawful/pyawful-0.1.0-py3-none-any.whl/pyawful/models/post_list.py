from dataclasses import dataclass
from typing import Sequence

from .forum import Forum
from .thread import Thread
from .post import Post


@dataclass
class PostList:
    forum: Forum
    thread: Thread
    posts: Sequence[Post]

    is_locked: bool

    current_page: int
    last_page: int
