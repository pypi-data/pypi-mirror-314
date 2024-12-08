from datetime import datetime

from lxml.html import HtmlElement, fromstring, html_parser

from .models import ThreadSortField
from .network_client import ClientAuthCookies, NetworkClient
from .parse import (
    parse_forum_page,
    parse_profile_page,
    parse_thread_page,
)
from .types import AwfulClient, AwfulSession

AUTH_COOKIES = (
    "bbuserid",
    "bbpassword",
    "sessionid",
    "sessionhash",
)


class InternalAwfulClient(AwfulClient):
    def __init__(self, network_client: NetworkClient):
        self._network_client = network_client

    @staticmethod
    def _parse(html: str) -> HtmlElement:
        return fromstring(html, parser=html_parser)

    def get_user_profile(self, user_id: int):
        response = self._network_client.get_user_profile(user_id)
        document = self._parse(response.text)
        return parse_profile_page(document)

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
        self._username = username
        self._password = password

        self._logout_csrf_token: str | None = None
        self._auth_cookies: ClientAuthCookies | None = None

        self._network_client = NetworkClient()

    @staticmethod
    def _parse(html: str) -> HtmlElement:
        return fromstring(html, parser=html_parser)

    def login(self):
        response = self._network_client.login(self._username, self._password)

        # The cookies are in the redirect and I can't find a better way to get at them.
        for r in response.history:
            for c in r.cookies:
                response.cookies.set_cookie(c)

        session_expiry = min(
            c.expires
            for c in response.cookies
            if c.name in AUTH_COOKIES and c.expires is not None
        )

        session_hash = response.cookies.get("sessionhash")
        bb_user_id = response.cookies.get("bbuserid")
        bb_password = response.cookies.get("bbpassword")

        if bb_user_id is None or bb_password is None or session_hash is None:
            raise ValueError("could not log in")

        return ClientAuthCookies(
            expiration=datetime.fromtimestamp(session_expiry),
            bb_user_id=bb_user_id,
            bb_password=bb_password,
            session_hash=session_hash,
        )

    def logout(self):
        if self._logout_csrf_token is None:
            return

        self._network_client.logout(self._logout_csrf_token)

    def get_client(self) -> AwfulClient:
        if self._auth_cookies is None:
            raise

        network_client = NetworkClient(auth_cookies=self._auth_cookies)
        return InternalAwfulClient(network_client)

    def __enter__(self) -> AwfulClient:
        self.login()

        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
