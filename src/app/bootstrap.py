from __future__ import annotations

import logging
from collections.abc import Sequence

from PySide6.QtWidgets import QApplication

from infrastructure.logging.logger import configure_logging
from ui.main_window import MainWindow


def create_application(argv: Sequence[str] | None = None) -> tuple[QApplication, MainWindow]:
    """Create the Qt application and main window."""
    configure_logging()

    application = QApplication(list(argv or []))
    application.setApplicationName("Extrator de Notas PDF")
    application.setOrganizationName("pdf-reader")

    logging.getLogger(__name__).debug("Qt application created.")

    window = MainWindow()
    return application, window
