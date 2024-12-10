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

from dataclasses import asdict
from http import HTTPStatus
from pathlib import Path

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aria_studio.app.constants import KEY_MESSAGE, MESSAGE_MPS_PREPARING
from aria_studio.app.routes.mps_routes import (
    _get_high_level_status,
    FeatureStatus,
    remove_none_values,
    router as app,
)

from fastapi import status

from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.testclient import TestClient
from projectaria_tools.aria_mps_cli.cli_lib.types import MpsRequest

client = TestClient(app)


def test_remove_none_values():
    # Test with a simple dictionary
    d = {"a": 1, "b": None, "c": 3}
    expected = {"a": 1, "c": 3}
    assert remove_none_values(d) == expected

    # Test with a nested dictionary
    d = {"a": 1, "b": {"x": None, "y": 2}, "c": 3}
    expected = {"a": 1, "b": {"y": 2}, "c": 3}
    assert remove_none_values(d) == expected

    # Test with an empty list
    d = {"a": 1, "b": [], "c": 3}
    expected = {"a": 1, "c": 3}
    assert remove_none_values(d) == expected

    # Test with a dictionary with no None values
    d = {"a": 1, "b": 2, "c": 3}
    expected = {"a": 1, "b": 2, "c": 3}
    assert remove_none_values(d) == expected

    # Test with an empty dictionary
    d = {}
    expected = {}
    assert remove_none_values(d) == expected


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

    @property
    def user(self):
        return self._user

    def is_logged_in(self):
        return True


# Fixture to mock authentication helper
@pytest.fixture
def mock_auth_helper(monkeypatch):
    monkeypatch.setattr(
        "aria_studio.app.utils.CliAuthHelper.get", MockCliAuthHelper.get
    )


# Mock class for HTTP helper
class MockCliHttpHelper:
    instance = None

    def __init__(self):
        MockCliHttpHelper.instance = self

    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def set_auth_token(self, token):
        pass  # Simulate setting an authentication token

    async def query_all_mps_requests(self):
        return [
            MpsRequest(
                fbid=1,
                creation_time=1234,
                features={},
                recordings_fbids=[],
                name="Request 1",
            ),
            MpsRequest(
                fbid=2,
                creation_time=5432,
                features={},
                recordings_fbids=[],
                name="Request 2",
            ),
        ]


# Fixture to mock HTTP helper
@pytest.fixture
def mock_http_helper(monkeypatch):
    monkeypatch.setattr(
        "aria_studio.app.utils.CliHttpHelper.get", lambda: MockCliHttpHelper()
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_auth_helper", "mock_http_helper")
async def test_get_all_requests():
    response = client.get("/get-all-requests/")

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "requests": [
            remove_none_values(asdict(req))
            for req in [
                MpsRequest(
                    fbid=1,
                    creation_time=1234,
                    features={},
                    recordings_fbids=[],
                    name="Request 1",
                ),
                MpsRequest(
                    fbid=2,
                    creation_time=5432,
                    features={},
                    recordings_fbids=[],
                    name="Request 2",
                ),
            ]
        ]
    }


def test_view_mps_vrs_path():
    vrs_path = Path("path/to/vrs.vrs")
    response = client.post("/view_mps", json={"vrs_path": str(vrs_path)})
    assert response.status_code == 200


def test_view_mps_no_vrs_or_group():
    try:
        client.post("/view_mps", json={})
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "No VRS files or group provided"


@pytest.mark.usefixtures("mock_auth_helper", "mock_http_helper")
def test_view_mps_invalid_group():
    group_name = "invalid_group"
    try:
        client.post("/view_mps", json={"group_name": group_name})
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.NOT_FOUND
        assert e.detail == "Group not found"


@pytest.mark.asyncio
async def test_single_request_no_vrs_files_provided():
    request_data = {"input": []}
    try:
        client.post("/request-single/", json=request_data)
        raise AssertionError
    except Exception as e:
        assert isinstance(e, RequestValidationError)


@pytest.mark.asyncio
async def test_single_request_no_feature_files_provided():
    request_data = {"input": ["test.vrs"]}
    try:
        client.post("/request-single/", json=request_data)
        raise AssertionError
    except Exception as e:
        assert isinstance(e, RequestValidationError)


@pytest.mark.asyncio
async def test_single_request_vrs_file_not_found():
    with patch("pathlib.Path.is_file", return_value=False):
        request_data = {"input": ["path/to/nonexistent/file.vrs"], "features": []}

        try:
            client.post("/request-single/", json=request_data)
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_404_NOT_FOUND
            assert e.detail == "File not found"


