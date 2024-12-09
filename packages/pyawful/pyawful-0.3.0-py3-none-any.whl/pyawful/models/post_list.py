from dataclasses import dataclass
from typing import Sequence

from .forum import Forum
from .post import Post
from .thread import Thread


@dataclass
class PostList:
    forum: Forum
    thread: Thread
    posts: Sequence[Post]

    is_locked: bool

    current_page: int
    last_page: int
