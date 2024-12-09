import re

from lxml.cssselect import CSSSelector
from lxml.html import HtmlElement

from ..models import (
    Forum,
    ThreadList,
    ThreadMetadata,
    ThreadSortField,
)
from .common import parse_attribute_int, parse_datetime, parse_int, parse_str

DATE_FORMAT_UPDATED_AT = "%H:%M %b %d, %Y"  # 21:06 May 23, 2012

PATTERN_RATING = re.compile("^([0-9]+) votes - ([0-9.]+) average$")

CSS_FORUM_IS_LOCKED = CSSSelector("[alt=Reply]:not([src*='forum-closed'])")
CSS_FORUM_ANCHOR = CSSSelector("div.breadcrumbs:first-of-type .bclast")
CSS_FORUM_CURRENT_PAGE = CSSSelector(".pages select option[selected]")
CSS_FORUM_LAST_PAGE = CSSSelector(".pages select option:last-child")

# We could include the `is_announce` selectors as part of that
# but CSSSelector seems to not work well with `:not(:has())`?
CSS_FORUM_THREADS = CSSSelector("#forum .thread")

CSS_THREAD_TITLE = CSSSelector(".thread_title")
CSS_THREAD_IS_ANNOUNCE = CSSSelector(".announcement")
CSS_THREAD_IS_STICKY = CSSSelector(".title_sticky")
CSS_THREAD_IS_CLOSED = CSSSelector(".closed")
CSS_THREAD_IS_READ = CSSSelector(".lastseen .x")
CSS_THREAD_RATING = CSSSelector(".rating img")
CSS_THREAD_TAG_ICON = CSSSelector(".icon img, .icon2 img")
CSS_THREAD_UNREAD_COUNT = CSSSelector(".lastseen .count")
CSS_THREAD_REPLY_COUNT = CSSSelector(".replies")
CSS_THREAD_UPDATED_AT = CSSSelector(".lastpost .date")
CSS_THREAD_AUTHOR_LINK = CSSSelector(".author a")


def is_announce_thread(thread_item: HtmlElement) -> bool:
    return len(CSS_THREAD_IS_ANNOUNCE(thread_item)) > 0


def parse_forum_info(document: HtmlElement) -> Forum:
    forum_id = int(document.body.get("data-forum", ""))

    forum_anchor: HtmlElement = CSS_FORUM_ANCHOR(document).pop()
    forum_title = forum_anchor.text_content()
    return Forum(forum_id, forum_title)


def parse_thread_item(thread_item: HtmlElement) -> ThreadMetadata:
    thread_id = int(thread_item.get("id", "").replace("thread", ""))
    title = parse_str(CSS_THREAD_TITLE(thread_item))

    is_sticky = len(CSS_THREAD_IS_STICKY(thread_item)) > 0
    is_closed = len(CSS_THREAD_IS_CLOSED(thread_item)) > 0
    is_unread = len(CSS_THREAD_IS_READ(thread_item)) == 0

    reply_count = parse_int(CSS_THREAD_REPLY_COUNT(thread_item), 0)

    unread_count = parse_int(CSS_THREAD_UNREAD_COUNT(thread_item), default=-1)

    if unread_count < 0:
        unread_count = reply_count + 1

    tags = [
        t.get("src", "") for t in CSS_THREAD_TAG_ICON(thread_item) if t.get("src", "")
    ]

    rating_elements = CSS_THREAD_RATING(thread_item)

    if len(rating_elements) > 0:
        rating_str = parse_str(rating_elements)
        match = PATTERN_RATING.match(rating_str)

        rating = float(match[2]) if match else 0
        rating_count = int(match[1]) if match else 0
    else:
        rating = 0
        rating_count = 0

    updated_at = parse_datetime(
        CSS_THREAD_UPDATED_AT(thread_item), DATE_FORMAT_UPDATED_AT
    )

    return ThreadMetadata(
        id=thread_id,
        title=title,
        tags=tags,
        updated_at=updated_at,
        rating=rating,
        rating_count=rating_count,
        is_closed=is_closed,
        is_sticky=is_sticky,
        is_unread=is_unread,
        unread_count=unread_count,
    )


def parse_forum_page(document: HtmlElement) -> ThreadList:
    current_page = parse_attribute_int(CSS_FORUM_CURRENT_PAGE(document), "value")
    last_page = parse_attribute_int(CSS_FORUM_LAST_PAGE(document), "value")

    is_locked = len(CSS_FORUM_IS_LOCKED(document)) > 0
    forum = parse_forum_info(document)

    forum_threads = CSS_FORUM_THREADS(document)

    return ThreadList(
        forum=forum,
        threads=[
            parse_thread_item(t) for t in forum_threads if not is_announce_thread(t)
        ],
        is_locked=is_locked,
        current_page=current_page,
        last_page=last_page,
        sort_field=ThreadSortField.CREATED_AT,
        sort_inverted=False,
    )


__all__ = ("parse_forum_page",)
