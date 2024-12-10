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

import json

import pytest

from aria_studio.app.constants import KEY_FILE_NAME, KEY_FILE_PATH

from .local_file_manager import (
    _cleanup_metadata,
    _create_metadata_from_metadata_json_file,
    _is_valid,
    _load_json,
    _RELEVANT_KEYS,
    _write_metadata,
)


@pytest.fixture
def test_file_path(tmp_path):
    return tmp_path / "test.json"


def test_is_valid_with_none_metadata():
    assert not _is_valid(None)


def test_is_valid_with_empty_metadata():
    assert not _is_valid({})


def test_is_valid_with_missing_key_metadata():
    metadata = {"key1": "value1", "key2": "value2"}
    assert not _is_valid(metadata)


def test_is_valid_with_valid_metadata():
    metadata = {}
    for key in _RELEVANT_KEYS:
        metadata[key] = "1"
    assert _is_valid(metadata)


def test_cleanup_metadata_with_valid_metadata():
    metadata = {"key1": "value1", "key2": 2, "key3": True}
    metadata_correct_keys = {}
    for key, value_type in _RELEVANT_KEYS.items():
        metadata_correct_keys[key] = value_type("1")

    metadata = metadata | metadata_correct_keys

    clean_metadata = _cleanup_metadata(metadata)
    assert clean_metadata == metadata_correct_keys


def test_cleanup_metadata_with_invalid_type():
    metadata_with_wrong_types = {"random_key": "random_value"}
    for key in _RELEVANT_KEYS:
        metadata_with_wrong_types[key] = "1"

    metadata_with_correct_types = {}
    for key, value_type in _RELEVANT_KEYS.items():
        metadata_with_correct_types[key] = value_type("1")

    clean_data = _cleanup_metadata(metadata_with_wrong_types)
    assert clean_data == metadata_with_correct_types


def test_cleanup_metadata_with_missing_key():
    metadata = {}
    for key in list(_RELEVANT_KEYS.keys())[1:]:
        metadata[key] = "1"

    with pytest.raises(KeyError):
        _cleanup_metadata(metadata)


def test_cleanup_metadata_with_empty_metadata():
    metadata = {}
    with pytest.raises(KeyError):
        _cleanup_metadata(metadata)


def test_load_json_file_exists(test_file_path):
    test_dict = {"key": "value"}
    with open(test_file_path, "w") as f:
        json.dump(test_dict, f)

    result = _load_json(test_file_path)

    assert result == test_dict


def test_load_json_file_not_exists(test_file_path):
    # Arrange
    test_file_path.unlink(missing_ok=True)
    # Act
    result = _load_json(test_file_path)
    # Assert
    assert result is None


def test_load_json_invalid_json(test_file_path):
    # Arrange
    with open(test_file_path, "w") as f:
        f.write("invalid json")
    # Act
    result = _load_json(test_file_path)
    # Assert
    assert result is None


@pytest.fixture
def test_vrs_path(tmp_path):
    return tmp_path / "test.vrs"


def test_create_metadata_from_metadata_json_file_exists(test_vrs_path):
    metadata_path = test_vrs_path.with_suffix(".vrs.json")

    with open(str(metadata_path), "w") as f:
        json.dump({"key": "value"}, f)

    result = _create_metadata_from_metadata_json_file(test_vrs_path)

    assert result == {"key": "value"}


def test_create_metadata_from_metadata_json_file_not_exists(test_vrs_path):
    metadata_path = test_vrs_path.with_suffix(".vrs.json")
    metadata_path.unlink(missing_ok=True)
    result = _create_metadata_from_metadata_json_file(test_vrs_path)
    assert result is None


def test_create_metadata_from_metadata_json_file_invalid_json(test_vrs_path):
    metadata_path = test_vrs_path.with_suffix(".vrs.json")
    with open(str(metadata_path), "w") as f:
        f.write("invalid json")

    with pytest.raises(json.JSONDecodeError):
        _create_metadata_from_metadata_json_file(test_vrs_path)


@pytest.fixture
def test_metadata():
    return {"key": "value"}


@pytest.fixture
def test_metadata_path(tmp_path):
    return tmp_path / "metadata.json"


def test_write_metadata(test_vrs_path, test_metadata, test_metadata_path):
    # Act
    _write_metadata(test_vrs_path, test_metadata, test_metadata_path)
    # Assert
    with open(test_metadata_path, "r") as f:
        written_metadata = json.load(f)
        assert written_metadata == test_metadata | {
            KEY_FILE_NAME: test_vrs_path.name,
            KEY_FILE_PATH: str(test_vrs_path.parent),
        }


def test_write_metadata_overwrites_existing_file(
    test_vrs_path, test_metadata, test_metadata_path
):
    with open(test_metadata_path, "w") as f:
        json.dump({"existing": "data"}, f)

    _write_metadata(test_vrs_path, test_metadata, test_metadata_path)

    with open(test_metadata_path, "r") as f:
        written_metadata = json.load(f)
        assert written_metadata == test_metadata | {
            KEY_FILE_NAME: test_vrs_path.name,
            KEY_FILE_PATH: str(test_vrs_path.parent),
        }


def test_write_metadata_invalid_metadata(test_vrs_path, test_metadata_path):
    # Arrange
    invalid_metadata = ""
    # Act and Assert
    with pytest.raises(TypeError):
        _write_metadata(test_vrs_path, invalid_metadata, test_metadata_path)
