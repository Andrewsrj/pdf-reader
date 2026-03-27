from __future__ import annotations

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app.version import REPOSITORY_URL, get_application_version

AUTHOR_NAME = "Andrews Costa"


class AboutDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Sobre o autor")
        self.setModal(True)
        self.resize(460, 280)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(22, 22, 22, 22)
        root_layout.setSpacing(16)

        card = QFrame(self)
        card.setObjectName("panelCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(14)

        eyebrow = QLabel("Projeto open source")
        eyebrow.setObjectName("heroEyebrow")
        eyebrow.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        title = QLabel("Extrator de Notas Fiscais em PDF")
        title.setObjectName("sectionTitle")

        description = QLabel(
            "Aplicacao desktop para OCR, extracao, consolidacao e exportacao de notas fiscais em Excel."
        )
        description.setObjectName("sectionDescription")
        description.setWordWrap(True)

        version_label = QLabel(f"<b>Versao atual:</b> {get_application_version()}")
        version_label.setObjectName("summaryLabel")
        version_label.setTextFormat(Qt.TextFormat.RichText)

        author_label = QLabel(f"<b>Autor:</b> {AUTHOR_NAME}")
        author_label.setObjectName("summaryLabel")
        author_label.setTextFormat(Qt.TextFormat.RichText)

        repository_label = QLabel(
            f'<b>Repositorio:</b> <a href="{REPOSITORY_URL}">{REPOSITORY_URL}</a>'
        )
        repository_label.setObjectName("summaryLabel")
        repository_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        repository_label.setOpenExternalLinks(True)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        open_repository_button = QPushButton("Abrir repositorio")
        open_repository_button.setObjectName("secondaryButton")
        open_repository_button.clicked.connect(self._open_repository)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)

        actions_layout.addWidget(open_repository_button)
        actions_layout.addStretch(1)
        actions_layout.addWidget(button_box)

        card_layout.addWidget(eyebrow)
        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addWidget(version_label)
        card_layout.addWidget(author_label)
        card_layout.addWidget(repository_label)
        card_layout.addStretch(1)
        card_layout.addLayout(actions_layout)

        root_layout.addWidget(card)

    def _open_repository(self) -> None:
        QDesktopServices.openUrl(QUrl(REPOSITORY_URL))
