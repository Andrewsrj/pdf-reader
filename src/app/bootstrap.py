from __future__ import annotations

import logging
from collections.abc import Sequence

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QStyleFactory

from infrastructure.logging.logger import configure_logging
from ui.main_window import MainWindow
from ui.theme import build_application_stylesheet


def create_application(argv: Sequence[str] | None = None) -> tuple[QApplication, MainWindow]:
    """Create the Qt application and main window."""
    configure_logging()

    application = QApplication(list(argv or []))
    application.setApplicationName("Extrator de Notas PDF")
    application.setOrganizationName("pdf-reader")
    application.setStyle(QStyleFactory.create("Fusion"))
    application.setFont(QFont("Segoe UI", 10))
    application.setStyleSheet(build_application_stylesheet())

    logging.getLogger(__name__).debug("Qt application created.")

    window = MainWindow()
    return application, window
