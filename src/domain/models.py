from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from pathlib import Path


@dataclass(slots=True)
class ExtractedItem:
    pdf_filename: str
    extraction_status: str
    city: str | None = None
    document_number: str | None = None
    issue_date: date | None = None
    item_description: str | None = None
    item_quantity: Decimal | None = None
    item_total_value: Decimal | None = None
    notes: str | None = None


@dataclass(slots=True)
class ExtractionError:
    pdf_filename: str
    error_type: str
    message: str
    stage: str | None = None


@dataclass(slots=True)
class InvoiceExtractionResult:
    pdf_path: Path
    items: list[ExtractedItem] = field(default_factory=list)
    errors: list[ExtractionError] = field(default_factory=list)

    @property
    def has_items(self) -> bool:
        return bool(self.items)
