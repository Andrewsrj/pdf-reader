from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

from domain.models import ExtractionError, ExtractedItem
from domain.normalizers import normalize_for_matching, parse_brazilian_date
from infrastructure.parser.city_parser import parse_city
from infrastructure.parser.item_line_parser import parse_item_rows


@dataclass(slots=True)
class ParsedInvoice:
    city: str | None = None
    document_number: str | None = None
    issue_date: date | None = None
    items: list[ExtractedItem] = field(default_factory=list)
    errors: list[ExtractionError] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


class InvoiceLayoutParser:
    """High-level parser that coordinates city and item extraction."""

    def parse(self, lines: list[str], pdf_filename: str) -> ParsedInvoice:
        city = parse_city(lines)
        document_number = self._extract_document_number(lines)
        issue_date = self._extract_issue_date(lines)
        items = parse_item_rows(
            lines,
            pdf_filename=pdf_filename,
            city=city,
            document_number=document_number,
            issue_date=issue_date,
        )

        errors: list[ExtractionError] = []
        notes: list[str] = []

        if city is None:
            errors.append(
                ExtractionError(
                    pdf_filename=pdf_filename,
                    error_type="cidade_nao_encontrada",
                    message="Nao foi possivel identificar a cidade da nota.",
                    stage="parser",
                )
            )

        if not items:
            errors.append(
                ExtractionError(
                    pdf_filename=pdf_filename,
                    error_type="itens_nao_extraidos",
                    message="Nenhuma linha de item util foi extraida da nota.",
                    stage="parser",
                )
            )

        status = "parcial" if errors else "sucesso"
        for item in items:
            item.extraction_status = status

        if document_number is None:
            notes.append("Numero do documento nao identificado.")

        if issue_date is None:
            notes.append("Data de emissao nao identificada.")

        return ParsedInvoice(
            city=city,
            document_number=document_number,
            issue_date=issue_date,
            items=items,
            errors=errors,
            notes=notes,
        )

    def _extract_document_number(self, lines: list[str]) -> str | None:
        pattern = re.compile(r"\b\d{3}\.\d{3}\.\d{3}\b")

        for line in lines:
            match = pattern.search(line)
            if match:
                return match.group(0)

        return None

    def _extract_issue_date(self, lines: list[str]) -> date | None:
        date_pattern = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")

        for index, line in enumerate(lines):
            if "DATA DA EMISSAO" not in normalize_for_matching(line):
                continue

            for candidate in lines[index + 1 : index + 3]:
                match = date_pattern.search(candidate)
                if match:
                    return parse_brazilian_date(match.group(0))

        for line in lines:
            match = date_pattern.search(line)
            if match:
                return parse_brazilian_date(match.group(0))

        return None
