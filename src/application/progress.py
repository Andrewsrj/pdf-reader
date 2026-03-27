from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProgressUpdate:
    current: int
    total: int
    message: str

    @property
    def percent(self) -> int:
        if self.total <= 0:
            return 0
        return int((self.current / self.total) * 100)


@dataclass(slots=True)
class BatchStatistics:
    total_files: int = 0
    succeeded: int = 0
    failed: int = 0
