from __future__ import annotations

from pathlib import Path


def discover_pdf_files(folder_path: Path) -> list[Path]:
    """Return the direct child PDF files from the selected folder."""
    if not folder_path.exists():
        raise ValueError(f"A pasta informada nao existe: {folder_path}")

    if not folder_path.is_dir():
        raise ValueError(f"O caminho informado nao e uma pasta: {folder_path}")

    return sorted(
        (path for path in folder_path.iterdir() if path.is_file() and path.suffix.lower() == ".pdf"),
        key=lambda path: path.name.lower(),
    )
