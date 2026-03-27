from __future__ import annotations

from domain.models import ExtractedItem


def has_meaningful_item_data(item: ExtractedItem) -> bool:
    return any(
        (
            bool(item.city),
            bool(item.item_description),
            item.item_quantity is not None,
            item.item_total_value is not None,
        )
    )
