from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import fitz
from PIL import Image


@dataclass(slots=True)
class RenderedPage:
    page_number: int
    image: Image.Image


class PdfRenderer:
    """Render PDF pages into OCR-ready image objects."""

    def __init__(self, dpi: int = 250) -> None:
        self._dpi = dpi

    def render(self, pdf_path: Path) -> list[RenderedPage]:
        zoom = self._dpi / 72
        pages: list[RenderedPage] = []

        with fitz.open(pdf_path) as document:
            for page_number, page in enumerate(document, start=1):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
                image = Image.open(io.BytesIO(pixmap.tobytes("png")))
                image.load()
                pages.append(RenderedPage(page_number=page_number, image=image))

        return pages
