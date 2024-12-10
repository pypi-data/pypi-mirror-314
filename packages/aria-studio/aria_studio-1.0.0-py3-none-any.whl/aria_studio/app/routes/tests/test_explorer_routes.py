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
from aria_studio.app.constants import (
    MESSAGE_DIRECTORY_NOT_FOUND,
    MESSAGE_INVALID_JSON,
    PERMISSION_DENIED,
)
from aria_studio.app.routes.explorer_routes import router as app
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.asyncio
async def test_file_explorer_success():
    path = "/mock/path"
    # Use a fixed timestamp string for simplicity
    expected_last_modified = "2021-01-01T05:30:00"

    with patch("pathlib.Path.exists", return_value=True), patch(
        "pathlib.Path.iterdir"
    ) as mock_iterdir, patch("os.path.getmtime", return_value=1609459200):
        mock_file = MagicMock()
        mock_file.is_file.return_value = True
        mock_file.is_dir.return_value = False
        mock_file.name = "testfile.txt"

        mock_dir = MagicMock()
        mock_dir.is_file.return_value = False
        mock_dir.is_dir.return_value = True
        mock_dir.name = "testdir"

        mock_iterdir.return_value = [mock_file, mock_dir]

        response = client.post("/file-explorer", json={"path": path})
        assert response.status_code == status.HTTP_200_OK
        expected_response = {
            "current_path": path,
            "files": [
                {"name": "testfile.txt", "last_modified": expected_last_modified}
            ],
            "directories": [
                {"name": "testdir", "last_modified": expected_last_modified}
            ],
        }
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_file_explorer_invalid_json():
    try:
        client.post("/file-explorer", data="{invalid_json}")
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == status.HTTP_400_BAD_REQUEST
        assert e.detail == MESSAGE_INVALID_JSON


@pytest.mark.asyncio
async def test_file_explorer_directory_not_found():
    with patch("pathlib.Path.exists", return_value=False):
        try:
            client.post("/file-explorer", json={"path": "/non/existent/path"})
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_404_NOT_FOUND
            assert e.detail == MESSAGE_DIRECTORY_NOT_FOUND


@pytest.mark.asyncio
async def test_file_explorer_permission_denied():
    with patch("pathlib.Path.exists", return_value=True), patch(
        "pathlib.Path.iterdir", side_effect=PermissionError
    ):
        try:
            client.post("/file-explorer", json={"path": "/restricted/path"})
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_403_FORBIDDEN
            assert e.detail == PERMISSION_DENIED
