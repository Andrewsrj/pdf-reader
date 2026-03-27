from decimal import Decimal

from domain.normalizers import (
    normalize_whitespace,
    parse_brazilian_currency,
    parse_brazilian_decimal,
)


def test_normalize_whitespace_collapses_internal_spaces() -> None:
    assert normalize_whitespace("  Sao   Paulo   Centro  ") == "Sao Paulo Centro"


def test_parse_brazilian_decimal_handles_thousands_separator() -> None:
    assert parse_brazilian_decimal("1.234,56") == Decimal("1234.56")


def test_parse_brazilian_currency_handles_currency_prefix() -> None:
    assert parse_brazilian_currency("R$ 87,40") == Decimal("87.40")


def test_parse_brazilian_decimal_handles_mixed_ocr_separators() -> None:
    assert parse_brazilian_decimal("36,339.65") == Decimal("36339.65")


def test_parse_brazilian_decimal_handles_repeated_commas_from_ocr_noise() -> None:
    assert parse_brazilian_decimal("220,835,34") == Decimal("220835.34")
