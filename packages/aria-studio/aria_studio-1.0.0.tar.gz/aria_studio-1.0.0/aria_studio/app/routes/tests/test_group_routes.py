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

from http import HTTPStatus
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from aria_studio.app.common.types import Group

from aria_studio.app.routes.group_routes import router as app

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient

client = TestClient(app)


def compare_group(group, data):
    assert group.name == data["name"]
    assert str(group.path_on_device) == data["path_on_device"]
    assert group.creation_time == data["creation_time"]
    assert [str(vrs_file) for vrs_file in group.vrs_files] == list(data["vrs_files"])


@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
def test_list_groups_success(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()

    group1 = Group(
        name="group1",
        path_on_device=Path("/path/to/device"),
        creation_time=123456,
        vrs_files={Path("/path/to/file1.vrs")},
    )
    group2 = Group(
        name="group2",
        path_on_device=Path("/path/to/device2"),
        creation_time=123457,
        vrs_files={Path("/path/to/file2.vrs")},
    )
    mock_group_manager.get_all.return_value = {
        "group1": group1,
        "group2": group2,
    }
    mock_get_instance.return_value = mock_group_manager

    # Make request
    response = client.get("/list")
    assert response.status_code == HTTPStatus.OK
    # Matcher
    data = response.json()
    assert len(data) == 2

    compare_group(group1, data[0])
    compare_group(group2, data[1])


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_list_groups_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_group_manager = AsyncMock()
    mock_group_manager.get_all.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_group_manager
    try:
        client.get("/list")
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Unexpected error"


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_create_group_success(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.create_group.return_value = {
        "name": "NewGroup",
        "path": "/new/path",
    }
    mock_get_instance.return_value = mock_group_manager

    # Define the group data
    group_data = {"name": "NewGroup", "path": "/new/path"}

    # Make request
    response = client.post("/create", json=group_data)
    assert response.status_code == HTTPStatus.OK

    # Matcher
    data = response.json()
    assert data["name"] == group_data["name"]
    assert data["path"] == group_data["path"]


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


@pytest.mark.usefixtures("mock_auth_helper")
def test_create_group_invalid_input():
    # Define invalid group data
    group_data = {"name": "", "path": ""}  # Assuming empty strings are invalid

    # Make request
    try:
        client.post("/create", json=group_data)
        assert AssertionError
    except Exception as e:
        assert isinstance(e, RequestValidationError)


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_create_group_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_group_manager = AsyncMock()
    mock_group_manager.create_group.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_group_manager

    # Define the group data
    group_data = {"name": "NewGroup", "path": "/new/path"}

    # Make request
    try:
        client.post("/create", json=group_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Unexpected error"


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_delete_groups_success(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.delete_group = AsyncMock()
    mock_get_instance.return_value = mock_group_manager

    # Define the group names to delete
    group_data = {"names": ["Group1", "Group2"]}

    # Make request
    response = client.post("/delete", json=group_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == ["Group1", "Group2"]


def test_delete_groups_no_input():
    # Define empty group data
    group_data = {"names": []}

    # Make request
    try:
        client.post("/delete", json=group_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "No groups provided"


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_delete_groups_with_errors(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.delete_group.side_effect = [None, Exception("Deletion failed")]
    mock_get_instance.return_value = mock_group_manager

    # Define the group names to delete
    group_data = {"names": ["Group1", "Group2"]}

    # Make request
    response = client.post("/delete", json=group_data)
    assert response.status_code == HTTPStatus.OK
    assert "Group1" in response.json()
    assert "Group2" not in response.json()  # Assuming partial success is possible


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_add_files_success(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.add_files = AsyncMock(
        return_value={"name": "Group1", "files": ["/path/to/file1", "/path/to/file2"]}
    )
    mock_get_instance.return_value = mock_group_manager

    # Define the data for adding files
    file_data = {"name": "Group1", "paths": ["/path/to/file1", "/path/to/file2"]}

    # Make request
    response = client.post("/add_files", json=file_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "name": "Group1",
        "files": ["/path/to/file1", "/path/to/file2"],
    }


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_add_files_with_existing_files_success(mock_get_instance):
    # Setup mock````
    mock_group_manager = AsyncMock()
    mock_group_manager.add_files = AsyncMock(
        return_value={
            "name": "Group1",
            "files": ["/path/to/file1", "/path/to/file2", "/path/to/file3"],
        }
    )
    mock_get_instance.return_value = mock_group_manager

    # Define the data for adding files
    file_data = {"name": "Group1", "paths": ["/path/to/file3"]}

    # Make request
    response = client.post("/add_files", json=file_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "name": "Group1",
        "files": ["/path/to/file1", "/path/to/file2", "/path/to/file3"],
    }


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_add_files_with_duplicated_files_error(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.add_files = AsyncMock(
        side_effect=Exception("Duplicated files found")
    )
    mock_get_instance.return_value = mock_group_manager

    # Define the data for adding files
    file_data = {"name": "Group1", "paths": ["/path/to/file1", "/path/to/file1"]}

    # Make request
    try:
        client.post("/add_files", json=file_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Duplicated files found"


@pytest.mark.usefixtures("mock_auth_helper")
def test_add_files_invalid_input():
    # Define invalid file data
    file_data = {"name": "", "paths": []}  # Assuming empty name and paths are invalid

    # Make request
    try:
        client.post("/add_files", json=file_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures("mock_auth_helper")
@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_add_files_with_errors(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.add_files.side_effect = Exception("Addition failed")
    mock_get_instance.return_value = mock_group_manager

    # Define the data for adding files
    file_data = {"name": "Group1", "paths": ["/path/to/file1"]}

    # Make request
    try:
        client.post("/add_files", json=file_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Addition failed"


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_add_files_unexpected_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_group_manager = AsyncMock()
    mock_group_manager.add_files.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_group_manager

    # Define the data for adding files
    file_data = {"name": "Group1", "paths": ["/path/to/file1"]}

    # Make request
    try:
        client.post("/add_files", json=file_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Unexpected error"


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_remove_files_success(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.remove_files = AsyncMock(
        return_value={"name": "Group1", "files": []}
    )
    mock_get_instance.return_value = mock_group_manager

    # Define the data for removing files
    file_data = {"name": "Group1", "paths": ["/path/to/file1", "/path/to/file2"]}

    # Make request
    response = client.post("/remove_files", json=file_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"name": "Group1", "files": []}


@pytest.mark.usefixtures("mock_auth_helper")
def test_remove_files_invalid_input():
    # Define invalid file data
    file_data = {"name": "", "paths": []}  # Assuming empty name and paths are invalid

    # Make request
    try:
        client.post("/remove_files", json=file_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Group  doesn't exists."


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_remove_files_with_errors(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.remove_files.side_effect = Exception("Removal failed")
    mock_get_instance.return_value = mock_group_manager

    # Define the data for removing files
    file_data = {"name": "Group1", "paths": ["/path/to/file1"]}

    # Make request
    try:
        client.post("/remove_files", json=file_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Removal failed"


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_remove_files_unexpected_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_group_manager = AsyncMock()
    mock_group_manager.remove_files.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_group_manager

    # Define the data for removing files
    file_data = {"name": "Group1", "paths": ["/path/to/file1"]}

    # Make request
    try:
        client.post("/remove_files", json=file_data)
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Unexpected error"


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_is_allowed_group_name_allowed(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.exists = AsyncMock(return_value=False)
    mock_get_instance.return_value = mock_group_manager

    # Make request
    response = client.get("/is_allowed?group_name=NewGroup")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "allowed": True,
        "detail": "Group name 'NewGroup' is allowed",
    }


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_is_allowed_group_name_not_allowed(mock_get_instance):
    # Setup mock
    mock_group_manager = AsyncMock()
    mock_group_manager.exists = AsyncMock(return_value=True)
    mock_get_instance.return_value = mock_group_manager

    # Make request
    response = client.get("/is_allowed?group_name=ExistingGroup")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "allowed": False,
        "detail": "Group 'ExistingGroup' already exists",
    }


@pytest.mark.asyncio
@patch("aria_studio.app.groups.group_manager.GroupManager.get_instance")
async def test_is_allowed_unexpected_exception(mock_get_instance):
    # Setup mock to raise an exception
    mock_group_manager = AsyncMock()
    mock_group_manager.exists.side_effect = Exception("Unexpected error")
    mock_get_instance.return_value = mock_group_manager

    # Make request
    try:
        client.get("/is_allowed?group_name=AnyGroup")
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == HTTPStatus.BAD_REQUEST
        assert e.detail == "Unexpected error"
