from contextlib import AbstractContextManager
from urllib.parse import urljoin
from typing import Any
from datetime import datetime
from dataclasses import dataclass

from requests import request

from .models import ThreadSortField

DEFAULT_BASE_URL = "https://forums.somethingawful.com/"
AUTH_COOKIES = (
    "bbuserid",
    "bbpassword",
    "sessionid",
    "sessionhash",
)


@dataclass
class ClientAuthCookies:
    expiration: datetime
    bb_user_id: str
    bb_password: str
    session_hash: str


class NetworkClient:
    def __init__(
        self,
        *,
        auth_cookies: ClientAuthCookies | None = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self._base_url = base_url
        self._cookies: dict[str, str] = {}

        if auth_cookies:
            self._cookies["sessionhash"] = auth_cookies.session_hash
            self._cookies["bbuserid"] = auth_cookies.bb_user_id
            self._cookies["bbpassword"] = auth_cookies.bb_password

    def request(self, method: str, path: str, *, params: Any = None, data: Any = None):
        return request(
            method,
            urljoin(self._base_url, path),
            cookies=self._cookies,
            data=data,
            params=params,
        )

    def login(self, username: str, password: str):
        return self.request(
            "POST",
            "/account.php",
            data={
                "action": "login",
                "username": username,
                "password": password,
                "next": "/",
            },
        )

    def get_user_control_panel(self):
        return self.request("GET", "/usercp.php")

    def get_forum(
        self,
        forum_id: int,
        *,
        thread_page: int = 1,
        thread_sort_field: ThreadSortField = ThreadSortField.CREATED_AT,
        thread_sort_invert: bool = False,
    ):
        return self.request(
            "GET",
            "/forumdisplay.php",
            params={
                "forumid": forum_id,
                "pagenumber": thread_page,
                "sortfield": thread_sort_field,
                "sortorder": "asc" if thread_sort_invert else "desc",
            },
        )

    def get_thread(self, thread_id: int, page: int = 1):
        return self.request(
            "GET",
            "/showthread.php",
            params={
                "thread_id": thread_id,
                "pagenumber": page,
            },
        )

    def get_bookmarked_threads(self, page: int = 1):
        return self.request(
            "GET",
            "/bookmarkthreads.php",
            params={
                "pagenumber": page,
            },
        )


class AuthenticatedNetworkClientSession(AbstractContextManager):
    def __init__(
        self, username: str, password: str, *, base_url: str = DEFAULT_BASE_URL
    ):
        self._username = username
        self._password = password
        self._base_url = base_url

        self._unauthenticated_client = NetworkClient(base_url=self._base_url)

    def _authenticate(self):
        response = self._unauthenticated_client.login(self._username, self._password)

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

    def __enter__(self) -> NetworkClient:
        auth_cookies = self._authenticate()

        return NetworkClient(auth_cookies=auth_cookies, base_url=self._base_url)

    def __exit__(self, exc_type, exc_value, traceback, /):
        pass
