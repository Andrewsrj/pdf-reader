from __future__ import annotations

from datetime import date
from decimal import Decimal


EXPECTED_SAMPLE_RESULTS = {
    "NFSE_SP_11964_MT_TIM.pdf": {
        "city": "FORTALEZA",
        "document_number": "000.011.964",
        "issue_date": date(2026, 2, 27),
        "items": [
            ("MAN INSTALLATION KIT TYPE AGGREGATION ITEM", Decimal("1.000"), Decimal("36339.6500")),
        ],
    },
    "PR_6478_HW_TIM.pdf": {
        "city": "FORTALEZA",
        "document_number": "000.006.478",
        "issue_date": date(2026, 2, 27),
        "items": [
            ("MAN HW NCST MPA 2D4H FC NAC SOB ITEM 30", Decimal("2.000"), Decimal("14898.52")),
        ],
    },
    "PR_6482_HW_TIM.pdf": {
        "city": "FORTALEZA",
        "document_number": "000.006.482",
        "issue_date": date(2026, 2, 27),
        "items": [
            ("MAN NCS 57C3 MOD SYS NAC SOB ITEM 10", Decimal("1.000"), Decimal("56825.5000")),
            ("MAN HW NCS7 MOD RP2 E NAC SOB ITEM 20", Decimal("2.000"), Decimal("10641.80")),
            ("MAN MOD CONEX BRIGHT 400G NAC SOB ITEM 40", Decimal("4.000"), Decimal("129344.24")),
            ("MAN HW MOD CONEX 100G LR4 S NAC SOB ITEM 50", Decimal("8.000"), Decimal("18805.60")),
            ("MAN HW MOD CONEX SFP 10G LR NAC SOB ITEM 60", Decimal("20.000"), Decimal("5218.20")),
        ],
    },
    "PR_6483_HW_TIM.pdf": {
        "city": "FORTALEZA",
        "document_number": "000.006.483",
        "issue_date": date(2026, 2, 27),
        "items": [
            ("MAN HW ESS 100G RTU 2 NAC SOB ITEM 10", Decimal("12.000"), Decimal("23704.68")),
        ],
    },
    "PR_6484_HW_TIM.pdf": {
        "city": "FORTALEZA",
        "document_number": "000.006.484",
        "issue_date": date(2026, 2, 27),
        "items": [
            ("HW MOD GLC LH SMD NAC SOB ITEM 10", Decimal("2.000"), Decimal("311.90")),
        ],
    },
}


EXPECTED_SUMMARY_ROWS = [
    ("FORTALEZA", "HW MOD GLC LH SMD NAC SOB ITEM 10", Decimal("2.000"), Decimal("311.90")),
    ("FORTALEZA", "MAN HW ESS 100G RTU 2 NAC SOB ITEM 10", Decimal("12.000"), Decimal("23704.68")),
    ("FORTALEZA", "MAN HW MOD CONEX 100G LR4 S NAC SOB ITEM 50", Decimal("8.000"), Decimal("18805.60")),
    ("FORTALEZA", "MAN HW MOD CONEX SFP 10G LR NAC SOB ITEM 60", Decimal("20.000"), Decimal("5218.20")),
    ("FORTALEZA", "MAN HW NCS7 MOD RP2 E NAC SOB ITEM 20", Decimal("2.000"), Decimal("10641.80")),
    ("FORTALEZA", "MAN HW NCST MPA 2D4H FC NAC SOB ITEM 30", Decimal("2.000"), Decimal("14898.52")),
    ("FORTALEZA", "MAN INSTALLATION KIT TYPE AGGREGATION ITEM", Decimal("1.000"), Decimal("36339.6500")),
    ("FORTALEZA", "MAN MOD CONEX BRIGHT 400G NAC SOB ITEM 40", Decimal("4.000"), Decimal("129344.24")),
    ("FORTALEZA", "MAN NCS 57C3 MOD SYS NAC SOB ITEM 10", Decimal("1.000"), Decimal("56825.5000")),
]


EXPECTED_TOTAL_FILES = 5
EXPECTED_TOTAL_ITEMS = 9
