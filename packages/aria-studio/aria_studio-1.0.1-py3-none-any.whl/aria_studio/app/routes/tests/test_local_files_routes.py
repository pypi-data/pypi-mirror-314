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

import os
from http import HTTPStatus
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Final
from unittest.mock import MagicMock, patch

import pytest
from aria_studio.app.routes.local_files_routes import router as app
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.asyncio
@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
async def test_delete_files_success(mock_get_instance):
    # Setup mock
    mock_file_manager = MagicMock()
    mock_file_manager.delete = MagicMock()
    mock_get_instance.return_value = mock_file_manager

    # Define the data for deleting files
    file_data = {
        "files_to_delete": [
            str(Path("/path/to/file1.vrs")),
            str(Path("/path/to/file2.vrs")),
        ]
    }

    # Make request
    response = client.post("/delete", json=file_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": f"{len(file_data['files_to_delete'])} file(s) deleted successfully."
    }


def test_delete_files_no_input():
    # Define empty data
    file_data = {}

    # Make request
    try:
        client.post("/delete", json=file_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "No files or folder is specified to delete."


@pytest.mark.asyncio
@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
@patch("pathlib.Path.glob")
async def test_delete_folder_success(mock_glob, mock_get_instance):
    # Setup mocks
    mock_file_manager = MagicMock()
    mock_file_manager.delete = MagicMock()
    mock_get_instance.return_value = mock_file_manager
    path_to_delete: Final[str] = "/path/to_delete"
    mock_glob.return_value = [
        Path(f"{path_to_delete}/file1.vrs"),
        Path(f"{path_to_delete}/file2.vrs"),
    ]

    # Define the data for deleting a folder
    file_data = {"path_to_delete": path_to_delete}

    # Make request
    response = client.post("/delete", json=file_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "2 file(s) deleted successfully."}


@pytest.mark.asyncio
@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
async def test_delete_files_unexpected_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_file_manager = MagicMock()
    mock_file_manager.delete.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_file_manager

    # Define the data for deleting files
    file_data = {"files_to_delete": [str(Path("/path/to/file1.vrs"))]}

    # Make request
    try:
        client.post("/delete", json=file_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert e.detail == "Unexpected error"


@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
def test_serve_thumbnail_jpeg_success(mock_get_instance):
    # Setup mock for os.stat to simulate a valid file stat result

    try:
        # Create a temporary file to simulate the thumbnail
        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file_path = tmp_file.name

        # Setup mock for LocalFileManager
        mock_file_manager = MagicMock()
        mock_file_manager.get_thumbnail_jpeg = MagicMock(return_value=tmp_file.name)
        mock_get_instance.return_value = mock_file_manager

        # Define the data for requesting a thumbnail
        media_data = {"file_path": "/path/to/media/file"}

        # Make request
        response = client.get("/thumbnail_jpeg", params=media_data)
        assert response.status_code == HTTPStatus.OK
        assert response.headers["content-type"] == "image/jpeg"
    finally:
        # Clean up the temporary file
        os.remove(tmp_file_path)


@pytest.mark.asyncio
@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
async def test_serve_thumbnail_jpeg_not_found(mock_get_instance):
    # Setup mock
    mock_file_manager = MagicMock()
    mock_file_manager.get_thumbnail_jpeg = MagicMock(return_value=None)
    mock_get_instance.return_value = mock_file_manager

    # Define the data for requesting a thumbnail
    media_data = {"file_path": "/path/to/nonexistent/file"}

    # Make request
    try:
        client.get("/thumbnail_jpeg", params=media_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.NOT_FOUND
        assert e.detail == "Thumbnail not found"


@pytest.mark.asyncio
@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
async def test_serve_thumbnail_jpeg_unexpected_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_file_manager = MagicMock()
    mock_file_manager.get_thumbnail_jpeg.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_file_manager

    # Define the data for requesting a thumbnail
    media_data = {"file_path": "/path/to/file"}

    # Make request
    try:
        client.get("/thumbnail_jpeg", params=media_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert e.detail == "Unexpected error"


@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
def test_get_file_details_success(mock_get_instance):
    # Setup mock
    mock_file_manager = MagicMock()
    mock_file_manager.get_metadata = MagicMock(
        return_value={"size": 1024, "created": "2021-01-01"}
    )
    mock_get_instance.return_value = mock_file_manager

    # Define the data for requesting file details
    file_path = "/path/to/file.vrs"

    # Make request
    response = client.get(f"/details?vrs_path={file_path}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"size": 1024, "created": "2021-01-01"}


@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
def test_get_file_details_invalid_path(mock_get_instance):
    # Setup mock
    mock_file_manager = MagicMock()
    mock_file_manager.get_metadata.side_effect = FileNotFoundError("File not found")
    mock_get_instance.return_value = mock_file_manager

    # Define the data for requesting file details
    file_path = "/path/to/nonexistent/file.vrs"

    # Make request
    try:
        client.get(f"/details?vrs_path={file_path}")
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert e.detail == "File not found"


@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
def test_get_file_details_unexpected_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_file_manager = MagicMock()
    mock_file_manager.get_metadata.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_file_manager

    # Define the data for requesting file details
    file_path = "/path/to/file.vrs"

    # Make request
    try:
        client.get(f"/details?vrs_path={file_path}")
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert e.detail == "Unexpected error"


@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
@patch("pathlib.Path.is_dir", return_value=True)
def test_local_files_success(mock_is_dir, mock_get_instance):
    # Setup mock
    mock_file_manager = MagicMock()
    mock_file_manager.get_metadata_on_folder = MagicMock(
        return_value=[{"file_name": "file1.vrs", "size": 1024}]
    )
    mock_get_instance.return_value = mock_file_manager

    # Define the data for requesting file details
    file_data = {"path": "/path/to/directory"}

    # Make request
    response = client.post("/files", json=file_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [{"file_name": "file1.vrs", "size": 1024}],
    }


@patch("pathlib.Path.is_dir", return_value=False)
def test_local_files_invalid_directory(mock_is_dir):
    # Define the data for requesting file details
    file_data = {"path": "/path/to/nonexistent/directory"}

    # Make request
    try:
        client.post("/files", json=file_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.NOT_FOUND
        assert e.detail == "Directory not found"


@patch("aria_studio.app.routes.local_files_routes.LocalFileManager.get_instance")
@patch("pathlib.Path.is_dir", return_value=True)
def test_local_files_unexpected_exception(mock_is_dir, mock_get_instance):
    # Setup mock to raise an exception
    mock_file_manager = MagicMock()
    error_msg: Final[str] = "Unexpected error"
    mock_file_manager.get_metadata_on_folder.side_effect = Exception(error_msg)
    mock_get_instance.return_value = mock_file_manager

    # Define the data for requesting file details
    file_data = {"path": "/path/to/directory"}

    # Make request
    try:
        client.post("/files", json=file_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert e.detail == error_msg


@patch("os.environ.get")
@patch("asyncio.create_task")
def test_view_vrs(mock_create_task, mock_get, monkeypatch):
    mock_get.return_value = True
    mock_task = MagicMock()
    mock_create_task.return_value = mock_task

    request = {"file_path": "some_file"}
    monkeypatch.setattr(Path, "is_file", lambda self: True)
    response = client.post("/view_vrs", json=request)

    assert response.status_code == HTTPStatus.OK
    mock_create_task.assert_called_once()


def test_view_vrs_missing_filename():
    # Define empty data
    media_data = {}

    # Make request
    try:
        client.post("/view_vrs", json=media_data)
        raise AssertionError
    except RequestValidationError as e:
        assert isinstance(e, RequestValidationError)  # Dummy operation


@patch("pathlib.Path.is_file", return_value=False)
def test_view_vrs_file_not_found(mock_is_file):
    # Define the data for a non-existent file
    media_data = {"file_path": "/path/to/nonexistent/file.vrs"}

    # Make request
    try:
        client.post("/view_vrs", json=media_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.NOT_FOUND
        assert e.detail == f"{media_data['file_path']} file not found"
