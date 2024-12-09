from datetime import datetime

from lxml.html import HtmlElement, fromstring, html_parser

from .models import ThreadSortField
from .network_client import NetworkClient
from .parse import (
    parse_forum_page,
    parse_profile_page,
    parse_thread_page,
)
from .types import AwfulClient, AwfulCookies, AwfulSession

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
    def __init__(
        self,
        username: str,
        password: str,
    ):
        self._username = username
        self._password = password

        self._logout_csrf_token: str | None = None
        self._session_cookies: AwfulCookies | None = None
        self._session_expiration: datetime | None = None

        self._network_client = NetworkClient()

    @staticmethod
    def _parse(html: str) -> HtmlElement:
        return fromstring(html, parser=html_parser)

    def resume_session(self, cookies: AwfulCookies, expiration: datetime):
        self._session_cookies = AwfulCookies(**cookies)
        self._session_expiration = expiration

    def get_cookies(self) -> AwfulCookies:
        if self._session_cookies is None:
            raise ValueError("not logged in")

        # Return a copy
        return AwfulCookies(**self._session_cookies)

    def get_expiration(self):
        return self._session_expiration

    def login(self):
        if (
            self._session_expiration is not None
            and self._session_expiration > datetime.now()
        ):
            # If the session expiration is set and is in the future then
            # we can probably be safe to assume that we don't need to log
            # in again.
            return

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

        self._session_cookies = AwfulCookies(
            bbuserid=bb_user_id,
            bbpassword=bb_password,
            sessionhash=session_hash,
        )
        self._session_expiration = datetime.fromtimestamp(session_expiry)

    def logout(self):
        if self._logout_csrf_token is None:
            return

        self._network_client.logout(self._logout_csrf_token)

    def get_client(self) -> AwfulClient:
        if self._session_cookies is None:
            raise ValueError("not logged in")

        network_client = NetworkClient(cookies=self._session_cookies)
        return InternalAwfulClient(network_client)

    def __enter__(self) -> AwfulClient:
        self.login()

        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
