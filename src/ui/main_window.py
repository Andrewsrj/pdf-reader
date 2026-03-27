from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QThreadPool, QUrl
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from application.extraction_service import InvoiceBatchProcessor, discover_pdf_files
from domain.models import BatchExtractionResult
from infrastructure.export.excel_exporter import ExcelExporter
from ui.about_dialog import AboutDialog, REPOSITORY_URL
from ui.dialogs import choose_input_folder, choose_output_file
from ui.view_state import (
    build_completion_message,
    build_dashboard_metrics,
    build_export_cancelled_message,
    build_folder_status_text,
    build_latest_run_summary,
)
from ui.workers import BackgroundTaskWorker


class MetricCard(QFrame):
    def __init__(self, title: str, accent_color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("metricCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(6)

        self.value_label = QLabel("0")
        self.value_label.setObjectName("metricValue")
        self.value_label.setStyleSheet(f"color: {accent_color};")

        self.title_label = QLabel(title)
        self.title_label.setObjectName("metricTitle")

        self.description_label = QLabel("")
        self.description_label.setObjectName("metricDescription")
        self.description_label.setWordWrap(True)

        layout.addWidget(self.value_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addStretch(1)

    def update_metric(self, value: int, description: str) -> None:
        self.value_label.setText(str(value))
        self.description_label.setText(description)


class MainWindow(QMainWindow):
    """Main desktop window for the invoice extraction workflow."""

    def __init__(self) -> None:
        super().__init__()
        self._selected_folder: Path | None = None
        self._pdf_files: list[Path] = []
        self._thread_pool = QThreadPool.globalInstance()
        self._active_worker: BackgroundTaskWorker | None = None
        self._last_result: BatchExtractionResult | None = None
        self._last_output_path: Path | None = None

        self.setWindowTitle("Extrator de Notas Fiscais em PDF")
        self.resize(980, 720)
        self.setMinimumSize(900, 620)

        self._build_menu()
        self._build_ui()
        self._update_ui_state()

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("Arquivo")

        select_folder_action = QAction("Selecionar pasta...", self)
        select_folder_action.setShortcut("Ctrl+O")
        select_folder_action.triggered.connect(self._on_select_folder_clicked)

        self.export_again_action = QAction("Exportar ultimo resultado...", self)
        self.export_again_action.setShortcut("Ctrl+S")
        self.export_again_action.triggered.connect(self._on_export_again_clicked)

        exit_action = QAction("Sair", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(select_folder_action)
        file_menu.addAction(self.export_again_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu = self.menuBar().addMenu("Ajuda")

        about_action = QAction("Sobre o autor", self)
        about_action.triggered.connect(self._show_about_dialog)

        repository_action = QAction("Abrir repositorio no GitHub", self)
        repository_action.triggered.connect(self._open_repository_url)

        help_menu.addAction(about_action)
        help_menu.addAction(repository_action)

    def _build_ui(self) -> None:
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        page = QWidget(self)
        page.setObjectName("appPage")
        scroll_area.setWidget(page)
        self.setCentralWidget(scroll_area)

        root_layout = QVBoxLayout(page)
        root_layout.setContentsMargins(28, 28, 28, 28)
        root_layout.setSpacing(18)

        root_layout.addWidget(self._build_workspace_card())
        root_layout.addLayout(self._build_metrics_grid())
        root_layout.addWidget(self._build_progress_card())
        root_layout.addLayout(self._build_actions_row())
        root_layout.addStretch(1)

    def _build_workspace_card(self) -> QFrame:
        card = QFrame(self)
        card.setObjectName("panelCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Pasta de entrada")
        title.setObjectName("sectionTitle")

        description = QLabel(
            "Selecione a pasta que contem as notas fiscais. O app identifica os PDFs, "
            "prepara o lote e deixa a extracao pronta para um clique."
        )
        description.setObjectName("sectionDescription")
        description.setWordWrap(True)

        folder_row = QHBoxLayout()
        folder_row.setSpacing(12)

        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setObjectName("folderPathEdit")
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.setPlaceholderText("Nenhuma pasta selecionada")

        self.select_folder_button = QPushButton("Selecionar pasta")
        self.select_folder_button.setObjectName("secondaryButton")
        self.select_folder_button.clicked.connect(self._on_select_folder_clicked)

        folder_row.addWidget(self.folder_path_edit, stretch=1)
        folder_row.addWidget(self.select_folder_button)

        meta_row = QHBoxLayout()
        meta_row.setSpacing(12)

        self.folder_count_label = QLabel("0 PDF(s) no lote")
        self.folder_count_label.setObjectName("folderCounter")

        self.folder_status_label = QLabel("")
        self.folder_status_label.setObjectName("subtleLabel")
        self.folder_status_label.setWordWrap(True)

        meta_row.addWidget(self.folder_count_label)
        meta_row.addWidget(self.folder_status_label, stretch=1)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(folder_row)
        layout.addLayout(meta_row)

        return card

    def _build_metrics_grid(self) -> QGridLayout:
        layout = QGridLayout()
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(16)

        self.pdf_metric_card = MetricCard("PDFs no lote", "#d27a42")
        self.items_metric_card = MetricCard("Itens do ultimo lote", "#245b49")
        self.groups_metric_card = MetricCard("Grupos consolidados", "#244d7a")
        self.failures_metric_card = MetricCard("Falhas do ultimo lote", "#a5452b")

        layout.addWidget(self.pdf_metric_card, 0, 0)
        layout.addWidget(self.items_metric_card, 0, 1)
        layout.addWidget(self.groups_metric_card, 1, 0)
        layout.addWidget(self.failures_metric_card, 1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        return layout

    def _build_progress_card(self) -> QFrame:
        card = QFrame(self)
        card.setObjectName("panelCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        status_title = QLabel("Status do processamento")
        status_title.setObjectName("statusTitle")

        self.status_badge = QLabel("Aguardando lote")
        self.status_badge.setObjectName("statusBadge")
        self.status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_row.addWidget(status_title)
        header_row.addStretch(1)
        header_row.addWidget(self.status_badge)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p% concluido")

        self.status_label = QLabel("Selecione uma pasta para comecar.")
        self.status_label.setObjectName("statusMessage")
        self.status_label.setWordWrap(True)

        self.summary_label = QLabel(build_latest_run_summary(None))
        self.summary_label.setObjectName("summaryLabel")
        self.summary_label.setWordWrap(True)

        layout.addLayout(header_row)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.summary_label)

        return card

    def _build_actions_row(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.about_button = QPushButton("Sobre o autor")
        self.about_button.setObjectName("ghostButton")
        self.about_button.clicked.connect(self._show_about_dialog)

        self.export_again_button = QPushButton("Exportar ultimo resultado")
        self.export_again_button.setObjectName("ghostButton")
        self.export_again_button.clicked.connect(self._on_export_again_clicked)

        self.extract_button = QPushButton("Extrair agora")
        self.extract_button.setObjectName("primaryButton")
        self.extract_button.clicked.connect(self._on_extract_clicked)
        self.extract_button.setDefault(True)

        layout.addWidget(self.about_button)
        layout.addStretch(1)
        layout.addWidget(self.export_again_button)
        layout.addWidget(self.extract_button)

        return layout

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
        self._last_output_path = None
        self.progress_bar.setValue(0)
        self.status_label.setText("Iniciando o processamento em segundo plano...")
        self.summary_label.setText(build_latest_run_summary(self._last_result))
        self._set_status_badge("OCR em andamento", "processing")
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

    def _on_export_again_clicked(self) -> None:
        if self._last_result is None:
            QMessageBox.information(
                self,
                "Nenhum resultado disponivel",
                "Execute ao menos um lote antes de exportar novamente o Excel.",
            )
            return

        self._export_result(self._last_result, show_cancel_message=False)

    def _show_about_dialog(self) -> None:
        dialog = AboutDialog(self)
        dialog.exec()

    def _open_repository_url(self) -> None:
        if not QDesktopServices.openUrl(QUrl(REPOSITORY_URL)):
            QMessageBox.warning(
                self,
                "Nao foi possivel abrir o link",
                f"Abra manualmente o repositorio em {REPOSITORY_URL}.",
            )

    def _on_extraction_started(self) -> None:
        self.status_label.setText("Renderizando paginas e preparando o OCR...")
        self._set_status_badge("Processando", "processing")

    def _on_extraction_progress(self, update: object) -> None:
        if not hasattr(update, "percent") or not hasattr(update, "message"):
            return

        self.progress_bar.setValue(int(update.percent))
        self.status_label.setText(str(update.message))

    def _on_extraction_finished(self, result: object) -> None:
        self._active_worker = None
        self._set_processing_state(False)

        if not isinstance(result, BatchExtractionResult):
            self._set_status_badge("Resultado invalido", "error")
            QMessageBox.warning(self, "Resultado invalido", "O worker retornou um resultado inesperado.")
            return

        self._last_result = result
        self.progress_bar.setValue(100)
        self._update_metrics()
        self._update_export_actions()

        if result.failed > 0 or result.partial > 0:
            self._set_status_badge("Concluido com alertas", "warning")
        else:
            self._set_status_badge("Lote concluido", "success")

        self.status_label.setText("Extracao concluida. Escolha onde salvar o Excel.")
        self.summary_label.setText(build_latest_run_summary(result))
        self._export_result(result, show_cancel_message=True)

    def _on_extraction_failed(self, message: str) -> None:
        self._active_worker = None
        self._set_processing_state(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("O processamento falhou.")
        self._set_status_badge("Falha na extracao", "error")
        QMessageBox.critical(self, "Falha na extracao", message)

    def _export_result(self, result: BatchExtractionResult, *, show_cancel_message: bool) -> Path | None:
        output_file = choose_output_file(self, self._default_output_filename())
        if not output_file:
            self.status_label.setText("Extracao concluida. Salvamento do Excel cancelado.")
            self.summary_label.setText(build_latest_run_summary(result))
            if show_cancel_message:
                QMessageBox.information(
                    self,
                    "Salvamento cancelado",
                    build_export_cancelled_message(result),
                )
            return None

        try:
            output_path = ExcelExporter().export_batch(Path(output_file), result)
        except Exception as exc:
            self.status_label.setText("Extracao concluida, mas a exportacao falhou.")
            self._set_status_badge("Falha na exportacao", "error")
            QMessageBox.critical(self, "Falha na exportacao", str(exc))
            return None

        self._last_output_path = output_path
        self.status_label.setText(
            f"Excel salvo com sucesso em {output_path.name}. "
            f"{result.total_summary_rows} grupo(s) consolidados."
        )
        self.summary_label.setText(build_latest_run_summary(result, output_path))
        self._set_status_badge("Excel exportado", "success")
        QMessageBox.information(
            self,
            "Extracao e exportacao concluidas",
            build_completion_message(result, output_path),
        )
        return output_path

    def _update_ui_state(self) -> None:
        total_pdfs = len(self._pdf_files)
        self.folder_count_label.setText(f"{total_pdfs} PDF(s) no lote")
        self.folder_status_label.setText(build_folder_status_text(self._selected_folder, total_pdfs))
        self._update_metrics()
        self._update_export_actions()

        if self._selected_folder is None:
            self.status_label.setText("Selecione uma pasta para comecar.")
            self._set_status_badge("Aguardando lote", "idle")
        elif total_pdfs == 0:
            self.status_label.setText("A pasta selecionada nao contem arquivos PDF.")
            self._set_status_badge("Nenhum PDF encontrado", "warning")
        else:
            self.status_label.setText("Pasta validada. Clique em Extrair agora para iniciar o OCR.")
            self._set_status_badge("Lote pronto", "ready")

        self.summary_label.setText(build_latest_run_summary(self._last_result, self._last_output_path))
        self.extract_button.setEnabled(total_pdfs > 0)

    def _update_metrics(self) -> None:
        metrics = build_dashboard_metrics(len(self._pdf_files), self._last_result)

        self.pdf_metric_card.update_metric(
            metrics.total_pdfs,
            "Arquivos prontos na pasta atualmente selecionada.",
        )
        self.items_metric_card.update_metric(
            metrics.extracted_items,
            "Linhas extraidas no ultimo lote executado.",
        )
        self.groups_metric_card.update_metric(
            metrics.grouped_rows,
            "Agrupamentos cidade + item gerados por OCR e parser.",
        )
        self.failures_metric_card.update_metric(
            metrics.failed_files,
            "Arquivos que exigem revisao manual no ultimo lote.",
        )

    def _update_export_actions(self) -> None:
        has_result = self._last_result is not None
        self.export_again_button.setEnabled(has_result and self._active_worker is None)
        self.export_again_action.setEnabled(has_result and self._active_worker is None)

    def _set_processing_state(self, is_processing: bool) -> None:
        self.select_folder_button.setEnabled(not is_processing)
        self.extract_button.setEnabled(not is_processing and bool(self._pdf_files))
        self.export_again_button.setEnabled(not is_processing and self._last_result is not None)
        self.export_again_action.setEnabled(not is_processing and self._last_result is not None)
        self.about_button.setEnabled(not is_processing)

    def _set_status_badge(self, text: str, kind: str) -> None:
        self.status_badge.setText(text)
        self.status_badge.setProperty("kind", kind)
        self.status_badge.style().unpolish(self.status_badge)
        self.status_badge.style().polish(self.status_badge)
        self.status_badge.update()

    def _default_output_filename(self) -> str:
        if self._selected_folder is not None:
            return f"relatorio_{self._selected_folder.name}.xlsx"
        return "relatorio_notas.xlsx"
