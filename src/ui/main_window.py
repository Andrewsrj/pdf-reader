from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QThreadPool
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

from application.extraction_service import InvoiceBatchProcessor, discover_pdf_files
from domain.models import BatchExtractionResult
from infrastructure.export.excel_exporter import ExcelExporter
from ui.dialogs import choose_input_folder, choose_output_file
from ui.workers import BackgroundTaskWorker


class MainWindow(QMainWindow):
    """Initial main window for the invoice extraction workflow."""

    def __init__(self) -> None:
        super().__init__()
        self._selected_folder: Path | None = None
        self._pdf_files: list[Path] = []
        self._thread_pool = QThreadPool.globalInstance()
        self._active_worker: BackgroundTaskWorker | None = None
        self._last_result: BatchExtractionResult | None = None

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
            "O processamento roda em segundo plano com OCR e parser de itens."
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

        processor = InvoiceBatchProcessor()
        self.progress_bar.setValue(0)
        self.status_label.setText("Iniciando o processamento em segundo plano...")
        self._set_processing_state(True)

        worker = BackgroundTaskWorker(
            lambda emit_progress: processor.extract_batch(self._pdf_files, progress_callback=emit_progress)
        )
        worker.signals.started.connect(self._on_extraction_started)
        worker.signals.progress.connect(self._on_extraction_progress)
        worker.signals.finished.connect(self._on_extraction_finished)
        worker.signals.failed.connect(self._on_extraction_failed)

        self._active_worker = worker
        self._thread_pool.start(worker)

    def _on_extraction_started(self) -> None:
        self.status_label.setText("Renderizando PDFs e preparando o OCR...")

    def _on_extraction_progress(self, update: object) -> None:
        if not hasattr(update, "percent") or not hasattr(update, "message"):
            return

        self.progress_bar.setValue(int(update.percent))
        self.status_label.setText(str(update.message))

    def _on_extraction_finished(self, result: object) -> None:
        self._active_worker = None
        self._set_processing_state(False)

        if not isinstance(result, BatchExtractionResult):
            QMessageBox.warning(self, "Resultado invalido", "O worker retornou um resultado inesperado.")
            return

        self._last_result = result
        self.progress_bar.setValue(100)
        self.status_label.setText("Extracao concluida. Escolha onde salvar o Excel.")

        output_file = choose_output_file(self, self._default_output_filename())
        if not output_file:
            self.status_label.setText("Extracao concluida. Salvamento do Excel cancelado.")
            QMessageBox.information(
                self,
                "Salvamento cancelado",
                (
                    f"A extracao foi concluida com {result.total_items} item(ns) e "
                    f"{result.total_summary_rows} grupo(s), mas o arquivo Excel nao foi salvo."
                ),
            )
            return

        try:
            output_path = ExcelExporter().export_batch(Path(output_file), result)
        except Exception as exc:
            self.status_label.setText("Extracao concluida, mas a exportacao falhou.")
            QMessageBox.critical(self, "Falha na exportacao", str(exc))
            return

        self.status_label.setText(
            f"Excel salvo com sucesso em {output_path.name}. "
            f"{result.total_summary_rows} grupo(s) consolidados."
        )
        QMessageBox.information(
            self,
            "Extracao e exportacao concluidas",
            (
                f"Arquivos processados: {result.total_files}\n"
                f"Sucessos: {result.succeeded}\n"
                f"Parciais: {result.partial}\n"
                f"Falhas: {result.failed}\n"
                f"Itens extraidos: {result.total_items}\n"
                f"Grupos cidade/item: {result.total_summary_rows}\n"
                f"Arquivo gerado: {output_path}"
            ),
        )

    def _on_extraction_failed(self, message: str) -> None:
        self._active_worker = None
        self._set_processing_state(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("O processamento falhou.")
        QMessageBox.critical(self, "Falha na extracao", message)

    def _update_ui_state(self) -> None:
        total_pdfs = len(self._pdf_files)
        self.pdf_count_label.setText(f"{total_pdfs} PDF(s) encontrado(s)")

        if self._selected_folder is None:
            self.status_label.setText("Selecione uma pasta para comecar.")
        elif total_pdfs == 0:
            self.status_label.setText("A pasta selecionada nao contem arquivos PDF.")
        else:
            self.status_label.setText("Pasta validada. O lote esta pronto para extracao.")

        self.extract_button.setEnabled(total_pdfs > 0)

    def _set_processing_state(self, is_processing: bool) -> None:
        self.select_folder_button.setEnabled(not is_processing)
        self.extract_button.setEnabled(not is_processing and bool(self._pdf_files))

    def _default_output_filename(self) -> str:
        if self._selected_folder is not None:
            return f"relatorio_{self._selected_folder.name}.xlsx"
        return "relatorio_notas.xlsx"
