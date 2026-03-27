from __future__ import annotations

import re
from datetime import date
from decimal import Decimal

from domain.models import ExtractedItem
from domain.normalizers import normalize_for_matching, normalize_whitespace, parse_brazilian_decimal


_SECTION_START_MARKERS = ("DADOS DOS PRODUTOS", "DADOS DOS SERVICOS")
_SECTION_END_MARKERS = (
    "DADOS ADICIONAIS",
    "INFORMACOES COMPLEMENTARES",
    "RESERVADO AO FISCO",
    "RECEBEMOS DE",
)
_ITEM_MARKER_PATTERN = re.compile(r"\bITEM(?:\s+\d+)?\b", re.IGNORECASE)
_ITEM_CODE_PATTERN = re.compile(r"^\d{4,6}[,.]?\s")
_QUANTITY_PATTERN = re.compile(r"\b\d+[,.]\d{3}\b")


def parse_item_line(line: str, pdf_filename: str) -> ExtractedItem | None:
    items = parse_item_rows([line], pdf_filename=pdf_filename)
    return items[0] if items else None


def parse_item_rows(
    lines: list[str],
    pdf_filename: str,
    *,
    city: str | None = None,
    document_number: str | None = None,
    issue_date: date | None = None,
) -> list[ExtractedItem]:
    item_section = _extract_item_section(lines)
    item_blocks = _split_item_blocks(item_section)
    items: list[ExtractedItem] = []

    for block in item_blocks:
        item = _parse_item_block(
            block,
            pdf_filename=pdf_filename,
            city=city,
            document_number=document_number,
            issue_date=issue_date,
        )
        if item is not None:
            items.append(item)

    return items


def _extract_item_section(lines: list[str]) -> list[str]:
    start_index: int | None = None

    for index, line in enumerate(lines):
        normalized_line = normalize_for_matching(line)
        if any(marker in normalized_line for marker in _SECTION_START_MARKERS):
            start_index = index + 1
            break

    if start_index is None:
        return []

    item_lines: list[str] = []

    for line in lines[start_index:]:
        normalized_line = normalize_for_matching(line)
        if any(marker in normalized_line for marker in _SECTION_END_MARKERS):
            break
        if _is_header_line(normalized_line):
            continue

        item_lines.append(normalize_whitespace(line))

    return item_lines


def _split_item_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current_block: list[str] = []

    for line in lines:
        if not line:
            continue

        has_numeric_line = any(_looks_like_item_numeric_line(entry) for entry in current_block)

        if current_block and has_numeric_line and (_contains_item_marker(line) or _looks_like_item_numeric_line(line)):
            blocks.append(current_block)
            current_block = [line]
            continue

        current_block.append(line)

    if current_block:
        blocks.append(current_block)

    return [block for block in blocks if any(_looks_like_item_numeric_line(line) for line in block)]


def _parse_item_block(
    block: list[str],
    *,
    pdf_filename: str,
    city: str | None,
    document_number: str | None,
    issue_date: date | None,
) -> ExtractedItem | None:
    numeric_line_index = next(
        (index for index, line in enumerate(block) if _looks_like_item_numeric_line(line)),
        None,
    )
    if numeric_line_index is None:
        return None

    numeric_line = block[numeric_line_index]
    quantity, total_value = _extract_quantity_and_total(numeric_line)
    if quantity is None or total_value is None:
        return None

    prefix_lines = block[:numeric_line_index]
    suffix_lines = block[numeric_line_index + 1 :]
    inline_description = _extract_inline_description(numeric_line)

    if prefix_lines:
        raw_description = " ".join(prefix_lines)
    else:
        raw_description = " ".join(part for part in [inline_description, *suffix_lines] if part)

    description = _clean_item_description(raw_description or inline_description)
    if not description:
        description = "ITEM NAO IDENTIFICADO"

    return ExtractedItem(
        pdf_filename=pdf_filename,
        extraction_status="sucesso",
        city=city,
        document_number=document_number,
        issue_date=issue_date,
        item_description=description,
        item_quantity=quantity,
        item_total_value=total_value,
    )


def _contains_item_marker(line: str) -> bool:
    return _ITEM_MARKER_PATTERN.search(normalize_for_matching(line)) is not None


def _looks_like_item_numeric_line(line: str) -> bool:
    normalized_line = normalize_whitespace(line)
    has_quantity = _QUANTITY_PATTERN.search(normalized_line) is not None
    if not has_quantity:
        return False

    if _contains_item_marker(normalized_line) or _ITEM_CODE_PATTERN.match(normalized_line) is not None:
        return True

    return _count_numeric_values_after_quantity(normalized_line) >= 3


