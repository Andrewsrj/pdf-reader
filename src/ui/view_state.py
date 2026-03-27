from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from domain.models import BatchExtractionResult


@dataclass(frozen=True, slots=True)
class DashboardMetrics:
    total_pdfs: int
    extracted_items: int
    grouped_rows: int
    failed_files: int


def build_dashboard_metrics(total_pdfs: int, result: BatchExtractionResult | None) -> DashboardMetrics:
    if result is None:
        return DashboardMetrics(
            total_pdfs=total_pdfs,
            extracted_items=0,
            grouped_rows=0,
            failed_files=0,
        )

    return DashboardMetrics(
        total_pdfs=total_pdfs,
        extracted_items=result.total_items,
        grouped_rows=result.total_summary_rows,
        failed_files=result.failed,
    )


def build_folder_status_text(selected_folder: Path | None, total_pdfs: int) -> str:
    if selected_folder is None:
        return "Escolha uma pasta para montar o lote e acompanhar o progresso do OCR."

    if total_pdfs == 0:
        return "A pasta selecionada nao contem PDFs. Escolha outro diretorio para continuar."

    return (
        f"Pasta pronta: {selected_folder.name}. "
        f"{total_pdfs} PDF(s) aguardando processamento."
    )


def build_latest_run_summary(
    result: BatchExtractionResult | None,
    output_path: Path | None = None,
) -> str:
    if result is None:
        return "Nenhum lote executado ainda. Os indicadores do ultimo processamento aparecem aqui."

    base_summary = (
        f"Ultimo lote: {result.total_files} arquivo(s), "
        f"{result.total_items} item(ns), "
        f"{result.total_summary_rows} grupo(s) "
        f"e {result.failed} falha(s)."
    )

    if output_path is not None:
        return f"{base_summary} Ultimo Excel: {output_path.name}."

    return base_summary


def build_export_cancelled_message(result: BatchExtractionResult) -> str:
    return (
        f"A extracao foi concluida com {result.total_items} item(ns) e "
        f"{result.total_summary_rows} grupo(s), mas o arquivo Excel nao foi salvo."
    )


def build_completion_message(result: BatchExtractionResult, output_path: Path) -> str:
    return (
        f"Arquivos processados: {result.total_files}\n"
        f"Sucessos: {result.succeeded}\n"
        f"Parciais: {result.partial}\n"
        f"Falhas: {result.failed}\n"
        f"Itens extraidos: {result.total_items}\n"
        f"Grupos cidade/item: {result.total_summary_rows}\n"
        f"Arquivo gerado: {output_path}"
    )
