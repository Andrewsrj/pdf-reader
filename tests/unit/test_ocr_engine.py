from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

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
