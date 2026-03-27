from __future__ import annotations

from collections.abc import Sequence
from typing import Any


class TesseractOcrEngine:
    """OCR adapter placeholder for a local Tesseract installation."""

    def extract_lines(self, images: Sequence[Any]) -> list[str]:
        raise NotImplementedError("OCR extraction will be implemented in the next milestone.")
