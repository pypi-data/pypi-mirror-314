# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import MagicMock, patch

import pytest
from aria_studio.app.routes.app_routes import (
    _DEFAULT_VERSION,
    _SUFFIX_DEVELOPMENT,
    _VERSION_FILE,
    router as app,
)

from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def version_file(tmp_path):
    # Create a temporary version file for testing
    version_file = tmp_path / "VERSION"
    return version_file


def test_check_version_status_code():
    # Test to ensure that the endpoint returns a 200 OK status code
    response = client.get("/version")
    assert response.status_code == status.HTTP_200_OK


def test_check_version_with_version_file(version_file):
    # Test to check the version endpoint when a version file exists
    TEST_VERSION = "0.1.0b1"
    version_file.write_text(TEST_VERSION)
    with patch("aria_studio.app.routes.app_routes._VERSION_FILE", version_file):
        response = client.get("/version")
    assert response.json()["version"] == TEST_VERSION + _SUFFIX_DEVELOPMENT


def test_check_version_without_version_file(version_file):
    # Test to check the version endpoint when no version file exists
    if version_file.exists():
        version_file.unlink()
    with patch("aria_studio.app.routes.app_routes._VERSION_FILE", version_file):
        response = client.get("/version")
    assert response.json()["version"] == _DEFAULT_VERSION


def test_check_version_with_pip_failure(version_file):
    # Test to simulate a failure in fetching the version via pip and no version file exists
    mock_process = MagicMock()

    async def mock_communicate():
        return (b"", b"pip3 show aria_studio failed")  # stdout, stderr

    mock_process.communicate = mock_communicate
    mock_process.returncode = 1  # Non-zero return code indicates failure
    with patch("asyncio.create_subprocess_exec", return_value=mock_process), patch(
        "pathlib.Path.is_file", return_value=False
    ):  # Mock is_file to always return False
        response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == _DEFAULT_VERSION


def test_check_version_with_pip_success():
    # Test to simulate a successful fetch of the version via pip
    mock_process = MagicMock()

    async def mock_communicate():
        return (b"Name: aria_studio\nVersion: 0.1.0b1\n", b"")

    mock_process.communicate = mock_communicate
    mock_process.returncode = 0
    with patch("asyncio.create_subprocess_exec", return_value=mock_process):
        response = client.get("/version")

    if _VERSION_FILE.is_file():
        with open(_VERSION_FILE, "r") as fp:
            version = f"{fp.read().strip()}{_SUFFIX_DEVELOPMENT}"

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["version"] == version


def test_clear_cache():
    response = client.get("/clear_cache")
    assert response.status_code == 200
    assert response.json()["message"] == "Cache cleared"


def test_clear_cache_permission_error(monkeypatch):
    with patch("os.path.exists", return_value=True), patch(
        "shutil.rmtree", side_effect=PermissionError("Test error")
    ):
        response = client.get("/clear_cache")
    assert response.status_code == 200
    assert response.json()["message"] == "Error deleting cache directory: Test error"
