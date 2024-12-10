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

import pytest
from aria_studio.app.constants import (
    KEY_LOGGED_IN,
    KEY_MESSAGE,
    KEY_USER,
    MESSAGE_LOGGED_IN_SUCCESS,
    MESSAGE_LOGGED_OUT_FAILED,
    MESSAGE_LOGGED_OUT_SUCCESS,
)
from aria_studio.app.routes.auth_routes import router as app

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from projectaria_tools.aria_mps_cli.cli_lib.authentication import AuthenticationError

# Initialize the test client for FastAPI application
client = TestClient(app)


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
    def auth_token(self):
        return self._auth_token

    async def login(self, username, password, save_token):
        if username == "test" and password == "test":
            return True
        raise AuthenticationError("Login failed with exception")

    async def logout(self):
        return True  # Simulate successful logout

    async def logout_failure(self):
        return False  # Simulate failed logout

    @property
    def user(self):
        return self._user

    def is_logged_in(self):
        return True


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


# Fixture to mock HTTP helper
@pytest.fixture
def mock_http_helper(monkeypatch):
    monkeypatch.setattr(
        "aria_studio.app.utils.CliHttpHelper.get", lambda: MockCliHttpHelper()
    )


# Fixture to mock authentication helper
@pytest.fixture
def mock_auth_helper(monkeypatch):
    monkeypatch.setattr(
        "aria_studio.app.utils.CliAuthHelper.get", MockCliAuthHelper.get
    )


# Test to verify successful logout
@pytest.mark.usefixtures("mock_auth_helper")
def test_logout_success():
    response = client.get("/logout")
    assert response.status_code == 200
    assert response.json()["message"] == MESSAGE_LOGGED_OUT_SUCCESS


# Test to verify failed logout
@pytest.mark.usefixtures("mock_auth_helper")
def test_logout_failure(monkeypatch):
    monkeypatch.setattr(MockCliAuthHelper, "logout", MockCliAuthHelper.logout_failure)
    try:
        client.get("/logout")
        assert AssertionError
    except HTTPException as e:
        assert e.status_code == status.HTTP_400_BAD_REQUEST
        assert e.detail == MESSAGE_LOGGED_OUT_FAILED


# Test to verify successful login
@pytest.mark.usefixtures("mock_auth_helper", "mock_http_helper")
def test_login_success():
    response = client.post(
        "/login", json={"username": "test", "password": "test", "save_token": False}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[KEY_MESSAGE] == MESSAGE_LOGGED_IN_SUCCESS


# Test to verify failed login due to incorrect credentials
@pytest.mark.usefixtures("mock_auth_helper")
def test_login_failure(mock_auth_helper, mock_http_helper):
    try:
        client.post(
            "/login",
            json={"username": "wrong", "password": "wrong", "save_token": False},
        )
    except HTTPException as e:
        assert e.status_code == status.HTTP_401_UNAUTHORIZED
        assert e.detail == "Login failed with exception"


# Test to verify logged-in status
@pytest.mark.usefixtures("mock_auth_helper")
def test_is_logged_in():
    response = client.get("/is-logged-in")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[KEY_LOGGED_IN]


# Test to verify current user information
@pytest.mark.usefixtures("mock_auth_helper")
def test_current_user():
    response = client.get("/current-user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[KEY_USER] == "test_user"
