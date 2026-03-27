from __future__ import annotations

from pathlib import Path


class PdfMetadataReader:
    """Read lightweight metadata from a PDF file."""

    def read(self, pdf_path: Path) -> dict[str, str]:
        raise NotImplementedError("PDF metadata reading will be implemented in a later step.")
