<!--
SPDX-FileCopyrightText: 2025 Joe Pitt

SPDX-License-Identifier: GPL-3.0-only
-->
# Latest Version

Python module to get the latest version for various package types.

All package sources, except PyPI support passing a minimum and maximum version to constrain results.

## Usage

```sh
pip install get_latest_version
```

### Digest of current `latest` Ubuntu image

```python
from get_latest_version.dockerhub import get_current_image_digest

print(get_current_image_digest(USERNAME, DOCKER_HUB_TOKEN, "ubuntu"))
```

### Latest available version of the Nextcloud AIO image

```python
from get_latest_version.dockerhub import get_latest_image_version

print(get_latest_image_version(USERNAME, DOCKER_HUB_TOKEN, "nextcloud"))
```

### Latest version of Matrix Authentication Service based on GitHub Container Registry versions

```python
from get_latest_version.github import get_latest_version_from_package

print(get_latest_version_from_package(GITHUB_PAT, "element-hq", "matrix-authentication-service"))
```

### Latest version of the ComfyUI based on GitHub releases

```python
from get_latest_version.github import get_latest_version_from_releases

print(get_latest_version_from_releases(GITHUB_PAT, "comfyanonymous", "ComfyUI"))
```

### Latest version of the ComfyUI based on GitHub tags

```python
from get_latest_version.github import get_latest_version_from_tags

print(get_latest_version_from_tags(GITHUB_PAT, "comfyanonymous", "ComfyUI"))
```

### Latest version of the requests from on PyPI

```python
from get_latest_version.pypi import get_current_module_version

print(get_current_module_version("requests"))
```
