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
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aria_studio.app.constants import (
    KEY_END_TIME,
    KEY_ERROR,
    KEY_FILE_NAME,
    KEY_FILE_SIZE,
    KEY_RECORDING_PROFILE,
    KEY_START_TIME,
    MESSAGE_DEVICE_NOT_CONNECTED,
    MESSAGE_FILE_NOT_FOUND,
)
from aria_studio.app.device.device_manager import AriaError, AriaException
from aria_studio.app.routes.device_routes import router as app
from fastapi import HTTPException, status
from fastapi.testclient import TestClient


client = TestClient(app)


def test_device_connected_success():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = MagicMock()
        mock_device_manager.check_device_connected = AsyncMock(return_value=True)
        mock_get_instance.return_value = mock_device_manager

        response = client.get("/connected")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()  # Expect True directly


def test_device_connected_failure():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = MagicMock()
        mock_device_manager.check_device_connected = AsyncMock(
            side_effect=AriaException("Connection error")
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.get("/connected")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_device_status_success():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = MagicMock()
        mock_device_manager.get_status = AsyncMock(
            return_value=MagicMock(
                serial_number="123456",
                wifi_ssid="TestSSID",
                battery_level=85,
                import_in_progress=False,
            )
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.get("/status")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "serial_number": "123456",
            "wifi_ssid": "TestSSID",
            "battery_level": 85,
            "import_in_progress": False,
        }


@pytest.mark.asyncio
async def test_status_device_not_connected():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = MagicMock()
        mock_device_manager.get_status = AsyncMock(
            side_effect=AriaException(error_code=AriaError.DEVICE_NOT_CONNECTED)
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.get("/status")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None


@pytest.mark.asyncio
async def test_device_status_throws_exception():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        try:
            mock_device_manager = MagicMock()
            mock_device_manager.get_status = AsyncMock(
                side_effect=AriaException("Unexpected error")
            )
            mock_get_instance.return_value = mock_device_manager
            client.get("/status")
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST
            assert "Failed to get device status" in e.detail


@pytest.mark.asyncio
async def test_delete_files_success():
    files_to_delete = ["file1.vrs", "file2.vrs"]
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.delete_files = AsyncMock(return_value=None)
        mock_get_instance.return_value = mock_device_manager

        response = client.post(
            "/delete-files", json={"files_to_delete": files_to_delete}
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_files_throws_exception():
    files_to_delete = ["nonexistentfile.vrs"]
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        try:
            mock_device_manager = AsyncMock()
            mock_device_manager.delete_files = AsyncMock(
                side_effect=Exception("Deletion failed")
            )
            mock_get_instance.return_value = mock_device_manager

            client.post("/delete-files", json={"files_to_delete": files_to_delete})
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST
            assert "Deletion failed" in e.detail


@pytest.mark.asyncio
async def test_import_progress_success():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = MagicMock()
        # Create file mocks with proper string names
        current_files = [MagicMock(), MagicMock(), MagicMock()]
        copied_files = [MagicMock(), MagicMock(), MagicMock()]
        deleted_files = [MagicMock(), MagicMock(), MagicMock()]
        error_files = [MagicMock(), MagicMock(), MagicMock()]

        # Set the name attribute to return a string directly
        for i, file in enumerate(current_files):
            file.name = f"current_file{i}.vrs"
        for i, file in enumerate(copied_files):
            file.name = f"copied_file{i}.vrs"
        for i, file in enumerate(deleted_files):
            file.name = f"deleted_file{i}.vrs"
        for i, file in enumerate(error_files):
            file.name = f"error_file{i}.vrs"

        # Set the return value of get_copy_progress
        mock_device_manager.get_copy_progress.return_value = MagicMock(
            current_files=current_files,
            copied_files=copied_files,
            deleted_files=deleted_files,
            total_files=3,
            copied_bytes=1024,
            total_bytes=2048,
            error=None,
            error_files=error_files,
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.get("/import-progress")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "current_files": [
                "current_file0.vrs",
                "current_file1.vrs",
                "current_file2.vrs",
            ],
            "copied_files": [
                "copied_file0.vrs",
                "copied_file1.vrs",
                "copied_file2.vrs",
            ],
            "deleted_files": [
                "deleted_file0.vrs",
                "deleted_file1.vrs",
                "deleted_file2.vrs",
            ],
            "total_files": 3,
            "copied_bytes": 1024,
            "total_bytes": 2048,
            "error": None,
            "error_files": ["error_file0.vrs", "error_file1.vrs", "error_file2.vrs"],
        }


@pytest.mark.asyncio
async def test_import_progress_no_import_in_progress():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        try:
            mock_device_manager = MagicMock()
            mock_device_manager.get_copy_progress.side_effect = AriaException(
                "No import in progress"
            )
            mock_get_instance.return_value = mock_device_manager

            client.get("/import-progress")
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_cancel_import_success():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.cancel_copy = AsyncMock(return_value=None)
        mock_get_instance.return_value = mock_device_manager

        response = client.post("/cancel-import")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"success": True}


@pytest.mark.asyncio
async def test_cancel_import_no_import_in_progress():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        try:
            mock_device_manager = AsyncMock()
            mock_device_manager.cancel_copy.side_effect = AriaException(
                "No import in progress"
            )
            mock_get_instance.return_value = mock_device_manager
            client.post("/cancel-import")
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_cancel_import_no_import_in_progress_raise_ariaerror():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.cancel_copy.side_effect = AriaException(
            error_code=AriaError.VRS_PULL_NOT_STARTED
        )
        mock_get_instance.return_value = mock_device_manager
        response = client.post("/cancel-import")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"success": False}


@pytest.mark.asyncio
async def test_cancel_import_other_exception():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.cancel_copy.side_effect = Exception("Unexpected error")
        mock_get_instance.return_value = mock_device_manager

        try:
            client.post("/cancel-import")
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST
            assert "Unexpected error" in e.detail


@pytest.mark.asyncio
async def test_thumbnail_jpeg_success():
    vrs_file = "test_file.vrs"
    # Create a temporary file to simulate the thumbnail
    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file_path = tmp_file.name

    try:
        with patch(
            "aria_studio.app.device.device_manager.DeviceManager.get_instance"
        ) as mock_get_instance:
            mock_device_manager = AsyncMock()
            # Use the path of the temporary file
            mock_device_manager.get_thumbnail_jpeg = AsyncMock(
                return_value=tmp_file_path
            )
            mock_get_instance.return_value = mock_device_manager

            response = client.get(f"/thumbnail_jpeg/{vrs_file}")
            assert response.status_code == status.HTTP_200_OK
            assert response.headers["content-type"] == "image/jpeg"
    finally:
        # Clean up the temporary file
        os.remove(tmp_file_path)


@pytest.mark.asyncio
async def test_thumbnail_jpeg_device_not_connected():
    vrs_file = "test_file.vrs"
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.get_thumbnail_jpeg.side_effect = AriaException(
            error_code=AriaError.DEVICE_NOT_CONNECTED
        )
        mock_get_instance.return_value = mock_device_manager
        response = client.get(f"/thumbnail_jpeg/{vrs_file}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {KEY_ERROR: MESSAGE_DEVICE_NOT_CONNECTED}


@pytest.mark.asyncio
async def test_thumbnail_jpeg_file_not_found():
    vrs_file = "nonexistent_file.vrs"
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.get_thumbnail_jpeg.side_effect = Exception("File not found")
        mock_get_instance.return_value = mock_device_manager

        response = client.get(f"/thumbnail_jpeg/{vrs_file}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {KEY_ERROR: MESSAGE_FILE_NOT_FOUND}


@pytest.mark.asyncio
async def test_thumbnail_gif_success():
    vrs_file = "test_file.vrs"
    # Create a temporary file with a .gif extension to simulate the thumbnail
    with NamedTemporaryFile(delete=False, suffix=".gif") as tmp_file:
        tmp_file_path = tmp_file.name

    try:
        with patch(
            "aria_studio.app.device.device_manager.DeviceManager.get_instance"
        ) as mock_get_instance:
            mock_device_manager = AsyncMock()
            mock_device_manager.get_thumbnail_gif = AsyncMock(
                return_value=tmp_file_path
            )
            mock_get_instance.return_value = mock_device_manager

            response = client.get(f"/thumbnail_gif/{vrs_file}")
            assert response.status_code == status.HTTP_200_OK
            assert response.headers["content-type"] == "image/gif"
    finally:
        # Clean up the temporary file
        os.remove(tmp_file_path)


@pytest.mark.asyncio
async def test_thumbnail_gif_device_not_connected():
    vrs_file = "test_file.vrs"
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.get_thumbnail_gif.side_effect = AriaException(
            error_code=AriaError.DEVICE_NOT_CONNECTED
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.get(f"/thumbnail_gif/{vrs_file}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {KEY_ERROR: MESSAGE_DEVICE_NOT_CONNECTED}


@pytest.mark.asyncio
async def test_thumbnail_gif_file_not_found():
    vrs_file = "nonexistent_file.vrs"
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.get_thumbnail_gif.side_effect = Exception("File not found")
        mock_get_instance.return_value = mock_device_manager

        response = client.get(f"/thumbnail_gif/{vrs_file}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {KEY_ERROR: MESSAGE_FILE_NOT_FOUND}


# Mock class for authentication helper
class MockCliAuthHelper:
    instance = None

    def __init__(self):
        self._user = "test_user"
        self._auth_token = "test_token"
        MockCliAuthHelper.instance = self

    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def is_logged_in(self):
        return True


# Fixture to mock authentication helper
@pytest.fixture
def mock_auth_helper(monkeypatch):
    monkeypatch.setattr(
        "aria_studio.app.utils.CliAuthHelper.get", MockCliAuthHelper.get
    )


@pytest.mark.usefixtures("mock_auth_helper")
@pytest.mark.asyncio
async def test_import_files_success():
    request_data = {
        "files_to_import": ["file1.vrs", "file2.vrs"],
        "destination_path": "/destination",
        "delete": True,
    }
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        # Create file mocks with proper string names
        current_files = [MagicMock(), MagicMock()]
        copied_files = [MagicMock(), MagicMock()]
        deleted_files = [MagicMock(), MagicMock()]
        error_files = [MagicMock(), MagicMock()]

        # Set the name attribute to return a string directly
        for i, file in enumerate(current_files):
            file.name = f"current_file{i}.vrs"
        for i, file in enumerate(copied_files):
            file.name = f"copied_file{i}.vrs"
        for i, file in enumerate(deleted_files):
            file.name = f"deleted_file{i}.vrs"
        for i, file in enumerate(error_files):
            file.name = f"error_file{i}.vrs"

        # Set the return value of get_copy_progress
        mock_device_manager.get_copy_progress = MagicMock(
            return_value=MagicMock(
                current_files=current_files,
                copied_files=copied_files,
                deleted_files=deleted_files,
                total_files=2,
                copied_bytes=1024,
                total_bytes=2048,
                error=None,
                error_files=error_files,
            )
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.post("/import-files", json=request_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "current_files": ["current_file0.vrs", "current_file1.vrs"],
            "copied_files": ["copied_file0.vrs", "copied_file1.vrs"],
            "deleted_files": ["deleted_file0.vrs", "deleted_file1.vrs"],
            "total_files": 2,
            "copied_bytes": 1024,
            "total_bytes": 2048,
            "error": None,
            "error_files": ["error_file0.vrs", "error_file1.vrs"],
        }
        # Check if delete_files was called
        mock_device_manager.start_copy_vrs_files.assert_called_once_with(
            ["file1.vrs", "file2.vrs"],
            destination=Path("/destination"),
            delete_src_after_copy=True,
        )


@pytest.mark.asyncio
async def test_import_files_in_progress_exception():
    request_data = {
        "files_to_import": ["file1.vrs"],
        "destination_path": "/destination",
        "delete": False,
    }
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.start_copy_vrs_files.side_effect = AriaException(
            "Import already in progress"
        )
        mock_get_instance.return_value = mock_device_manager

        try:
            client.post("/import-files", json=request_data)
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_import_files_file_exists_error():
    request_data = {
        "files_to_import": ["existing_file.vrs"],
        "destination_path": "/destination",
        "delete": True,
    }
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.start_copy_vrs_files.side_effect = FileExistsError(
            "File already exists"
        )
        mock_get_instance.return_value = mock_device_manager

        try:
            client.post("/import-files", json=request_data)
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_409_CONFLICT
            assert e.detail == "File already exists"


@pytest.mark.asyncio
async def test_list_files_success():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        # Create MagicMock objects with the name attribute correctly set
        file1 = MagicMock()
        file1.name = "file1.vrs"
        file2 = MagicMock()
        file2.name = "file2.vrs"

        mock_device_manager.list_vrs_files = AsyncMock(return_value=[file1, file2])
        mock_device_manager.get_metadata = AsyncMock(
            side_effect=[
                {
                    KEY_START_TIME: 1609459200,
                    KEY_END_TIME: 1609462800,
                    KEY_FILE_SIZE: 1024,
                    KEY_RECORDING_PROFILE: "profile1",
                },
                {
                    KEY_START_TIME: 1609462800,
                    KEY_END_TIME: 1609466400,
                    KEY_FILE_SIZE: 2048,
                    KEY_RECORDING_PROFILE: "profile2",
                },
            ]
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.get("/list-files")
        assert response.status_code == status.HTTP_200_OK
        expected_response = {
            "count": 2,
            "results": [
                {
                    KEY_FILE_NAME: "file1.vrs",
                    KEY_START_TIME: 1609459200,
                    KEY_END_TIME: 1609462800,
                    KEY_FILE_SIZE: 1024,
                    KEY_RECORDING_PROFILE: "profile1",
                },
                {
                    KEY_FILE_NAME: "file2.vrs",
                    KEY_START_TIME: 1609462800,
                    KEY_END_TIME: 1609466400,
                    KEY_FILE_SIZE: 2048,
                    KEY_RECORDING_PROFILE: "profile2",
                },
            ],
        }
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_list_files_device_not_connected():
    with patch(
        "aria_studio.app.device.device_manager.DeviceManager.get_instance"
    ) as mock_get_instance:
        mock_device_manager = AsyncMock()
        mock_device_manager.list_vrs_files.side_effect = AriaException(
            error_code=AriaError.DEVICE_NOT_CONNECTED
        )
        mock_get_instance.return_value = mock_device_manager

        response = client.get("/list-files")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {KEY_ERROR: MESSAGE_DEVICE_NOT_CONNECTED}
