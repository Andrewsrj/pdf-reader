from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal

from domain.models import ExtractedItem


def aggregate_by_city_and_item(items: Iterable[ExtractedItem]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, object]] = {}

    for item in items:
        city = item.city or ""
        description = item.item_description or ""
        key = (city, description)

        if key not in grouped:
            grouped[key] = {
                "cidade": city,
                "item_descricao": description,
                "soma_item_qtd": Decimal("0"),
                "soma_item_valor_total": Decimal("0"),
            }

        if item.item_quantity is not None:
            grouped[key]["soma_item_qtd"] += item.item_quantity

        if item.item_total_value is not None:
            grouped[key]["soma_item_valor_total"] += item.item_total_value

    return [grouped[key] for key in sorted(grouped)]
