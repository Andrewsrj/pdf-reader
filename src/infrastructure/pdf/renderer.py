from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any


class PdfRenderer:
    """Render PDF pages into OCR-ready image objects."""

    def render(self, pdf_path: Path) -> Sequence[Any]:
        raise NotImplementedError("PDF rendering will be implemented in the OCR pipeline phase.")
