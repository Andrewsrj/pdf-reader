from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

from application.aggregation_service import CityItemAggregationService
from application.progress import ProgressUpdate
from domain.models import BatchExtractionResult, ExtractionError, InvoiceExtractionResult
from infrastructure.ocr.ocr_engine import TesseractOcrEngine
from infrastructure.parser.invoice_layout_parser import InvoiceLayoutParser
from infrastructure.pdf.renderer import PdfRenderer


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


class InvoiceBatchProcessor:
    """Orchestrate PDF rendering, OCR and invoice parsing for a batch."""

    _STEPS_PER_FILE = 4
    _FINALIZATION_STEPS = 1

    def __init__(
        self,
        renderer: PdfRenderer | None = None,
        ocr_engine: TesseractOcrEngine | None = None,
        parser: InvoiceLayoutParser | None = None,
        aggregation_service: CityItemAggregationService | None = None,
    ) -> None:
        self._renderer = renderer or PdfRenderer()
        self._ocr_engine = ocr_engine or TesseractOcrEngine()
        self._parser = parser or InvoiceLayoutParser()
        self._aggregation_service = aggregation_service or CityItemAggregationService()

    def extract_batch(
        self,
        pdf_paths: Sequence[Path],
        progress_callback: Callable[[ProgressUpdate], None] | None = None,
    ) -> BatchExtractionResult:
        results: list[InvoiceExtractionResult] = []
        total_steps = max((len(pdf_paths) * self._STEPS_PER_FILE) + self._FINALIZATION_STEPS, 1)

        for index, pdf_path in enumerate(pdf_paths):
            base_step = index * self._STEPS_PER_FILE

            self._emit_progress(
                progress_callback,
                current=base_step + 1,
                total=total_steps,
                message=f"Preparando {pdf_path.name}...",
            )

            result = self._extract_single_pdf(pdf_path, progress_callback, base_step, total_steps)
            results.append(result)

            self._emit_progress(
                progress_callback,
                current=base_step + self._STEPS_PER_FILE,
                total=total_steps,
                message=self._build_completion_message(result),
            )

        self._emit_progress(
            progress_callback,
            current=total_steps,
            total=total_steps,
            message="Consolidando resumo por cidade e item...",
        )

        batch_result = BatchExtractionResult(results=results)
        summary_rows = self._aggregation_service.aggregate_batch(batch_result)
        return BatchExtractionResult(results=results, summary_rows=summary_rows)

    def _extract_single_pdf(
        self,
        pdf_path: Path,
        progress_callback: Callable[[ProgressUpdate], None] | None,
        base_step: int,
        total_steps: int,
    ) -> InvoiceExtractionResult:
        try:
            self._emit_progress(
                progress_callback,
                current=base_step + 2,
                total=total_steps,
                message=f"Renderizando {pdf_path.name}...",
            )
            rendered_pages = self._renderer.render(pdf_path)
        except Exception as exc:
            return self._build_failure_result(pdf_path, "renderizacao_pdf", str(exc))

        try:
            self._emit_progress(
                progress_callback,
                current=base_step + 3,
                total=total_steps,
                message=f"Executando OCR em {pdf_path.name}...",
            )
            ocr_lines = self._ocr_engine.extract_lines([page.image for page in rendered_pages])
        except Exception as exc:
            return self._build_failure_result(pdf_path, "ocr", str(exc))

        if not ocr_lines:
            return self._build_failure_result(
                pdf_path,
                "ocr_sem_texto",
                "O OCR nao retornou linhas utilizaveis para esta nota.",
            )

        try:
            parsed_invoice = self._parser.parse(ocr_lines, pdf_path.name)
        except Exception as exc:
            return self._build_failure_result(pdf_path, "parser", str(exc), raw_lines=ocr_lines)

        return InvoiceExtractionResult(
            pdf_path=pdf_path,
            city=parsed_invoice.city,
            document_number=parsed_invoice.document_number,
            issue_date=parsed_invoice.issue_date,
            items=parsed_invoice.items,
            errors=parsed_invoice.errors,
            raw_lines=ocr_lines,
        )

    def _build_failure_result(
        self,
        pdf_path: Path,
        error_type: str,
        message: str,
        *,
        raw_lines: list[str] | None = None,
    ) -> InvoiceExtractionResult:
        return InvoiceExtractionResult(
            pdf_path=pdf_path,
            errors=[
                ExtractionError(
                    pdf_filename=pdf_path.name,
                    error_type=error_type,
                    message=message,
                    stage=error_type,
                )
            ],
            raw_lines=raw_lines or [],
        )

    def _emit_progress(
        self,
        progress_callback: Callable[[ProgressUpdate], None] | None,
        *,
        current: int,
        total: int,
        message: str,
    ) -> None:
        if progress_callback is None:
            return

        progress_callback(ProgressUpdate(current=current, total=total, message=message))

    def _build_completion_message(self, result: InvoiceExtractionResult) -> str:
        if result.status == "sucesso":
            return f"{result.pdf_path.name}: {len(result.items)} item(ns) extraido(s) com sucesso."
        if result.status == "parcial":
            return f"{result.pdf_path.name}: extracao parcial com {len(result.items)} item(ns)."
        return f"{result.pdf_path.name}: falha na extracao."
