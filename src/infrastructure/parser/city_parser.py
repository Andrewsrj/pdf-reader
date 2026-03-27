from __future__ import annotations

from collections.abc import Sequence
import re

from domain.normalizers import normalize_for_matching, normalize_whitespace


_STATE_PATTERN = r"(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)"
_CITY_IN_LINE_PATTERN = re.compile(rf"(?P<city>[A-Z][A-Z\s]+?)\s+{_STATE_PATTERN}\b")
_LOCAL_DELIVERY_PATTERN = re.compile(rf"LOCAL DE ENTREGA:.*?-\s*(?P<city>[A-Z][A-Z\s]+)-{_STATE_PATTERN}\b")


def parse_city(text: str | Sequence[str]) -> str | None:
    lines = text.splitlines() if isinstance(text, str) else list(text)

    for index, line in enumerate(lines):
        if "MUNICIPIO" not in normalize_for_matching(line):
            continue

        for candidate in lines[index + 1 : index + 4]:
            city = _extract_city_from_line(candidate)
            if city:
                return city

    for line in lines:
        normalized_line = normalize_for_matching(line)
        match = _LOCAL_DELIVERY_PATTERN.search(normalized_line)
        if match:
            return normalize_whitespace(match.group("city"))

    return None


def _extract_city_from_line(line: str) -> str | None:
    normalized_line = normalize_for_matching(line)
    match = _CITY_IN_LINE_PATTERN.search(normalized_line)
    if not match:
        return None

    return normalize_whitespace(match.group("city"))
