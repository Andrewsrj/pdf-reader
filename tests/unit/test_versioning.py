from pathlib import Path
import tomllib
from urllib.error import HTTPError

from app.version import get_application_version
from infrastructure.version.github_version_checker import check_github_version


def test_get_application_version_matches_project_metadata() -> None:
    with Path("pyproject.toml").open("rb") as file:
        project_data = tomllib.load(file)

    assert get_application_version() == project_data["project"]["version"]


def test_check_github_version_reports_update_available(monkeypatch) -> None:
    def fake_fetch_json(url: str, timeout: float):
        assert timeout == 4.0
        return {"tag_name": "v0.2.0"}

    monkeypatch.setattr(
        "infrastructure.version.github_version_checker._fetch_json",
        fake_fetch_json,
    )

    result = check_github_version("0.1.0")

    assert result.status == "update_available"
    assert result.latest_version == "v0.2.0"


def test_check_github_version_handles_missing_release_and_missing_tags(monkeypatch) -> None:
    release_error = HTTPError(
        url="https://api.github.com/repos/Andrewsrj/pdf-reader/releases/latest",
        code=404,
        msg="Not Found",
        hdrs=None,
        fp=None,
    )

    def fake_fetch_json(url: str, timeout: float):
        if "releases/latest" in url:
            raise release_error
        return []

    monkeypatch.setattr(
        "infrastructure.version.github_version_checker._fetch_json",
        fake_fetch_json,
    )

    result = check_github_version("0.1.0")

    assert result.status == "no_remote_version"
    assert result.latest_version is None
    assert "nenhuma release ou tag publicada" in result.message
