from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


_NON_NUMERIC_PATTERN = re.compile(r"[^\d,.-]")
_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_whitespace(value: str | None) -> str:
    if value is None:
        return ""
    return _WHITESPACE_PATTERN.sub(" ", value).strip()


def normalize_for_matching(value: str | None) -> str:
    normalized = normalize_whitespace(value)
    if not normalized:
        return ""

    ascii_text = (
        unicodedata.normalize("NFKD", normalized)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    return ascii_text.upper()


def parse_brazilian_decimal(value: str | None) -> Decimal | None:
    normalized = normalize_whitespace(value)
    if not normalized:
        return None

    sanitized = _NON_NUMERIC_PATTERN.sub("", normalized)
    if not sanitized:
        return None

    sign = ""
    if sanitized.startswith("-"):
        sign = "-"
        sanitized = sanitized[1:]

    if sanitized in {"", ".", ","}:
        return None

    last_comma = sanitized.rfind(",")
    last_dot = sanitized.rfind(".")

    if last_comma == -1 and last_dot == -1:
        canonical = sanitized
    else:
        decimal_separator = "," if last_comma > last_dot else "."
        decimal_index = sanitized.rfind(decimal_separator)
        integer_part = sanitized[:decimal_index].replace(",", "").replace(".", "")
        decimal_part = sanitized[decimal_index + 1 :]
        canonical = integer_part

        if decimal_part:
            canonical = f"{canonical}.{decimal_part}"

    try:
        return Decimal(f"{sign}{canonical}")
    except InvalidOperation:
        return None


def parse_brazilian_currency(value: str | None) -> Decimal | None:
    return parse_brazilian_decimal(value)


def parse_brazilian_date(value: str | None) -> date | None:
    normalized = normalize_whitespace(value)
    if not normalized:
        return None

    try:
        return datetime.strptime(normalized, "%d/%m/%Y").date()
    except ValueError:
        return None
