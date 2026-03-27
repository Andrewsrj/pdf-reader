from pathlib import Path

from domain.models import BatchExtractionResult, InvoiceExtractionResult
from ui.view_state import (
    build_completion_message,
    build_dashboard_metrics,
    build_export_cancelled_message,
    build_folder_status_text,
    build_latest_run_summary,
)


def test_build_dashboard_metrics_uses_folder_count_and_last_result() -> None:
    result = BatchExtractionResult(results=[InvoiceExtractionResult(pdf_path=Path("a.pdf"))])
    result.summary_rows = []

    metrics = build_dashboard_metrics(4, result)

    assert metrics.total_pdfs == 4
    assert metrics.extracted_items == 0
    assert metrics.grouped_rows == 0
    assert metrics.failed_files == 1


def test_build_folder_status_text_reflects_selected_folder_state() -> None:
    assert build_folder_status_text(None, 0) == (
        "Escolha uma pasta para montar o lote e acompanhar o progresso do OCR."
    )
    assert build_folder_status_text(Path("Notas"), 0) == (
        "A pasta selecionada nao contem PDFs. Escolha outro diretorio para continuar."
    )
    assert build_folder_status_text(Path("Notas"), 7) == (
        "Pasta pronta: Notas. 7 PDF(s) aguardando processamento."
    )


def test_build_completion_and_summary_messages_include_export_path() -> None:
    result = BatchExtractionResult(results=[InvoiceExtractionResult(pdf_path=Path("a.pdf"))])
    output_path = Path("relatorio.xlsx")

    completion_message = build_completion_message(result, output_path)
    latest_summary = build_latest_run_summary(result, output_path)
    cancelled_message = build_export_cancelled_message(result)

    assert "Arquivo gerado: relatorio.xlsx" in completion_message
    assert "Ultimo Excel: relatorio.xlsx." in latest_summary
    assert "mas o arquivo Excel nao foi salvo." in cancelled_message
