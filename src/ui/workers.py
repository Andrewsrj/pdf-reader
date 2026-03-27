from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, QRunnable, Signal, Slot


class WorkerSignals(QObject):
    """Generic signals for background tasks."""

    started = Signal()
    progress = Signal(object)
    finished = Signal(object)
    failed = Signal(str)


class BackgroundTaskWorker(QRunnable):
    """Run a callable in a Qt thread pool."""

    def __init__(self, task: Callable[[Callable[[Any], None]], Any]) -> None:
        super().__init__()
        self._task = task
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        self._emit_safely(self.signals.started.emit)

        try:
            result = self._task(lambda payload: self._emit_safely(self.signals.progress.emit, payload))
        except Exception as exc:  # pragma: no cover - defensive UI path
            logging.getLogger(__name__).exception("Background task failed.")
            self._emit_safely(self.signals.failed.emit, str(exc))
            return

        self._emit_safely(self.signals.finished.emit, result)

    def _emit_safely(self, emitter: Callable[..., None], *args: Any) -> None:
        try:
            emitter(*args)
        except RuntimeError:  # pragma: no cover - UI teardown race
            logging.getLogger(__name__).debug("Signal emission skipped because the Qt object was already deleted.")
