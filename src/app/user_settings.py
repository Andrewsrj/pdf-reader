from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path


APP_SETTINGS_FOLDER = "pdf-reader"
SETTINGS_FILENAME = "settings.json"


@dataclass(slots=True)
class UserSettings:
    tesseract_cmd: str | None = None


def get_settings_dir() -> Path:
    appdata_dir = os.getenv("APPDATA")
    if appdata_dir:
        return Path(appdata_dir) / APP_SETTINGS_FOLDER

    return Path.home() / f".{APP_SETTINGS_FOLDER}"


def get_settings_path() -> Path:
    return get_settings_dir() / SETTINGS_FILENAME


def load_user_settings() -> UserSettings:
    settings_path = get_settings_path()
    if not settings_path.exists():
        return UserSettings()

    try:
        with settings_path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return UserSettings()

    if not isinstance(raw_data, dict):
        return UserSettings()

    configured_cmd = raw_data.get("tesseract_cmd")
    if configured_cmd is not None:
        configured_cmd = str(configured_cmd)

    return UserSettings(tesseract_cmd=configured_cmd)


def save_user_settings(settings: UserSettings) -> Path:
    settings_path = get_settings_path()
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    with settings_path.open("w", encoding="utf-8") as file:
        json.dump(asdict(settings), file, indent=2, ensure_ascii=True)

    return settings_path
