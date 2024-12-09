from datetime import datetime
from typing import Mapping, Sequence

from lxml.cssselect import CSSSelector
from lxml.html import HtmlElement

from ..models import Profile, User
from .common import parse_attribute_str, parse_str

DATE_FORMAT_LAST_POST = "%b %d, %Y %H:%M"  # Dec 5, 2024 21:37
DATE_FORMAT_REGISTRATION = "%b %d, %Y"

CSS_USER_USERINFO = CSSSelector(".userinfo")
CSS_USER_USERNAME = CSSSelector(".userinfo .author")
CSS_USER_REGISTERED_AT = CSSSelector(".userinfo .registered")
CSS_USER_ADDITIONAL_INFO = CSSSelector(".info .additional")
CSS_USER_RAP_SHEET_LINK = CSSSelector('a[href^="banlist.php"]')
CSS_USER_CONTACT_ICQ = CSSSelector(".contacts .icq + dd")
CSS_USER_CONTACT_AIM = CSSSelector(".contacts .aim + dd")
CSS_USER_CONTACT_YAHOO = CSSSelector(".contacts .yahoo + dd")
CSS_USER_CONTACT_HOMEPAGE = CSSSelector(".contacts .homepage + dd")
CSS_USER_CONTACT_IS_UNSET = CSSSelector(".unset")


def parse_user(document: HtmlElement) -> User:
    rap_sheet_href = parse_attribute_str(CSS_USER_RAP_SHEET_LINK(document), "href")
    user_id = int(rap_sheet_href.split("=")[-1])

    username = parse_str(CSS_USER_USERNAME(document))

    return User(id=user_id, username=username)


def parse_contact_info(contact_info_elements: Sequence[HtmlElement]) -> str | None:
    contact_info = contact_info_elements[-1]

    if contact_info is None or len(CSS_USER_CONTACT_IS_UNSET(contact_info)) > 0:
        return None

    return contact_info.text_content().strip()


def parse_additional_info(document: HtmlElement) -> Mapping[str, str]:
    additional_info_element: HtmlElement = CSS_USER_ADDITIONAL_INFO(document).pop()

    if additional_info_element is None:
        return {}

    info_children = additional_info_element.iterchildren()

    additional_info = {}

    for key_element in info_children:
        value_element = next(info_children, None)

        key = key_element.text_content().lower().replace(" ", "_")
        value = value_element.text_content() if value_element is not None else ""

        additional_info[key] = value

    return additional_info


def parse_profile_page(document: HtmlElement) -> Profile:
    user = parse_user(document)

    contact_icq = parse_contact_info(CSS_USER_CONTACT_ICQ(document))
    contact_aim = parse_contact_info(CSS_USER_CONTACT_AIM(document))
    contact_yahoo = parse_contact_info(CSS_USER_CONTACT_YAHOO(document))
    contact_homepage = parse_contact_info(CSS_USER_CONTACT_HOMEPAGE(document))

    registered_at = datetime.strptime(
        parse_str(CSS_USER_REGISTERED_AT(document)),
        DATE_FORMAT_REGISTRATION,
    )

    additional_info = parse_additional_info(document)

    last_posted_at = datetime.strptime(
        additional_info.get("last_post", ""), DATE_FORMAT_LAST_POST
    )
    post_rate = float(additional_info.get("post_rate", "0").split(" ")[0])
    post_count = int(additional_info.get("post_count", "0"))

    return Profile(
        user=user,
        homepage_url=contact_homepage,
        aim_username=contact_aim,
        icq_name=contact_icq,
        yahoo_name=contact_yahoo,
        registered_at=registered_at,
        last_posted_at=last_posted_at,
        post_rate=post_rate,
        post_count=post_count,
    )
