from pathlib import Path

from app.user_settings import UserSettings, load_user_settings, save_user_settings


def test_user_settings_roundtrip(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("APPDATA", str(tmp_path))

    save_user_settings(UserSettings(tesseract_cmd=r"C:\OCR\tesseract.exe"))
    loaded_settings = load_user_settings()

    assert loaded_settings.tesseract_cmd == r"C:\OCR\tesseract.exe"
