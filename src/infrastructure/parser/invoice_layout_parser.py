from __future__ import annotations

from dataclasses import dataclass, field

from infrastructure.parser.city_parser import parse_city
from infrastructure.parser.item_line_parser import parse_item_line


@dataclass(slots=True)
class ParsedInvoice:
    city: str | None = None
    item_count: int = 0
    notes: list[str] = field(default_factory=list)


class InvoiceLayoutParser:
    """High-level parser that coordinates city and item extraction."""

    def parse(self, lines: list[str], pdf_filename: str) -> ParsedInvoice:
        city = parse_city("\n".join(lines))
        item_count = sum(1 for line in lines if parse_item_line(line, pdf_filename) is not None)
        return ParsedInvoice(city=city, item_count=item_count)
