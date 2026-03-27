from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation


_NON_NUMERIC_PATTERN = re.compile(r"[^\d,.-]")
_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_whitespace(value: str | None) -> str:
    if value is None:
        return ""
    return _WHITESPACE_PATTERN.sub(" ", value).strip()


def parse_brazilian_decimal(value: str | None) -> Decimal | None:
    normalized = normalize_whitespace(value)
    if not normalized:
        return None

    sanitized = _NON_NUMERIC_PATTERN.sub("", normalized)
    sanitized = sanitized.replace(".", "").replace(",", ".")

    if sanitized in {"", "-", ".", "-."}:
        return None

    try:
        return Decimal(sanitized)
    except InvalidOperation:
        return None


def parse_brazilian_currency(value: str | None) -> Decimal | None:
    return parse_brazilian_decimal(value)
