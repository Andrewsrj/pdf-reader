from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal
from pathlib import Path
from typing import Any

import pandas as pd
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from domain.models import BatchExtractionResult, CityItemSummaryRow, InvoiceExtractionResult
from infrastructure.aggregation.city_item_aggregator import aggregate_by_city_and_item


class ExcelExporter:
    """Persist extracted data into the required workbook sheets."""

    BASE_COLUMNS = [
        "arquivo_pdf",
        "status_extracao",
        "cidade",
        "numero_documento",
        "data_emissao",
        "item_descricao",
        "item_qtd",
        "item_valor_total",
        "observacoes",
    ]
    SUMMARY_COLUMNS = [
        "cidade",
        "item_descricao",
        "soma_item_qtd",
        "soma_item_valor_total",
    ]
    ERROR_COLUMNS = [
        "arquivo_pdf",
        "tipo_erro",
        "mensagem",
        "etapa",
    ]

    def export_batch(self, output_path: Path, batch_result: BatchExtractionResult) -> Path:
        if output_path.suffix.lower() != ".xlsx":
            output_path = output_path.with_suffix(".xlsx")

        summary_rows = batch_result.summary_rows or aggregate_by_city_and_item(batch_result.items)
        base_df = pd.DataFrame(self._build_base_rows(batch_result.results), columns=self.BASE_COLUMNS)
        summary_df = pd.DataFrame(self._build_summary_rows(summary_rows), columns=self.SUMMARY_COLUMNS)
        errors_df = pd.DataFrame(self._build_error_rows(batch_result.results), columns=self.ERROR_COLUMNS)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            base_df.to_excel(writer, sheet_name="Base_Itens", index=False)
            summary_df.to_excel(writer, sheet_name="Resumo_Cidade_Item", index=False)
            errors_df.to_excel(writer, sheet_name="Erros", index=False)

            workbook = writer.book
            self._format_base_sheet(workbook["Base_Itens"])
            self._format_summary_sheet(workbook["Resumo_Cidade_Item"], summary_df.shape[0])
            self._format_error_sheet(workbook["Erros"])

        return output_path

    def _build_base_rows(self, results: Sequence[InvoiceExtractionResult]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []

        for result in results:
            shared_observations = self._combine_messages(
                result.notes,
                [error.message for error in result.errors],
            )

            for item in result.items:
                item_observations = self._combine_messages(
                    [item.notes] if item.notes else [],
                    [shared_observations] if shared_observations else [],
                )
                rows.append(
                    {
                        "arquivo_pdf": item.pdf_filename,
                        "status_extracao": item.extraction_status or result.status,
                        "cidade": item.city or result.city or None,
                        "numero_documento": item.document_number or result.document_number or None,
                        "data_emissao": (
                            (item.issue_date or result.issue_date).isoformat()
                            if (item.issue_date or result.issue_date) is not None
                            else None
                        ),
                        "item_descricao": item.item_description or None,
                        "item_qtd": self._excel_number(item.item_quantity),
                        "item_valor_total": self._excel_number(item.item_total_value),
                        "observacoes": item_observations or None,
                    }
                )

        return rows

    def _build_summary_rows(self, summary_rows: Sequence[CityItemSummaryRow]) -> list[dict[str, Any]]:
        rows = [
            {
                "cidade": row.city or None,
                "item_descricao": row.item_description or None,
                "soma_item_qtd": self._excel_number(row.total_item_quantity),
                "soma_item_valor_total": self._excel_number(row.total_item_value),
            }
            for row in summary_rows
        ]

        if summary_rows:
            rows.append(
                {
                    "cidade": "TOTAL GERAL",
                    "item_descricao": None,
                    "soma_item_qtd": self._excel_number(
                        sum((row.total_item_quantity for row in summary_rows), start=Decimal("0"))
                    ),
                    "soma_item_valor_total": self._excel_number(
                        sum((row.total_item_value for row in summary_rows), start=Decimal("0"))
                    ),
                }
            )

        return rows

    def _build_error_rows(self, results: Sequence[InvoiceExtractionResult]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []

        for result in results:
            for error in result.errors:
                rows.append(
                    {
                        "arquivo_pdf": error.pdf_filename,
                        "tipo_erro": error.error_type,
                        "mensagem": error.message,
                        "etapa": error.stage,
                    }
                )

        return rows

    def _format_base_sheet(self, worksheet: Worksheet) -> None:
        self._format_header(worksheet)
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
        self._set_column_widths(
            worksheet,
            {
                "A": 26,
                "B": 16,
                "C": 18,
                "D": 18,
                "E": 14,
                "F": 58,
                "G": 14,
                "H": 18,
                "I": 48,
            },
        )
        self._apply_number_format(worksheet, "G", "#,##0.000")
        self._apply_number_format(worksheet, "H", "#,##0.00")

    def _format_summary_sheet(self, worksheet: Worksheet, data_row_count: int) -> None:
        self._format_header(worksheet)
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
        self._set_column_widths(
            worksheet,
            {
                "A": 20,
                "B": 58,
                "C": 16,
                "D": 20,
            },
        )
        self._apply_number_format(worksheet, "C", "#,##0.000")
        self._apply_number_format(worksheet, "D", "#,##0.00")

        total_row_index = data_row_count + 1
        if data_row_count >= 1:
            for cell in worksheet[total_row_index]:
                cell.font = Font(bold=True)

    def _format_error_sheet(self, worksheet: Worksheet) -> None:
        self._format_header(worksheet)
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
        self._set_column_widths(
            worksheet,
            {
                "A": 28,
                "B": 24,
                "C": 80,
                "D": 18,
            },
        )

    def _format_header(self, worksheet: Worksheet) -> None:
        for cell in worksheet[1]:
            cell.font = Font(bold=True)

    def _set_column_widths(self, worksheet: Worksheet, widths: dict[str, int]) -> None:
        for column, width in widths.items():
            worksheet.column_dimensions[column].width = width

    def _apply_number_format(self, worksheet: Worksheet, column: str, number_format: str) -> None:
        for cell in worksheet[column][1:]:
            if cell.value is not None:
                cell.number_format = number_format

    def _combine_messages(self, *message_groups: Sequence[str]) -> str:
        messages: list[str] = []

        for group in message_groups:
            for message in group:
                normalized = str(message).strip()
                if normalized and normalized not in messages:
                    messages.append(normalized)

        return " | ".join(messages)

    def _excel_number(self, value: Decimal | None) -> float | None:
        if value is None:
            return None
        return float(value)
