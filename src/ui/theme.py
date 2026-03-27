from __future__ import annotations


def build_application_stylesheet() -> str:
    return """
    QWidget {
        background-color: #f4efe6;
        color: #1f2933;
        font-family: "Segoe UI Variable Text", "Segoe UI";
        font-size: 10.5pt;
    }

    QWidget#appPage {
        background:
            qlineargradient(
                x1: 0, y1: 0,
                x2: 1, y2: 1,
                stop: 0 #f6f2ea,
                stop: 0.55 #efe6d7,
                stop: 1 #e8dece
            );
    }

    QScrollArea, QScrollBar {
        border: none;
        background: transparent;
    }

    QMenuBar {
        background: rgba(255, 250, 242, 0.78);
        border-bottom: 1px solid #d8c8b3;
        padding: 6px 10px;
    }

    QMenuBar::item {
        background: transparent;
        border-radius: 10px;
        padding: 8px 12px;
        margin-right: 4px;
    }

    QMenuBar::item:selected,
    QMenuBar::item:pressed {
        background: #efe1cb;
    }

    QMenu {
        background: #fffaf2;
        border: 1px solid #d8c8b3;
        padding: 8px;
    }

    QMenu::item {
        border-radius: 10px;
        padding: 8px 18px;
    }

    QMenu::item:selected {
        background: #efe1cb;
    }

    QFrame#heroCard {
        background:
            qlineargradient(
                x1: 0, y1: 0,
                x2: 1, y2: 1,
                stop: 0 #143d33,
                stop: 0.5 #245b49,
                stop: 1 #d27a42
            );
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 28px;
    }

    QLabel#heroEyebrow {
        background: rgba(255, 249, 240, 0.16);
        border: 1px solid rgba(255, 249, 240, 0.18);
        border-radius: 12px;
        color: #fff6ea;
        font-size: 9pt;
        font-weight: 600;
        letter-spacing: 0.04em;
        padding: 6px 10px;
    }

    QLabel#heroTitle {
        background: transparent;
        color: #fffdf9;
        font-family: "Bahnschrift SemiBold", "Segoe UI Variable Display", "Segoe UI";
        font-size: 23pt;
        font-weight: 700;
    }

    QLabel#heroDescription {
        background: transparent;
        color: rgba(255, 247, 235, 0.92);
        font-size: 10.5pt;
        line-height: 1.45em;
    }

    QLabel#heroChip {
        background: rgba(20, 61, 51, 0.24);
        border: 1px solid rgba(255, 250, 242, 0.18);
        border-radius: 13px;
        color: #fff7ed;
        font-size: 9pt;
        font-weight: 600;
        padding: 7px 12px;
    }

    QFrame#panelCard,
    QFrame#metricCard {
        background: rgba(255, 250, 242, 0.92);
        border: 1px solid #ddcfbb;
        border-radius: 24px;
    }

    QLabel#sectionTitle {
        color: #20313e;
        font-family: "Bahnschrift SemiBold", "Segoe UI Variable Display", "Segoe UI";
        font-size: 15pt;
        font-weight: 700;
        background: transparent;
    }

    QLabel#sectionDescription {
        color: #54606d;
        background: transparent;
        font-size: 10pt;
    }

    QLineEdit#folderPathEdit {
        background: #fffdf9;
        border: 1px solid #d7c9b4;
        border-radius: 16px;
        color: #20313e;
        padding: 14px 16px;
        selection-background-color: #245b49;
    }

    QLabel#subtleLabel {
        background: transparent;
        color: #5b6470;
        font-size: 9.5pt;
    }

    QLabel#folderCounter {
        background: #efe2cc;
        border-radius: 12px;
        color: #6b4e2d;
        font-size: 9pt;
        font-weight: 700;
        padding: 6px 10px;
    }

    QLabel#statusBadge {
        border-radius: 12px;
        font-size: 9pt;
        font-weight: 700;
        padding: 6px 12px;
    }

    QLabel#statusBadge[kind="idle"] {
        background: #ebeff3;
        color: #55606d;
    }

    QLabel#statusBadge[kind="ready"] {
        background: #e4f2df;
        color: #2f5c35;
    }

    QLabel#statusBadge[kind="processing"] {
        background: #fff0c7;
        color: #7a560f;
    }

    QLabel#statusBadge[kind="success"] {
        background: #dff2e9;
        color: #20624b;
    }

    QLabel#statusBadge[kind="warning"] {
        background: #ffe5cf;
        color: #8a4a16;
    }

    QLabel#statusBadge[kind="error"] {
        background: #f8d9d4;
        color: #8a2f27;
    }

    QProgressBar {
        background: #ede2d0;
        border: 1px solid #d4c4ae;
        border-radius: 12px;
        color: #274150;
        min-height: 20px;
        padding: 2px;
        text-align: center;
    }

    QProgressBar::chunk {
        background:
            qlineargradient(
                x1: 0, y1: 0,
                x2: 1, y2: 0,
                stop: 0 #1c6253,
                stop: 0.6 #328270,
                stop: 1 #d27a42
            );
        border-radius: 9px;
    }

    QLabel#statusTitle {
        background: transparent;
        color: #20313e;
        font-size: 10pt;
        font-weight: 700;
    }

    QLabel#statusMessage {
        background: transparent;
        color: #243743;
        font-family: "Bahnschrift SemiBold", "Segoe UI Variable Display", "Segoe UI";
        font-size: 13pt;
        font-weight: 700;
    }

    QLabel#summaryLabel {
        background: transparent;
        color: #5e6873;
        font-size: 9.75pt;
        line-height: 1.45em;
    }

    QLabel#versionValue {
        background: transparent;
        color: #153f34;
        font-family: "Bahnschrift SemiBold", "Segoe UI Variable Display", "Segoe UI";
        font-size: 22pt;
        font-weight: 700;
    }

    QLabel#versionTitle {
        background: transparent;
        color: #20313e;
        font-size: 10pt;
        font-weight: 700;
    }

    QLabel#versionStatus {
        background: #efe2cc;
        border-radius: 12px;
        color: #5c4a32;
        font-size: 9pt;
        font-weight: 700;
        padding: 6px 10px;
    }

    QLabel#versionDetails {
        background: transparent;
        color: #66717c;
        font-size: 9.5pt;
    }

    QLabel#metricValue {
        background: transparent;
        font-family: "Bahnschrift SemiBold", "Segoe UI Variable Display", "Segoe UI";
        font-size: 21pt;
        font-weight: 700;
    }

    QLabel#metricTitle {
        background: transparent;
        color: #20313e;
        font-size: 10pt;
        font-weight: 700;
    }

    QLabel#metricDescription {
        background: transparent;
        color: #68727c;
        font-size: 9.25pt;
    }

    QPushButton {
        border-radius: 16px;
        font-weight: 700;
        padding: 12px 18px;
    }

    QPushButton#primaryButton {
        background: #153f34;
        border: 1px solid #11352b;
        color: #fffaf4;
    }

    QPushButton#primaryButton:hover {
        background: #1c5143;
    }

    QPushButton#primaryButton:disabled {
        background: #b7c1bc;
        border-color: #b7c1bc;
        color: #eef2ef;
    }

    QPushButton#secondaryButton {
        background: #fffaf2;
        border: 1px solid #cdbba2;
        color: #274150;
    }

    QPushButton#secondaryButton:hover {
        background: #f7eedf;
    }

    QPushButton#ghostButton {
        background: transparent;
        border: 1px dashed #c3b198;
        color: #5d4a32;
    }

    QPushButton#ghostButton:hover {
        background: rgba(255, 250, 242, 0.62);
    }

    QMessageBox {
        background: #fffaf2;
    }
    """
