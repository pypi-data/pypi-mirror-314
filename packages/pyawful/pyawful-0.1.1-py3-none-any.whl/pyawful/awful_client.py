from lxml.html import HtmlElement, fromstring, html_parser

from .models import ThreadSortField
from .network_client import AuthenticatedNetworkClientSession, NetworkClient
from .parse import (
    parse_forum_page,
    parse_thread_page,
)
from .types import AwfulClient, AwfulSession


class InternalAwfulClient(AwfulClient):
    def __init__(self, network_client: NetworkClient):
        self._network_client = network_client

    @staticmethod
    def _parse(html: str) -> HtmlElement:
        return fromstring(html, parser=html_parser)

    def get_forum_threads(
        self,
        forum_id: int,
        page: int = 1,
        sort_field: ThreadSortField = ThreadSortField.CREATED_AT,
        sort_invert: bool = False,
    ):
        response = self._network_client.get_forum(
            forum_id,
            thread_page=page,
            thread_sort_field=sort_field,
            thread_sort_invert=sort_invert,
        )
        document = self._parse(response.text)
        return parse_forum_page(document)

    def get_thread_posts(self, thread_id: int, page: int = 1):
        response = self._network_client.get_thread(thread_id, page)
        document = self._parse(response.text)
        return parse_thread_page(document)


class AuthenticatedAwfulSession(AwfulSession):
    def __init__(self, username: str, password: str):
        self._session = AuthenticatedNetworkClientSession(username, password)

    def __enter__(self) -> AwfulClient:
        network_client = self._session.__enter__()
        return InternalAwfulClient(network_client)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._session.__exit__(exc_type, exc_val, exc_tb)
