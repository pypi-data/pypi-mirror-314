from abc import abstractmethod
from typing import Protocol, TypedDict

from .models import PostList, ThreadList, ThreadSortField


class AwfulClient(Protocol):
    @abstractmethod
    def get_forum_threads(
        self,
        forum_id: int,
        page: int = 1,
        sort_field: ThreadSortField = ThreadSortField.CREATED_AT,
        sort_invert: bool = False,
    ) -> ThreadList:
        """Get awful forum threads."""

    @abstractmethod
    def get_thread_posts(self, thread_id: int, page: int = 1) -> PostList:
        """Get an awful thread's posts."""


class AwfulSession(Protocol):
    @abstractmethod
    def __enter__(self) -> AwfulClient: ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb): ...


class AwfulCookies(TypedDict):
    bbuserid: str
    bbpassword: str
    sessionhash: str
