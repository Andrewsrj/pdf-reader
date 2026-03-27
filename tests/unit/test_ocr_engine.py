from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from app.user_settings import UserSettings
from infrastructure.ocr.ocr_engine import TesseractOcrEngine


def test_ocr_engine_prefers_portuguese_and_english_combo_when_both_exist() -> None:
    with (
        patch.object(TesseractOcrEngine, "_detect_tesseract_cmd", return_value="tesseract"),
        patch.object(TesseractOcrEngine, "_detect_tessdata_dir", return_value=Path("tessdata")),
        patch.object(TesseractOcrEngine, "_list_available_languages", return_value={"eng", "por"}),
    ):
        engine = TesseractOcrEngine()

    assert engine.language == "por+eng"


def test_ocr_engine_uses_configured_tessdata_dir_from_environment() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        tessdata_dir = Path(temp_dir)
        (tessdata_dir / "por.traineddata").write_bytes(b"test")

        with (
            patch.dict(os.environ, {"PDF_READER_TESSDATA_DIR": str(tessdata_dir)}, clear=False),
            patch.object(TesseractOcrEngine, "_detect_tesseract_cmd", return_value="tesseract"),
            patch.object(TesseractOcrEngine, "_list_available_languages", return_value={"por"}),
        ):
            engine = TesseractOcrEngine()

        assert engine.tessdata_dir == tessdata_dir.resolve()
        assert engine.language == "por"


def test_ocr_engine_uses_saved_tesseract_cmd_before_system_detection() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        configured_executable = Path(temp_dir) / "tesseract.exe"
        configured_executable.write_text("", encoding="utf-8")

        with (
            patch("infrastructure.ocr.ocr_engine.load_user_settings", return_value=UserSettings(tesseract_cmd=str(configured_executable))),
            patch.object(TesseractOcrEngine, "_detect_tessdata_dir", return_value=Path("tessdata")),
            patch.object(TesseractOcrEngine, "_list_available_languages", return_value={"por"}),
        ):
            engine = TesseractOcrEngine()

        assert Path(engine.tesseract_cmd) == configured_executable


def test_ocr_engine_detects_bundled_vendor_tesseract() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        runtime_root = Path(temp_dir)
        bundled_executable = runtime_root / "vendor" / "tesseract" / "tesseract.exe"
        bundled_executable.parent.mkdir(parents=True, exist_ok=True)
        bundled_executable.write_text("", encoding="utf-8")

        with (
            patch("infrastructure.ocr.ocr_engine.load_user_settings", return_value=UserSettings()),
            patch("infrastructure.ocr.ocr_engine.get_runtime_search_roots", return_value=[runtime_root]),
            patch.object(TesseractOcrEngine, "_detect_tessdata_dir", return_value=Path("tessdata")),
            patch.object(TesseractOcrEngine, "_list_available_languages", return_value={"por"}),
        ):
            engine = TesseractOcrEngine()

        assert Path(engine.tesseract_cmd) == bundled_executable
