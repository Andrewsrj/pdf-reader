from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal

from domain.models import CityItemSummaryRow, ExtractedItem
from domain.normalizers import normalize_whitespace


def aggregate_by_city_and_item(items: Iterable[ExtractedItem]) -> list[CityItemSummaryRow]:
    grouped: dict[tuple[str, str], CityItemSummaryRow] = {}

    for item in items:
        city = normalize_whitespace(item.city)
        description = normalize_whitespace(item.item_description)
        key = (city, description)

        if key not in grouped:
            grouped[key] = CityItemSummaryRow(
                city=city,
                item_description=description,
                total_item_quantity=Decimal("0"),
                total_item_value=Decimal("0"),
            )

        if item.item_quantity is not None:
            grouped[key].total_item_quantity += item.item_quantity

        if item.item_total_value is not None:
            grouped[key].total_item_value += item.item_total_value

    return [grouped[key] for key in sorted(grouped, key=lambda pair: (pair[0], pair[1]))]
