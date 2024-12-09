import re
from datetime import datetime

from lxml.cssselect import CSSSelector
from lxml.html import HtmlElement, tostring

from ..models import Forum, Post, PostList, Thread, User
from .common import parse_attribute_str, parse_int, parse_str

DATE_FORMAT_CREATED_AT = "%b %d, %Y %H:%M"  # Dec 1, 2024 23:32
DATE_FORMAT_UPDATED_AT = "%H:%M on %b %d, %Y"  # 05:20 on Dec  5, 2024

PATTERN_EDIT_LINE = re.compile(
    "^(?P<username>.+) fucked around with this message at (?P<timestamp>.+)$"
)

CSS_FORUM_IS_LOCKED = CSSSelector("[alt=Reply]:not([src*='forum-closed'])")
CSS_FORUM_BREADCRUMBS = CSSSelector(
    "div.breadcrumbs:first-of-type .mainbodytextlarge a:not(.bclast)"
)

CSS_THREAD_ANCHOR = CSSSelector(
    "div.breadcrumbs:first-of-type .mainbodytextlarge .bclast"
)
CSS_THREAD_CURRENT_PAGE = CSSSelector(".pages select option[selected]")
CSS_THREAD_LAST_PAGE = CSSSelector(".pages select option:last-child")

CSS_THREAD_POSTS = CSSSelector("#thread .post")

CSS_POST_IS_SEEN = CSSSelector("[class^=seen]")
CSS_POST_IS_IGNORED = CSSSelector(".ignored")
CSS_POST_BODY = CSSSelector(".postbody, .complete_shit")
CSS_POST_EDIT_LINE = CSSSelector(".postbody .editedby, .complete_shit .editedby")
CSS_POST_IS_EDITABLE = CSSSelector('.postbuttons [alt="Edit"]')
CSS_POST_CREATED_AT = CSSSelector(".postdate")

CSS_POST_AUTHOR_PROFILE_LINK = CSSSelector(".profilelinks li:first-of-type a")
CSS_POST_AUTHOR = CSSSelector("td.userinfo .author")


def parse_post_body(post_body: HtmlElement) -> str:
    result: str = ""
    for e in post_body.iterchildren():
        # Hacky omit of the editedby tag at the end of the post body
        e_class = e.get("class") or ""
        if "editedby" in e_class:
            continue

        e_html = tostring(e, encoding="unicode")

        if isinstance(e_html, str):
            result += e_html
            continue

        if isinstance(e_html, bytes):
            result += e_html.decode()
            continue

    return result.strip()


def parse_created_at(post_item: HtmlElement) -> datetime:
    # This is a bit messy, but it seems to work for now.
    created_at_str = (
        parse_str(CSS_POST_CREATED_AT(post_item))
        .replace("#", "")
        .replace("?", "")
        .strip()
    )

    return datetime.strptime(created_at_str, DATE_FORMAT_CREATED_AT)


def parse_updated_at(post_item: HtmlElement) -> datetime | None:
    edit_line_elements = CSS_POST_EDIT_LINE(post_item)

    if len(edit_line_elements) == 0:
        return None

    edit_line_text = edit_line_elements.pop().text_content().strip()
    edit_line_match = PATTERN_EDIT_LINE.match(edit_line_text)

    if not edit_line_match:
        return None

    updated_at = datetime.strptime(
        edit_line_match.group("timestamp"), DATE_FORMAT_UPDATED_AT
    )

    return updated_at


def parse_author(post_item: HtmlElement) -> User:
    user_profile_href = parse_attribute_str(
        CSS_POST_AUTHOR_PROFILE_LINK(post_item), "href"
    )
    user_id = int(user_profile_href.split("userid=")[-1])

    username = parse_str(CSS_POST_AUTHOR(post_item))

    return User(
        id=user_id,
        username=username,
    )


def parse_post(post_item: HtmlElement) -> Post:
    post_id = int(post_item.get("id", "").replace("post", ""))

    html = parse_post_body(CSS_POST_BODY(post_item).pop())

    is_ignored = len(CSS_POST_IS_IGNORED(post_item)) > 0
    is_editable = len(CSS_POST_IS_EDITABLE(post_item)) > 0

    author = parse_author(post_item)

    created_at = parse_created_at(post_item)
    updated_at = parse_updated_at(post_item) or created_at

    return Post(
        id=post_id,
        author=author,
        is_ignored=is_ignored,
        is_editable=is_editable,
        html=html,
        created_at=created_at,
        last_modified_at=updated_at,
    )


def parse_forum_info(document: HtmlElement) -> Forum:
    forum_id = int(document.body.get("data-forum", ""))

    forum_anchor: HtmlElement = CSS_FORUM_BREADCRUMBS(document).pop()
    forum_title = forum_anchor.text_content()
    return Forum(forum_id, forum_title)


def parse_thread_info(document: HtmlElement) -> Thread:
    thread_id = int(document.body.get("data-thread", ""))

    thread_anchor: HtmlElement = CSS_THREAD_ANCHOR(document).pop()
    thread_title = thread_anchor.text_content()

    return Thread(
        id=thread_id,
        title=thread_title,
    )


def parse_thread_page(document: HtmlElement) -> PostList:
    forum = parse_forum_info(document)
    thread = parse_thread_info(document)

    is_locked = False

    current_page = parse_int(CSS_THREAD_CURRENT_PAGE(document))
    last_page = parse_int(CSS_THREAD_LAST_PAGE(document))

    thread_posts = CSS_THREAD_POSTS(document)

    return PostList(
        forum,
        thread,
        [parse_post(p) for p in thread_posts],
        is_locked,
        current_page,
        last_page,
    )


__all__ = ("parse_thread_page",)
