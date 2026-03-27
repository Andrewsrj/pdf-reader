from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytesseract
from PIL import Image

from app.runtime_paths import get_runtime_search_roots
from domain.normalizers import normalize_whitespace
from infrastructure.ocr.image_preprocessor import preprocess_image


class TesseractOcrEngine:
    """OCR adapter backed by a local Tesseract installation."""

    def __init__(
        self,
        tesseract_cmd: str | None = None,
        tessdata_dir: str | Path | None = None,
        preferred_languages: Sequence[str] = ("por", "eng"),
    ) -> None:
        self._tesseract_cmd = tesseract_cmd or self._detect_tesseract_cmd()
        self._tessdata_dir = self._detect_tessdata_dir(tessdata_dir)
        pytesseract.pytesseract.tesseract_cmd = self._tesseract_cmd
        self._available_languages = self._list_available_languages()
        self._language = self._select_language(preferred_languages, self._available_languages)

    @property
    def language(self) -> str:
        return self._language

    @property
    def tessdata_dir(self) -> Path:
        return self._tessdata_dir

    def extract_lines(self, images: Sequence[Image.Image]) -> list[str]:
        lines: list[str] = []

        for image in images:
            processed_image = preprocess_image(image)
            text = pytesseract.image_to_string(
                processed_image,
                lang=self._language,
                config=self._build_config("--oem 3"),
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

    def _detect_tessdata_dir(self, tessdata_dir: str | Path | None) -> Path:
        runtime_roots = get_runtime_search_roots()
        bundled_candidates = [
            root / "resources" / "tessdata"
            for root in runtime_roots
        ] + [
            root / "tessdata"
            for root in runtime_roots
        ]
        explicit_candidates = [
            Path(tessdata_dir) if tessdata_dir is not None else None,
            Path(os.environ["PDF_READER_TESSDATA_DIR"]) if os.getenv("PDF_READER_TESSDATA_DIR") else None,
            Path(os.environ["TESSDATA_PREFIX"]) if os.getenv("TESSDATA_PREFIX") else None,
            *bundled_candidates,
            runtime_roots[0] / "artifacts" / "tessdata",
            Path(self._tesseract_cmd).resolve().parent / "tessdata",
        ]

        for candidate in explicit_candidates:
            resolved_candidate = self._resolve_tessdata_candidate(candidate)
            if resolved_candidate is not None:
                return resolved_candidate

        raise RuntimeError(
            "Nao foi possivel localizar um diretorio tessdata com idiomas instalados. "
            "Defina PDF_READER_TESSDATA_DIR ou adicione arquivos .traineddata em resources/tessdata."
        )

    def _resolve_tessdata_candidate(self, candidate: Path | None) -> Path | None:
        if candidate is None:
            return None

        candidate = candidate.expanduser()
        for path_option in (candidate, candidate / "tessdata"):
            if path_option.exists() and path_option.is_dir() and any(path_option.glob("*.traineddata")):
                return path_option.resolve()

        return None

    def _list_available_languages(self) -> set[str]:
        completed = subprocess.run(
            [self._tesseract_cmd, "--tessdata-dir", str(self._tessdata_dir), "--list-langs"],
            capture_output=True,
            text=True,
            check=True,
        )

        return {
            normalize_whitespace(line)
            for line in completed.stdout.splitlines()
            if normalize_whitespace(line) and "List of available languages" not in line
        }

    def _select_language(self, preferred_languages: Sequence[str], available_languages: set[str]) -> str:
        selected_languages = [
            language
            for language in preferred_languages
            if language in available_languages
        ]

        if selected_languages:
            return "+".join(selected_languages)

        if available_languages:
            return sorted(available_languages)[0]

        raise RuntimeError("O Tesseract foi encontrado, mas nao possui idiomas instalados.")

    def _build_config(self, base_config: str) -> str:
        return f"--tessdata-dir {self._tessdata_dir} {base_config}".strip()
