from pathlib import Path

import pytest

from application.extraction_service import discover_pdf_files


def test_discover_pdf_files_returns_sorted_pdf_files_only(tmp_path: Path) -> None:
    (tmp_path / "b.pdf").write_text("", encoding="utf-8")
    (tmp_path / "A.PDF").write_text("", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("", encoding="utf-8")

    pdf_files = discover_pdf_files(tmp_path)

    assert [path.name for path in pdf_files] == ["A.PDF", "b.pdf"]


def test_discover_pdf_files_rejects_missing_folder(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing"

    with pytest.raises(ValueError, match="nao existe"):
        discover_pdf_files(missing_path)
