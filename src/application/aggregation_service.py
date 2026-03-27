from __future__ import annotations

from collections.abc import Iterable

from domain.models import BatchExtractionResult, CityItemSummaryRow, ExtractedItem
from infrastructure.aggregation.city_item_aggregator import aggregate_by_city_and_item


class CityItemAggregationService:
    """Build the grouped summary by city and item description."""

    def aggregate_items(self, items: Iterable[ExtractedItem]) -> list[CityItemSummaryRow]:
        return aggregate_by_city_and_item(items)

    def aggregate_batch(self, batch_result: BatchExtractionResult) -> list[CityItemSummaryRow]:
        return self.aggregate_items(batch_result.items)
