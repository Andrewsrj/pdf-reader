from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from domain.models import ExtractedItem, ExtractionError


class ExcelExporter:
    """Persist extracted data into the required workbook sheets."""

    def export(
        self,
        output_path: Path,
        items: Iterable[ExtractedItem],
        errors: Iterable[ExtractionError],
    ) -> None:
        _ = output_path
        _ = list(items)
        _ = list(errors)
        raise NotImplementedError("Excel export will be implemented after the parser milestone.")
