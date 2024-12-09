from datetime import datetime
from typing import Callable, Optional, Sequence, TypeVar

from lxml.html import HtmlElement


class ParseError(BaseException): ...


ValueT = TypeVar("ValueT")


def _try_parse(elements: Sequence[HtmlElement]) -> str | None:
    if len(elements) == 0:
        return None

    return elements[0].text_content()


def _try_parse_attribute(elements: Sequence[HtmlElement], key: str) -> str | None:
    if len(elements) == 0:
        return None

    return elements[0].get(key, None)


def _coerce_value(
    constructor: Callable[[str], ValueT],
    value: str | None,
    default: Optional[ValueT] = None,
) -> ValueT:
    if value is None:
        if default is not None:
            return default

        raise ParseError("no elements matching")

    return constructor(value)


def parse_str(elements: Sequence[HtmlElement], default: str | None = None) -> str:
    value = _try_parse(elements)
    return _coerce_value(str, value, default)


def parse_int(elements: Sequence[HtmlElement], default: int | None = None) -> int:
    value = _try_parse(elements)
    return _coerce_value(int, value, default)


def parse_float(elements: Sequence[HtmlElement], default: float | None = None) -> float:
    value = _try_parse(elements)
    return _coerce_value(float, value, default)


def parse_datetime(
    elements: Sequence[HtmlElement], date_format: str, default: datetime | None = None
) -> datetime:
    value = _try_parse(elements)
    return _coerce_value(
        lambda v: datetime.strptime(v, date_format),
        value,
        default,
    )


def parse_attribute_str(
    elements: Sequence[HtmlElement], key: str, default: Optional[str] = None
) -> str:
    value = _try_parse_attribute(elements, key)
    return _coerce_value(str, value, default)


def parse_attribute_int(
    elements: Sequence[HtmlElement], key: str, default: Optional[int] = None
) -> int:
    value = _try_parse_attribute(elements, key)
    return _coerce_value(int, value, default)


def parse_attribute_float(
    elements: Sequence[HtmlElement], key: str, default: Optional[float] = None
) -> float:
    value = _try_parse_attribute(elements, key)
    return _coerce_value(float, value, default)
