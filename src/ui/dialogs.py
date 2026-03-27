from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QWidget


def choose_input_folder(parent: QWidget) -> str:
    """Open a dialog to select the PDF input folder."""
    return QFileDialog.getExistingDirectory(parent, "Selecionar pasta com PDFs")


def choose_output_file(parent: QWidget, default_name: str = "relatorio_notas.xlsx") -> str:
    """Open a dialog to choose the Excel output file."""
    filename, _ = QFileDialog.getSaveFileName(
        parent,
        "Salvar relatorio Excel",
        default_name,
        "Arquivos Excel (*.xlsx)",
    )
    return filename
