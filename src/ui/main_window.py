from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from application.extraction_service import discover_pdf_files
from ui.dialogs import choose_input_folder


class MainWindow(QMainWindow):
    """Initial main window for the invoice extraction workflow."""

    def __init__(self) -> None:
        super().__init__()
        self._selected_folder: Path | None = None
        self._pdf_files: list[Path] = []

        self.setWindowTitle("Extrator de Notas Fiscais em PDF")
        self.resize(760, 320)

        self._build_ui()
        self._update_ui_state()

    def _build_ui(self) -> None:
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        title = QLabel("Extrair itens de notas fiscais em PDF")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        description = QLabel(
            "Selecione a pasta de entrada para preparar o lote. "
            "A infraestrutura inicial do aplicativo ja esta pronta para receber o pipeline de OCR."
        )
        description.setWordWrap(True)

        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(12)

        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.setPlaceholderText("Nenhuma pasta selecionada")

        self.select_folder_button = QPushButton("Selecionar pasta")
        self.select_folder_button.clicked.connect(self._on_select_folder_clicked)

        folder_layout.addWidget(self.folder_path_edit, stretch=1)
        folder_layout.addWidget(self.select_folder_button)

        self.pdf_count_label = QLabel("0 PDFs encontrados")
        self.status_label = QLabel("Selecione uma pasta para comecar.")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        actions_layout = QHBoxLayout()
        actions_layout.addStretch(1)

        self.extract_button = QPushButton("Extrair")
        self.extract_button.clicked.connect(self._on_extract_clicked)
        actions_layout.addWidget(self.extract_button)

        root_layout.addWidget(title)
        root_layout.addWidget(description)
        root_layout.addLayout(folder_layout)
        root_layout.addWidget(self.pdf_count_label)
        root_layout.addWidget(self.progress_bar)
        root_layout.addWidget(self.status_label)
        root_layout.addStretch(1)
        root_layout.addLayout(actions_layout)

    def _on_select_folder_clicked(self) -> None:
        selected_folder = choose_input_folder(self)
        if not selected_folder:
            return

        folder_path = Path(selected_folder)

        try:
            pdf_files = discover_pdf_files(folder_path)
        except ValueError as exc:
            QMessageBox.warning(self, "Pasta invalida", str(exc))
            return

        self._selected_folder = folder_path
        self._pdf_files = pdf_files
        self.folder_path_edit.setText(str(folder_path))
        self.progress_bar.setValue(0)
        self._update_ui_state()

    def _on_extract_clicked(self) -> None:
        if not self._pdf_files:
            QMessageBox.information(
                self,
                "Nenhum PDF encontrado",
                "Selecione uma pasta com ao menos um arquivo PDF antes de iniciar.",
            )
            return

        self.status_label.setText(
            "Estrutura inicial pronta. O worker de extracao, OCR, parser e exportacao "
            "sera conectado na proxima etapa."
        )
        QMessageBox.information(
            self,
            "Base pronta",
            (
                f"{len(self._pdf_files)} PDF(s) localizado(s). "
                "A janela principal e a descoberta de arquivos ja estao implementadas."
            ),
        )

    def _update_ui_state(self) -> None:
        total_pdfs = len(self._pdf_files)
        self.pdf_count_label.setText(f"{total_pdfs} PDF(s) encontrado(s)")

        if self._selected_folder is None:
            self.status_label.setText("Selecione uma pasta para comecar.")
        elif total_pdfs == 0:
            self.status_label.setText("A pasta selecionada nao contem arquivos PDF.")
        else:
            self.status_label.setText("Pasta validada. O lote esta pronto para a proxima etapa.")

        self.extract_button.setEnabled(total_pdfs > 0)
