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
    city: str | None = None
    document_number: str | None = None
    issue_date: date | None = None
    items: list[ExtractedItem] = field(default_factory=list)
    errors: list[ExtractionError] = field(default_factory=list)
    raw_lines: list[str] = field(default_factory=list)

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def status(self) -> str:
        if self.items and not self.errors:
            return "sucesso"
        if self.items:
            return "parcial"
        return "falha"


@dataclass(slots=True)
class BatchExtractionResult:
    results: list[InvoiceExtractionResult] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.results)

    @property
    def succeeded(self) -> int:
        return sum(1 for result in self.results if result.status == "sucesso")

    @property
    def partial(self) -> int:
        return sum(1 for result in self.results if result.status == "parcial")

    @property
    def failed(self) -> int:
        return sum(1 for result in self.results if result.status == "falha")

    @property
    def total_items(self) -> int:
        return sum(len(result.items) for result in self.results)
