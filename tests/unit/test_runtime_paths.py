from pathlib import Path
from types import SimpleNamespace

from app.runtime_paths import get_runtime_base_dir, get_runtime_search_roots


def test_runtime_base_dir_defaults_to_repository_root() -> None:
    assert get_runtime_base_dir() == Path(__file__).resolve().parents[2]


def test_runtime_search_roots_include_executable_dir_when_frozen(monkeypatch) -> None:
    monkeypatch.setattr("app.runtime_paths.sys", SimpleNamespace(
        frozen=True,
        executable=r"C:\apps\pdf-reader\pdf-reader.exe",
        _MEIPASS=r"C:\apps\pdf-reader\_internal",
    ))

    roots = get_runtime_search_roots()

    assert roots == [
        Path(r"C:\apps\pdf-reader\_internal").resolve(),
        Path(r"C:\apps\pdf-reader").resolve(),
    ]
