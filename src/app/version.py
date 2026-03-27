from __future__ import annotations

from importlib import metadata
from pathlib import Path
import tomllib


PROJECT_NAME = "pdf-reader"
REPOSITORY_FULL_NAME = "Andrewsrj/pdf-reader"
REPOSITORY_URL = f"https://github.com/{REPOSITORY_FULL_NAME}"
REPOSITORY_RELEASES_URL = f"{REPOSITORY_URL}/releases"
FALLBACK_VERSION = "0.1.0"


def get_application_version() -> str:
    try:
        return metadata.version(PROJECT_NAME)
    except metadata.PackageNotFoundError:
        pass

    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    if pyproject_path.exists():
        with pyproject_path.open("rb") as file:
            project_data = tomllib.load(file)
        return str(project_data.get("project", {}).get("version", FALLBACK_VERSION))

    return FALLBACK_VERSION
