from decimal import Decimal
from pathlib import Path

from application.aggregation_service import CityItemAggregationService
from domain.models import BatchExtractionResult, CityItemSummaryRow, ExtractedItem, InvoiceExtractionResult


def test_aggregate_items_groups_by_city_and_description() -> None:
    items = [
        ExtractedItem(
            pdf_filename="a.pdf",
            extraction_status="sucesso",
            city="FORTALEZA",
            item_description="ITEM A",
            item_quantity=Decimal("2"),
            item_total_value=Decimal("10.50"),
        ),
        ExtractedItem(
            pdf_filename="b.pdf",
            extraction_status="sucesso",
            city="FORTALEZA",
            item_description="ITEM A",
            item_quantity=Decimal("3"),
            item_total_value=Decimal("15.00"),
        ),
        ExtractedItem(
            pdf_filename="c.pdf",
            extraction_status="sucesso",
            city="SAO PAULO",
            item_description="ITEM B",
            item_quantity=Decimal("1"),
            item_total_value=Decimal("7.25"),
        ),
    ]

    summary = CityItemAggregationService().aggregate_items(items)

    assert summary == [
        CityItemSummaryRow(
            city="FORTALEZA",
            item_description="ITEM A",
            total_item_quantity=Decimal("5"),
            total_item_value=Decimal("25.50"),
        ),
        CityItemSummaryRow(
            city="SAO PAULO",
            item_description="ITEM B",
            total_item_quantity=Decimal("1"),
            total_item_value=Decimal("7.25"),
        ),
    ]


def test_aggregate_batch_uses_items_from_all_results() -> None:
    batch_result = BatchExtractionResult(
        results=[
            InvoiceExtractionResult(
                pdf_path=Path("a.pdf"),
                items=[
                    ExtractedItem(
                        pdf_filename="a.pdf",
                        extraction_status="sucesso",
                        city="FORTALEZA",
                        item_description="ITEM A",
                        item_quantity=Decimal("2"),
                        item_total_value=Decimal("10"),
                    )
                ],
            ),
            InvoiceExtractionResult(
                pdf_path=Path("b.pdf"),
                items=[
                    ExtractedItem(
                        pdf_filename="b.pdf",
                        extraction_status="sucesso",
                        city="FORTALEZA",
                        item_description="ITEM A",
                        item_quantity=Decimal("1"),
                        item_total_value=Decimal("5"),
                    ),
                    ExtractedItem(
                        pdf_filename="b.pdf",
                        extraction_status="sucesso",
                        city="CURITIBA",
                        item_description="ITEM C",
                        item_quantity=Decimal("4"),
                        item_total_value=Decimal("20"),
                    ),
                ],
            ),
        ]
    )

    summary = CityItemAggregationService().aggregate_batch(batch_result)

    assert [(row.city, row.item_description) for row in summary] == [
        ("CURITIBA", "ITEM C"),
        ("FORTALEZA", "ITEM A"),
    ]
    assert [(row.total_item_quantity, row.total_item_value) for row in summary] == [
        (Decimal("4"), Decimal("20")),
        (Decimal("3"), Decimal("15")),
    ]
