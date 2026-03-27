from __future__ import annotations

from domain.models import ExtractedItem


def parse_item_line(line: str, pdf_filename: str) -> ExtractedItem | None:
    """Return None until the invoice item parsing rules are defined."""
    _ = line
    _ = pdf_filename
    return None
