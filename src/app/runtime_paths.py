from __future__ import annotations

import sys
from pathlib import Path


def get_runtime_base_dir() -> Path:
    """Return the base directory that contains bundled resources at runtime."""
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass).resolve()
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[2]


def get_runtime_search_roots() -> list[Path]:
    roots = [get_runtime_base_dir()]

    if getattr(sys, "frozen", False):
        executable_dir = Path(sys.executable).resolve().parent
        if executable_dir not in roots:
            roots.append(executable_dir)

    return roots