@pytest.mark.asyncio
async def test_single_request_vrs_file_processed_successfully():
    with patch("pathlib.Path.is_file", return_value=True), patch(
        "aria_studio.app.mps.individual_mps_request_manager.IndividualMpsRequestManager.get_instance"
    ) as mock_manager:
        mock_manager.return_value.create_request = AsyncMock()
        request_data = {"input": ["path/to/existing/file.vrs"], "features": []}
        response = client.post("/request-single/", json=request_data)
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {KEY_MESSAGE: MESSAGE_MPS_PREPARING}


@pytest.mark.asyncio
async def test_single_request_exception_during_processing():
    with patch("pathlib.Path.is_file", return_value=True), patch(
        "aria_studio.app.mps.individual_mps_request_manager.IndividualMpsRequestManager.get_instance"
    ) as mock_manager:
        mock_manager.return_value.create_request = AsyncMock(
            side_effect=Exception("Error")
        )
        request_data = {"input": ["path/to/existing/file.vrs"], "features": []}
        try:
            client.post("/request-single/", json=request_data)
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST
            assert e.detail == "Error"


@pytest.mark.asyncio
async def test_single_request_retries_successful():
    # Setup mock data and response
    mock_request_data = {"vrs_paths": ["path/to/vrs1.vrs", "path/to/vrs2.vrs"]}
    with patch(
        "aria_studio.app.mps.individual_mps_request_manager.IndividualMpsRequestManager.get_instance"
    ) as mock_manager:
        mock_manager.return_value.retry_if_failed = AsyncMock(return_value=True)
        response = client.post("/individual/retry", json=mock_request_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_check_status_no_vrs_files_provided():
    request_data = {"vrs_paths": []}
    try:
        client.post("/check-processing-status/", json=request_data)
        raise AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "No VRS files provided"


@pytest.mark.asyncio
async def test_check_status_vrs_file_not_found():
    with patch("pathlib.Path.is_file", return_value=False):
        request_data = {"vrs_paths": ["path/to/nonexistent/file.vrs"]}
        try:
            client.post("/check-processing-status/", json=request_data)
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == HTTPStatus.NOT_FOUND
            assert e.detail == "File not found path/to/nonexistent/file.vrs"


@pytest.mark.asyncio
async def test_multi_request_no_groups_provided():
    request_data = {"groups": []}
    try:
        client.post("/multi/request", json=request_data)
        assert AssertionError
    except Exception as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "No groups provided"


@pytest.mark.asyncio
async def test_multi_request_groups_processed_successfully():
    with patch(
        "aria_studio.app.mps.group_mps_request_manager.GroupMpsRequestManager.get_instance"
    ) as mock_manager:
        mock_manager.return_value.create_request = AsyncMock()
        request_data = {
            "groups": ["group1", "group2"],
            "force": True,
            "retry_failed": False,
        }
        response = client.post("/multi/request", json=request_data)
        assert response.status_code == HTTPStatus.ACCEPTED
        assert response.json() == {KEY_MESSAGE: MESSAGE_MPS_PREPARING}


@pytest.mark.asyncio
async def test_multi_request_exception_during_processing():
    with patch(
        "aria_studio.app.mps.group_mps_request_manager.GroupMpsRequestManager.get_instance"
    ) as mock_manager:
        mock_manager.return_value.create_request = AsyncMock(
            side_effect=Exception("Error during processing")
        )
        request_data = {"groups": ["group1"], "force": True, "retry_failed": False}
        try:
            client.post("/multi/request", json=request_data)
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == HTTPStatus.BAD_REQUEST
            assert e.detail == "Error during processing"


def test_get_high_level_status_empty():
    status = {}
    result, error_code = _get_high_level_status(status)
    assert result is None
    assert error_code is None


from projectaria_tools.aria_mps_cli.cli_lib.types import MpsFeature


def test_get_high_level_status_error():
    status = {
        Path("/path/to/file"): {
            MpsFeature.MULTI_SLAM: FeatureStatus(status="Error", error_code=404)
        }
    }
    result, error_code = _get_high_level_status(status)
    assert result == "Failed"
    assert error_code == 404


def test_get_high_level_status_processing():
    status = {
        Path("/path/to/file"): {
            MpsFeature.MULTI_SLAM: FeatureStatus(status="Processing", error_code=None)
        }
    }
    result, error_code = _get_high_level_status(status)
    assert result == "Processing"
    assert error_code is None


def test_get_high_level_status_success():
    status = {
        Path("/path/to/file"): {
            MpsFeature.MULTI_SLAM: FeatureStatus(status="Success", error_code=None)
        }
    }
    result, error_code = _get_high_level_status(status)
    assert result == "Success"
    assert error_code is None


@pytest.mark.asyncio
async def test_multi_high_level_status_no_groups_provided():
    request_data = {"groups": []}
    try:
        client.post("/multi/high_level_status", json=request_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "No groups provided"


@pytest.mark.asyncio
async def test_multi_high_level_status_groups_processed_successfully():
    with patch(
        "aria_studio.app.mps.group_mps_request_manager.GroupMpsRequestManager.get_instance"
    ) as mock_manager, patch(
        "aria_studio.app.routes.mps_routes._get_high_level_status"
    ) as mock_get_high_level_status:
        # Setup the correct structure and return values for check_status
        mock_status = {
            Path("/some/path"): {
                MpsFeature.MULTI_SLAM: FeatureStatus(
                    status="Processing", error_code=None
                )
            }
        }
        mock_manager.return_value.check_status = AsyncMock(return_value=mock_status)

        # Mock _get_high_level_status to return the desired test values
        mock_get_high_level_status.return_value = ("HighLevelStatus1", 0)

        request_data = {"groups": ["group1", "group2"]}
        response = client.post("/multi/high_level_status", json=request_data)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "group1": "HighLevelStatus1",
            "group2": "HighLevelStatus1",
        }


@pytest.mark.asyncio
async def test_multi_status_no_vrs_path_provided_group_status_fetched():
    with patch(
        "aria_studio.app.mps.group_mps_request_manager.GroupMpsRequestManager.get_instance"
    ) as mock_manager, patch(
        "aria_studio.app.groups.group_manager.GroupManager.get_instance"
    ) as mock_group_manager:
        mock_manager.return_value.check_status = AsyncMock(return_value={})
        mock_group_manager.return_value.get = AsyncMock(
            return_value=MagicMock(path_on_device="path/to/device")
        )
        response = client.get("/multi/status", params={"group": "group1"})
        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_multi_status_vrs_path_not_found():
    with patch(
        "aria_studio.app.mps.group_mps_request_manager.GroupMpsRequestManager.get_instance"
    ) as mock_manager:
        mock_manager.return_value.check_status = AsyncMock(
            side_effect=Exception("Group not found")
        )
        try:
            client.get(
                "/multi/status",
                params={"group": "group1", "vrs_path": "nonexistent.vrs"},
            )
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == HTTPStatus.BAD_REQUEST
            assert e.detail == "Group not found"


@pytest.mark.asyncio
async def test_multi_status_vrs_path_found():
    with patch(
        "aria_studio.app.mps.group_mps_request_manager.GroupMpsRequestManager.get_instance"
    ) as mock_manager, patch(
        "aria_studio.app.groups.group_manager.GroupManager.get_instance"
    ) as mock_group_manager:
        # Setup the correct structure and return values for check_status
        mock_feature_status = FeatureStatus(
            status="Processing",
            error_code=None,
            creation_time=1234,  # Provide a datetime object for creation_time
            output_path=Path("/output/path"),
        )
        mock_status = {Path("/some/path"): {MpsFeature.MULTI_SLAM: mock_feature_status}}
        mock_manager.return_value.check_status = AsyncMock(return_value=mock_status)

        # Mock the group manager to return a group with a path
        mock_group_manager.return_value.get = AsyncMock(
            return_value=MagicMock(path_on_device=Path("/device/path"))
        )

        response = client.get(
            "/multi/status", params={"group": "group1", "vrs_path": "/some/path"}
        )
        assert response.status_code == HTTPStatus.OK
        assert "/some/path" in response.json()


@pytest.mark.asyncio
async def test_multi_status_exception_during_processing():
    with patch(
        "aria_studio.app.mps.group_mps_request_manager.GroupMpsRequestManager.get_instance"
    ) as mock_manager:
        mock_manager.return_value.check_status = AsyncMock(
            side_effect=Exception("Error during processing")
        )
        try:
            client.get("/multi/status", params={"group": "group1"})
            raise AssertionError
        except HTTPException as e:
            assert e.status_code == HTTPStatus.BAD_REQUEST
            assert e.detail == "Error during processing"
