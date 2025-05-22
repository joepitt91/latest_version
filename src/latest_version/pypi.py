# SPDX-FileCopyrightText: 2025 Joe Pitt
#
# SPDX-License-Identifier: GPL-3.0-only

"""Get latest version information from PIP module on PyPI."""

from requests import get


def get_current_module_version(module: str) -> str:
    """Get the current version of the specified PIP module.

    Args:
        package (str): The module to check.

    Raises:
        HTTPError: If communication with PyPI fails

    Returns:
        str: The current version of the module.
    """

    response = get(f"https://pypi.org/pypi/{module}/json", timeout=10)
    response.raise_for_status()

    return response.json()["info"]["version"]