def _extract_quantity_and_total(line: str) -> tuple[Decimal | None, Decimal | None]:
    tokens = [token for token in re.split(r"[|\s]+", line) if token]
    quantity_index = next(
        (index for index, token in enumerate(tokens) if _QUANTITY_PATTERN.fullmatch(token) is not None),
        None,
    )
    if quantity_index is None:
        return None, None

    quantity = parse_brazilian_decimal(tokens[quantity_index])
    values_after_quantity = [
        (token, value)
        for token in tokens[quantity_index + 1 :]
        if (value := parse_brazilian_decimal(token)) is not None
    ]

    if not values_after_quantity:
        return quantity, None

    if len(values_after_quantity) == 1:
        total_token, total_value = values_after_quantity[0]
    elif values_after_quantity[0][1] == values_after_quantity[1][1]:
        total_token, total_value = values_after_quantity[0]
    else:
        selected_index = 1
        if (
            len(values_after_quantity) >= 3
            and not _token_has_explicit_separator(values_after_quantity[1][0])
            and _token_has_explicit_separator(values_after_quantity[2][0])
        ):
            selected_index = 2
        total_token, total_value = values_after_quantity[selected_index]

    return quantity, _coerce_monetary_value(total_token, total_value)


def _coerce_monetary_value(token: str, parsed_value: Decimal) -> Decimal:
    if _token_has_explicit_separator(token):
        return parsed_value

    digits_only = re.sub(r"\D", "", token)
    if len(digits_only) >= 4:
        return Decimal(digits_only) / Decimal("100")

    return parsed_value


def _token_has_explicit_separator(token: str) -> bool:
    return "," in token or "." in token


def _count_numeric_values_after_quantity(line: str) -> int:
    tokens = [token for token in re.split(r"[|\s]+", line) if token]
    quantity_index = next(
        (index for index, token in enumerate(tokens) if _QUANTITY_PATTERN.fullmatch(token) is not None),
        None,
    )
    if quantity_index is None:
        return 0

    return sum(1 for token in tokens[quantity_index + 1 :] if parse_brazilian_decimal(token) is not None)


def _extract_inline_description(line: str) -> str:
    quantity_match = _QUANTITY_PATTERN.search(line)
    prefix = line[: quantity_match.start()] if quantity_match else line
    prefix = prefix.replace("|", " ")
    prefix = re.sub(r"^\d{4,6}[,.]?\s*", "", prefix)
    prefix = re.sub(r"\b\d{6,10}\b\s+\d{2,3}\s+\d{4}\s+[A-Z]{1,3}\s*$", "", prefix, flags=re.IGNORECASE)
    prefix = re.sub(r"\b\d{6,10}\b\s*$", "", prefix)
    return normalize_whitespace(prefix)


def _clean_item_description(description: str) -> str:
    cleaned = (
        description.replace("|", " ")
        .replace('"', " ")
        .replace("'", " ")
        .replace("“", " ")
        .replace("”", " ")
        .replace("‘", " ")
        .replace("’", " ")
        .replace("*", " ")
    )
    cleaned = normalize_whitespace(cleaned)
    cleaned = re.sub(r"\b(10|25|40|100|200|400)6\b", r"\1G", cleaned)
    cleaned = re.sub(r"(?i)\bcodigo\b.*$", "", cleaned)
    cleaned = re.sub(r"(?i)\bqtde\b.*$", "", cleaned)
    cleaned = re.sub(r"(?i)\bnumeros?\s+de\s+serie\b.*$", "", cleaned)
    cleaned = re.sub(r"(?i)\b(ITEM(?:\s+\d+)?)\b.*$", r"\1", cleaned)
    cleaned = re.sub(r"\s+[/-]\s*$", "", cleaned)
    cleaned = re.sub(r"^[^A-Z0-9]+", "", cleaned)
    return normalize_whitespace(cleaned)


def _is_header_line(normalized_line: str) -> bool:
    header_text = normalize_whitespace(
        normalized_line.replace(".", " ").replace("/", " ").replace("|", " ").replace("]", " ")
    )

    if header_text.startswith("CODIGO") or header_text.startswith("PRDPNY"):
        return True

    return any(
        marker in header_text
        for marker in (
            "PRODUTO DESCRICAO",
            "PRODUTO DESCRIGAO",
            "DESCRICAO DO PRODUTO",
            "DESCRIGAO DO PRODUTO",
            "QUANTIDADE ESPECIE",
            "VALOR TOTAL",
            "B CALC",
            "ALIQ",
        )
    )
