# SPDX-FileCopyrightText: 2025 Joe Pitt
#
# SPDX-License-Identifier: GPL-3.0-only

"""Get latest version information from GitHub packages and repositories."""

from typing import Dict, Literal, Optional, Union

from semver import Version
from requests import get

from .__version__ import __version__
from .functions import clean_version, find_latest


def get_latest_version_from_package(  # pylint: disable=too-many-arguments
    token: str,
    owner: str,
    package_name: str,
    package_type: Literal[
        "npm", "maven", "rubygems", "docker", "nuget", "container"
    ] = "container",
    *,
    minimum_version: Optional[Version] = None,
    maximum_version: Optional[Version] = None,
) -> str:
    """Get the latest version from a package.

    Args:
        token (str): The token to authenticate to GitHub with.
        owner (str): The owner of the package.
        package_name (str): The name of the package to query.
        package_type (Literal[npm, maven, rubygems, docker, nuget, container ], optional):
            The type of package to query. Defaults to "container".
        minimum_version (Optional[Version], optional): The minimum version to accept.
                                                            Defaults to None.
        maximum_version (Optional[Version], optional): The maximum version to accept.
                                                            Defaults to None.

    Raises:
        HTTPError: If communication with GitHub fails.
        ValueError: If no semantic versions could be found.

    Returns:
        str: The latest version of the package.
    """

    semantic_versions: Dict[str, Version] = {}
    response = get(
        f"https://api.github.com/users/{owner}/packages/{package_type}/{package_name}/versions",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": f"Python get_latest_version/v{__version__}",
        },
        timeout=10,
    )
    response.raise_for_status()

    versions: Dict[str, Union[str, Dict[str, str]]] = response.json()
    for version in versions:
        try:
            semantic_version = Version.parse(clean_version(version["name"]))
            if (minimum_version is not None and semantic_version < minimum_version) or (
                maximum_version is not None and semantic_version > maximum_version
            ):
                continue
            semantic_versions[version["name"]] = semantic_version
        except (TypeError, ValueError):
            continue

    return find_latest(semantic_versions)


def get_latest_version_from_releases(
    token: str,
    owner: str,
    repository: str,
    *,
    minimum_version: Optional[Version] = None,
    maximum_version: Optional[Version] = None,
) -> str:
    """Get the latest version from the releases in a GitHub repository.

    Args:
        token (str): The token to authenticate to GitHub API with.
        owner (str): The owner of the source repository.
        repository (str): The name of the source repository.
        minimum_version (Optional[Version], optional): The minimum version number to accept.
                                                            Defaults to None.
        maximum_version (Optional[Version], optional): The maximum version number to accept.
                                                            Defaults to None.

    Raises:
        HTTPError: if communication with GitHub fails.
        ValueError: If no semantic versions can be found.

    Returns:
        str: The name of the release of the latest version.
    """

    semantic_versions: Dict[str, Version] = {}
    response = get(
        f"https://api.github.com/repos/{owner}/{repository}/releases",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": f"Python get_latest_version/v{__version__}",
        },
        timeout=10,
    )
    response.raise_for_status()

    releases: Dict[str, Union[str, Dict[str, str]]] = response.json()
    for release in releases:
        if release["draft"]:
            continue
        try:
            semantic_version = Version.parse(clean_version(release["name"]))
        except (TypeError, ValueError):
            try:
                semantic_version = Version.parse(clean_version(release["tag_name"]))
            except (TypeError, ValueError):
                continue
        if (minimum_version is not None and semantic_version < minimum_version) or (
            maximum_version is not None and semantic_version > maximum_version
        ):
            continue
        semantic_versions[release["name"]] = semantic_version

    return find_latest(semantic_versions)


def get_latest_version_from_tags(
    token: str,
    owner: str,
    repository: str,
    *,
    minimum_version: Optional[Version] = None,
    maximum_version: Optional[Version] = None,
) -> str:
    """Get the latest version from the tags in a GitHub repository.

    Args:
        token (str): The token to authenticate to GitHub API with.
        owner (str): The owner of the source repository.
        repository (str): The name of the source repository.
        minimum_version (Optional[Version], optional): The minimum version number to accept.
                                                            Defaults to None.
        maximum_version (Optional[Version], optional): The maximum version number to accept.
                                                            Defaults to None.

    Raises:
        HTTPError: if communication with GitHub fails.
        ValueError: If no semantic versions can be found.

    Returns:
        str: The tag of the latest version.
    """

    semantic_versions: Dict[str, Version] = {}
    response = get(
        f"https://api.github.com/repos/{owner}/{repository}/tags",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": f"Python get_latest_version/v{__version__}",
        },
        timeout=10,
    )
    response.raise_for_status()

    tags: Dict[str, Union[str, Dict[str, str]]] = response.json()
    for tag in tags:
        try:
            semantic_version = Version.parse(clean_version(tag["name"]))
            if (minimum_version is not None and semantic_version < minimum_version) or (
                maximum_version is not None and semantic_version > maximum_version
            ):
                continue
            semantic_versions[tag["name"]] = semantic_version
        except (TypeError, ValueError):
            pass

    return find_latest(semantic_versions)
