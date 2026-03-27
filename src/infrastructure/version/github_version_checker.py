from __future__ import annotations

from dataclasses import dataclass
from json import load
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.version import REPOSITORY_FULL_NAME, REPOSITORY_RELEASES_URL


LATEST_RELEASE_API_URL = f"https://api.github.com/repos/{REPOSITORY_FULL_NAME}/releases/latest"
LATEST_TAGS_API_URL = f"https://api.github.com/repos/{REPOSITORY_FULL_NAME}/tags?per_page=1"


@dataclass(frozen=True, slots=True)
class GitHubVersionInfo:
    current_version: str
    latest_version: str | None
    status: str
    message: str
    source_url: str = REPOSITORY_RELEASES_URL


def check_github_version(current_version: str, timeout: float = 4.0) -> GitHubVersionInfo:
    try:
        latest_release_payload = _fetch_json(LATEST_RELEASE_API_URL, timeout=timeout)
    except HTTPError as exc:
        if exc.code != 404:
            return GitHubVersionInfo(
                current_version=current_version,
                latest_version=None,
                status="unreachable",
                message="GitHub: nao foi possivel verificar a ultima versao agora.",
            )
        latest_release_payload = None
    except URLError:
        return GitHubVersionInfo(
            current_version=current_version,
            latest_version=None,
            status="unreachable",
            message="GitHub: nao foi possivel verificar a ultima versao agora.",
        )

    latest_version = _extract_latest_version(latest_release_payload)
    if latest_version is not None:
        return _build_version_comparison(current_version=current_version, latest_version=latest_version)

    try:
        latest_tags_payload = _fetch_json(LATEST_TAGS_API_URL, timeout=timeout)
    except (HTTPError, URLError):
        return GitHubVersionInfo(
            current_version=current_version,
            latest_version=None,
            status="unreachable",
            message="GitHub: nao foi possivel verificar a ultima versao agora.",
        )

    latest_version = _extract_latest_version(latest_tags_payload)
    if latest_version is None:
        return GitHubVersionInfo(
            current_version=current_version,
            latest_version=None,
            status="no_remote_version",
            message="GitHub: nenhuma release ou tag publicada ate o momento.",
        )

    return _build_version_comparison(current_version=current_version, latest_version=latest_version)


def _build_version_comparison(current_version: str, latest_version: str) -> GitHubVersionInfo:
    if _compare_versions(latest_version, current_version) > 0:
        return GitHubVersionInfo(
            current_version=current_version,
            latest_version=latest_version,
            status="update_available",
            message=f"GitHub: nova versao disponivel ({latest_version}).",
        )

    return GitHubVersionInfo(
        current_version=current_version,
        latest_version=latest_version,
        status="up_to_date",
        message=f"GitHub: build atualizada em relacao a {latest_version}.",
    )


def _fetch_json(url: str, timeout: float):
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "pdf-reader-version-checker",
        },
    )

    with urlopen(request, timeout=timeout) as response:
        return load(response)


def _extract_latest_version(payload) -> str | None:
    if payload is None:
        return None

    if isinstance(payload, dict):
        tag_name = str(payload.get("tag_name") or payload.get("name") or "").strip()
        return tag_name or None

    if isinstance(payload, list) and payload:
        first_tag = payload[0]
        if isinstance(first_tag, dict):
            tag_name = str(first_tag.get("name") or "").strip()
            return tag_name or None

    return None


def _compare_versions(left: str, right: str) -> int:
    left_parts = _version_parts(left)
    right_parts = _version_parts(right)
    max_length = max(len(left_parts), len(right_parts))

    padded_left = left_parts + (0,) * (max_length - len(left_parts))
    padded_right = right_parts + (0,) * (max_length - len(right_parts))

    if padded_left > padded_right:
        return 1
    if padded_left < padded_right:
        return -1
    return 0


def _version_parts(value: str) -> tuple[int, ...]:
    normalized = value.strip().lower()
    if normalized.startswith("v"):
        normalized = normalized[1:]

    matches = re.findall(r"\d+", normalized)
    if not matches:
        return (0,)

    return tuple(int(part) for part in matches)
