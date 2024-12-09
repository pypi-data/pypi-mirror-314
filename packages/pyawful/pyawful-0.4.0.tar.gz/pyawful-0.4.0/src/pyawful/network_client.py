from typing import Any
from urllib.parse import urljoin

from requests import request

from .models import ThreadSortField
from .types import AwfulCookies

DEFAULT_BASE_URL = "https://forums.somethingawful.com/"


class NetworkClient:
    def __init__(
        self,
        *,
        cookies: AwfulCookies | None = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self._base_url = base_url
        self._cookies: dict[str, str] = {}

        if cookies is not None:
            self._cookies["sessionhash"] = cookies["sessionhash"]
            self._cookies["bbuserid"] = cookies["bbuserid"]
            self._cookies["bbpassword"] = cookies["bbpassword"]

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

    def logout(self, csrf_token: str):
        return self.request(
            "GET",
            "/account.php",
            data={
                "action": "logout",
                "ma": csrf_token,
            },
        )

    def get_user_control_panel(self):
        return self.request("GET", "/usercp.php")

    def get_user_profile(self, user_id: int):
        return self.request(
            "GET",
            "/member.php",
            params={
                "action": "getinfo",
                "userid": user_id,
            },
        )

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
                "sortfield": thread_sort_field.value,
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
