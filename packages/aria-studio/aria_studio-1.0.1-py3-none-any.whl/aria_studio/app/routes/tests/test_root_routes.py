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

from pathlib import Path
from unittest.mock import patch

from aria_studio.app.routes.root_routes import router as app
from fastapi import status
from fastapi.testclient import TestClient


class MockFileResponse:
    def __init__(
        self, path, filename=None, media_type=None, headers=None, stat_result=None
    ):
        self.status_code = status.HTTP_200_OK

    async def __call__(self, scope, receive, send):
        pass


client = TestClient(app)


@patch("aria_studio.app.routes.root_routes.FileResponse", new=MockFileResponse)
def test_serve_react_app_exists(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda self: True)
    client = TestClient(app)
    response = client.get("/some_path")
    assert response.status_code == status.HTTP_200_OK


def test_serve_react_app_fallback_to_index(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda self: False)
    response = client.get("/nonexistentpath")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"].startswith("text/html")


def test_serve_react_app_api_path(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda self: True)
    response = client.get("/api/some_path")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Not Found"}
