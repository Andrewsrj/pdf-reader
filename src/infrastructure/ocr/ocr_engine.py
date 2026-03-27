from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytesseract
from PIL import Image

from domain.normalizers import normalize_whitespace
from infrastructure.ocr.image_preprocessor import preprocess_image


class TesseractOcrEngine:
    """OCR adapter backed by a local Tesseract installation."""

    def __init__(
        self,
        tesseract_cmd: str | None = None,
        preferred_languages: Sequence[str] = ("por", "eng"),
    ) -> None:
        self._tesseract_cmd = tesseract_cmd or self._detect_tesseract_cmd()
        pytesseract.pytesseract.tesseract_cmd = self._tesseract_cmd
        self._language = self._select_language(preferred_languages)

    def extract_lines(self, images: Sequence[Image.Image]) -> list[str]:
        lines: list[str] = []

        for image in images:
            processed_image = preprocess_image(image)
            text = pytesseract.image_to_string(
                processed_image,
                lang=self._language,
                config="--oem 3",
            )
            lines.extend(
                normalize_whitespace(line)
                for line in text.splitlines()
                if normalize_whitespace(line)
            )

        return [line for line in lines if line]

    def _detect_tesseract_cmd(self) -> str:
        candidates = [
            os.getenv("TESSERACT_CMD"),
            shutil.which("tesseract"),
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.join(os.getenv("LOCALAPPDATA", ""), "Programs", "Tesseract-OCR", "tesseract.exe"),
        ]

        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return str(candidate)

        raise RuntimeError(
            "Nao foi possivel localizar o Tesseract OCR. Defina TESSERACT_CMD ou instale o executavel localmente."
        )

    def _select_language(self, preferred_languages: Sequence[str]) -> str:
        completed = subprocess.run(
            [self._tesseract_cmd, "--list-langs"],
            capture_output=True,
            text=True,
            check=True,
        )

        available_languages = {
            normalize_whitespace(line)
            for line in completed.stdout.splitlines()
            if normalize_whitespace(line) and "List of available languages" not in line
        }

        for language in preferred_languages:
            if language in available_languages:
                return language

        if available_languages:
            return sorted(available_languages)[0]

        raise RuntimeError("O Tesseract foi encontrado, mas nao possui idiomas instalados.")
