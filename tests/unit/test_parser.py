from datetime import date
from decimal import Decimal

from infrastructure.parser.city_parser import parse_city
from infrastructure.parser.invoice_layout_parser import InvoiceLayoutParser
from infrastructure.parser.item_line_parser import parse_item_rows


def test_parse_city_reads_destination_city_after_municipio_header() -> None:
    lines = [
        "ENDERECO BAIRRO/ DISTRITO CEP DATA DA SAIDA",
        "AV BARAO DE STUDART, 2575 DIONISIO TORRES 60120-375 27/02/2026",
        "MUNICIPIO UF | FONE/FAX INSCRIGAO ESTADUAL HORA DA SAIDA",
        "FORTALEZA CE 06287754-2 17:53:57",
    ]

    assert parse_city(lines) == "FORTALEZA"


def test_parse_item_rows_handles_single_line_item_block() -> None:
    lines = [
        "DADOS DOS PRODUTOS / SERVICOS",
        "CODIGO x VALOR VALOR B. CALC VALOR VALOR ALIQ | ALIQ",
        "PRODUTO DESCRICAO DO PRODUTO / SERVICO NCM/SH | O/CST | CFOP | UN | QUANT UNITARIO TOTAL ICMS ICMS IPI ICMS | IPI",
        "HW MOD GLC LH SMD NAC SOB *ITEM 10 85176259 | 700 2,000 155,9500 311,90 311,90 21,83 0,00 7,00 | 0,00",
        "DADOS ADICIONAIS",
    ]

    items = parse_item_rows(lines, pdf_filename="PR_6484_HW_TIM.pdf", city="FORTALEZA")

    assert len(items) == 1
    assert items[0].item_description == "HW MOD GLC LH SMD NAC SOB ITEM 10"
    assert items[0].item_quantity == Decimal("2.000")
    assert items[0].item_total_value == Decimal("311.90")


def test_parse_item_rows_handles_multiline_item_blocks() -> None:
    lines = [
        "DADOS DOS PRODUTOS / SERVICOS",
        "CODIGO x VALOR VALOR B. CALC VALOR VALOR ALIQ | ALIQ",
        "PRODUTO DESCRICAO DO PRODUTO / SERVICO NCM/SH | O/CST | CFOP | UN | QUANT UNITARIO TOTAL ICMS ICMS IPI ICMS | IPI",
        "MAN NCS 57C3 MOD SYS NAC SOB *ITEM 10 codigo NCS-",
        "25489 57C3-MOD-SYS - Qtde | - numeros de serie: FOC2944ROCE 85176249 | 200 | 6106 | PC 1,000 56.825,5000 | 56.825,50 56.825,50 2.273,02 0,00 4,00 | 0,00",
        "25487 MAN HW NCS7 MOD RP2 E NAC SOB *ITEM 20 85176249 | 200 | 6106 | PC 2,000 5.320,9000 10.641,80 10.641,80 425,67 0,00 4,00 | 0,00",
        "MAN MOD CONEX BRIGHT 400G NAC SOB ITEM 40",
        "25483 codigo aoe ncaa itd seer oe / 85176259 | 700 | 6106 | PC 4,000 32.336,0600 | 129.344,24 | 129.344,24 | 9.054,10 0,00 7,00 | 0,00",
        "MAN HW MOD CONEX 100G LR4 S NAC SOB ITEM 50",
        "25484 FNS29441396 / FNS294418B9 / FNS29441B2U / 85176259 | 700 | 6106 | PC 8,000 2.350,7000 | 18.805,60 | 18.805,60 | 1.316,39 0,00 7,00 | 0,00",
        "DADOS ADICIONAIS",
    ]

    items = parse_item_rows(lines, pdf_filename="PR_6482_HW_TIM.pdf", city="FORTALEZA")

    assert [item.item_description for item in items] == [
        "MAN NCS 57C3 MOD SYS NAC SOB ITEM 10",
        "MAN HW NCS7 MOD RP2 E NAC SOB ITEM 20",
        "MAN MOD CONEX BRIGHT 400G NAC SOB ITEM 40",
        "MAN HW MOD CONEX 100G LR4 S NAC SOB ITEM 50",
    ]
    assert [item.item_quantity for item in items] == [
        Decimal("1.000"),
        Decimal("2.000"),
        Decimal("4.000"),
        Decimal("8.000"),
    ]
    assert [item.item_total_value for item in items] == [
        Decimal("56825.5000"),
        Decimal("10641.80"),
        Decimal("129344.24"),
        Decimal("18805.60"),
    ]


def test_invoice_layout_parser_extracts_metadata_and_items() -> None:
    lines = [
        "000.006.483",
        "NOME /RAZAO SOCIAL CNPITCPF DATA DA EMISSAO",
        "TIM S/A 02.421.421/0080-15 27/02/2026",
        "MUNICIPIO UF | FONE/FAX INSCRIGAO ESTADUAL HORA DA SAIDA",
        "FORTALEZA CE 06287754-2 17:53:30",
        "DADOS DOS PRODUTOS / SERVICOS",
        "25486 MAN HW ESS 100G RTU 2 NAC SOB *ITEM 10 85176249 200 6106 | PC 12,000 1.975,3900 23.704,68 23.704,68 948,19 0,00 4,00 | 0,00",
        "DADOS ADICIONAIS",
    ]

    parsed = InvoiceLayoutParser().parse(lines, "PR_6483_HW_TIM.pdf")

    assert parsed.city == "FORTALEZA"
    assert parsed.document_number == "000.006.483"
    assert parsed.issue_date == date(2026, 2, 27)
    assert len(parsed.items) == 1
    assert parsed.items[0].item_description == "MAN HW ESS 100G RTU 2 NAC SOB ITEM 10"
    assert parsed.items[0].item_quantity == Decimal("12.000")
    assert parsed.items[0].item_total_value == Decimal("23704.68")
