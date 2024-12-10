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

import asyncio
import json

from io import BytesIO
from pathlib import Path
from unittest.mock import AsyncMock, call, MagicMock, patch

import pytest
from aria_studio.app.common.types import AriaError, AriaException

from aria_studio.app.device.device_manager import (
    _ARIA_RECORDINGS_ROOT,
    _ARIA_THUMBNAILS_ROOT,
    _DEVICE_MONITOR_INTERVAL,
    DeviceManager,
)
from PIL import Image


@pytest.fixture
def device_manager():
    return DeviceManager.get_instance()


@pytest.mark.asyncio
async def test_get_instance():
    # Test that get_instance() returns the same instance every time it is called
    instance1 = DeviceManager.get_instance()
    instance2 = DeviceManager.get_instance()
    assert instance1 is instance2


@pytest.mark.asyncio
async def test_reset():
    # Create a new instance of the DeviceManager class
    device_manager1 = DeviceManager.get_instance()

    # Call the reset method
    await DeviceManager.reset()

    assert device_manager1.instance_ is None

    # Create a new instance of the DeviceManager class
    device_manager2 = DeviceManager.get_instance()

    assert device_manager1 is not device_manager2


def test_set_adb_path_raise_error():
    # Test that set_adb_path() sets the path to the adb executable correctly

    adb_path = Path("/path/to/adb")
    # Test that set_adb_path() raises FileNotFoundError if the adb path does not exist
    with pytest.raises(FileNotFoundError):
        DeviceManager.set_adb_path(adb_path)


def test_set_adb_path_success(monkeypatch):
    adb_path = Path("/path/to/adb")
    monkeypatch.setattr(Path, "is_file", lambda self: True)
    DeviceManager.set_adb_path(adb_path)

    assert DeviceManager.adb_path_ == adb_path


def test_check_device_connected_raise_exception():
    try:
        device_manager = DeviceManager.get_instance()
        device_manager.check_device_connected()
        assert AssertionError
    except AriaException as e:
        assert e.error_code == AriaException.DEVICE_NOT_CONNECTED


def test_check_device_connected_success():
    try:
        device_manager = DeviceManager.get_instance()
        device_manager.check_device_connected()
        assert AssertionError
    except AriaException as e:
        assert e.error_code == AriaException.DEVICE_NOT_CONNECTED


@pytest.mark.asyncio
async def test_device_heartbeat_with_disconnection(device_manager):
    # mock asyncio.sleep to prevent actual sleep
    sleep_mock = AsyncMock(side_effect=[None, None, asyncio.CancelledError()])

    # mock check_device_connected to raise an exception on the second call
    check_connected_mock = AsyncMock(
        side_effect=[None, Exception("Device disconnected")]
    )

    with patch("asyncio.sleep", sleep_mock), patch.object(
        device_manager, "check_device_connected", check_connected_mock
    ), patch(
        "aria_studio.app.device.device_manager.logger.debug"
    ) as logger_mock, patch.object(
        device_manager._disk_cache, "clear"
    ) as cache_clear_mock:
        # Expect the loop to exit due to the CancelledError after handling an internal exception
        with pytest.raises(asyncio.CancelledError):
            await device_manager.device_heartbeat()

        sleep_mock.assert_awaited_with(_DEVICE_MONITOR_INTERVAL)

        # verify asyncio.sleep was called, indicating the loop ran
        assert sleep_mock.call_count == 3

        # verify check_device_connected was called twice
        assert check_connected_mock.call_count == 2

        # verify logger.debug was called twice
        assert logger_mock.call_count == 2

        logger_mock.assert_has_calls(
            [
                call("Heartbeat connected"),  # first loop, no exception
                call("Heartbeat not connected"),  # second loop, exception raised
            ]
        )

        # verify cache.clear was called once
        cache_clear_mock.assert_called_once()


@pytest.mark.asyncio
async def test_delete_files_success(device_manager):
    vrs_files = ["file1.vrs", "file2.vrs"]
    adb_command_mock = AsyncMock()

    with patch.object(device_manager, "_adb_command", adb_command_mock):
        await device_manager.delete_files(vrs_files)

        vrs_and_metadata_files = [
            Path(_ARIA_RECORDINGS_ROOT, f"{f}*") for f in vrs_files
        ]
        thumbnails = [_ARIA_THUMBNAILS_ROOT / f"{Path(f).stem}*" for f in vrs_files]

        adb_command_mock.assert_called_once_with(
            [
                "shell",
                "rm",
            ]
            + vrs_and_metadata_files
            + thumbnails,
            AriaError.DELETE_FAILED,
        )


@pytest.mark.asyncio
async def test_delete_files_no_files_found(device_manager):
    vrs_files = ["file1.vrs", "file2.vrs"]
    adb_command_mock = AsyncMock(side_effect=AriaException(AriaError.DELETE_FAILED))

    with patch.object(device_manager, "_adb_command", adb_command_mock), patch(
        "aria_studio.app.device.device_manager.logger.debug"
    ) as logger_mock:
        await device_manager.delete_files(vrs_files)

        logger_mock.assert_called_once_with("No files found on device")


@pytest.mark.asyncio
async def test_delete_files_other_exception(device_manager):
    vrs_files = ["file1.vrs", "file2.vrs"]
    adb_command_mock = AsyncMock(side_effect=AriaException("Some other error"))

    with patch.object(device_manager, "_adb_command", adb_command_mock):
        with pytest.raises(AriaException):
            await device_manager.delete_files(vrs_files)


@pytest.mark.asyncio
async def test_list_vrs_files_success(device_manager):
    adb_command_mock = AsyncMock(return_value=(b"file1.vrs\nfile2.vrs", b""))

    with patch.object(device_manager, "_adb_command", adb_command_mock):
        result = await device_manager.list_vrs_files()

        adb_command_mock.assert_called_once_with(
            ["shell", "ls", Path(_ARIA_RECORDINGS_ROOT) / "*.vrs"],
            AriaError.LIST_RECORDING_FAILED,
        )

        assert result == [Path("file1.vrs"), Path("file2.vrs")]


@pytest.mark.asyncio
async def test_list_vrs_files_no_files_found(device_manager):
    adb_command_mock = AsyncMock(
        side_effect=AriaException(AriaError.LIST_RECORDING_FAILED)
    )

    with patch.object(device_manager, "_adb_command", adb_command_mock), patch(
        "aria_studio.app.device.device_manager.logger.debug"
    ) as logger_mock:
        result = await device_manager.list_vrs_files()

        logger_mock.assert_called_once_with("No vrs files found on device")

        assert result == []


@pytest.mark.asyncio
async def test_list_vrs_files_other_exception(device_manager):
    adb_command_mock = AsyncMock(side_effect=AriaException("Some other error"))

    with patch.object(device_manager, "_adb_command", adb_command_mock):
        with pytest.raises(AriaException):
            await device_manager.list_vrs_files()


@pytest.mark.asyncio
async def test_pull_file_success(device_manager):
    file_path = Path("/device/path/to/file")
    destination = Path("/local/path/to/destination")
    adb_command_mock = AsyncMock(return_value=("output", "error"))

    with patch.object(device_manager, "_adb_command", adb_command_mock):
        result = await device_manager._pull_file(file_path, destination)
        adb_command_mock.assert_called_once_with(
            ["pull", file_path, destination], AriaError.PULL_FAILED
        )

        assert result == ("output", "error")


@pytest.mark.asyncio
async def test_pull_file_failure(device_manager):
    file_path = Path("/device/path/to/file")
    destination = Path("/local/path/to/destination")
    adb_command_mock = AsyncMock(side_effect=AriaException(AriaError.PULL_FAILED))

    with patch.object(device_manager, "_adb_command", adb_command_mock):
        with pytest.raises(AriaException):
            await device_manager._pull_file(file_path, destination)


@pytest.mark.asyncio
async def test_get_thumbnail_jpeg_cached(device_manager):
    vrs_file = Path("test.vrs")
    thumbnail_path = Path("/cache/dir/thumbnail.jpeg")
    disk_cache_mock = MagicMock()
    disk_cache_mock.get_cache_dir.return_value = thumbnail_path.parent

    with patch.object(device_manager, "_disk_cache", disk_cache_mock):
        with patch("pathlib.Path.exists", return_value=True):
            result = await device_manager.get_thumbnail_jpeg(vrs_file)

            assert result == thumbnail_path


@pytest.mark.asyncio
async def test_get_thumbnail_jpeg_no_thumbnails(device_manager):
    vrs_file = Path("test.vrs")
    thumbnail_path = Path("/cache/dir/thumbnail.jpeg")
    disk_cache_mock = MagicMock()
    disk_cache_mock.get_cache_dir.return_value = thumbnail_path.parent
    list_thumbnails_mock = AsyncMock(return_value=[])

    with patch.object(device_manager, "_disk_cache", disk_cache_mock):
        with patch("pathlib.Path.exists", return_value=False):
            with patch.object(device_manager, "_list_thumbnails", list_thumbnails_mock):
                with pytest.raises(AriaException) as excinfo:
                    await device_manager.get_thumbnail_jpeg(vrs_file)
                assert excinfo.value.args[0] == f"No thumbnail found for {vrs_file}"


@pytest.mark.asyncio
async def test_get_thumbnail_jpeg_success(device_manager):
    vrs_file = Path("test.vrs")
    thumbnail_path = Path("/cache/dir/thumbnail.jpeg")
    disk_cache_mock = MagicMock()
    disk_cache_mock.get_cache_dir.return_value = thumbnail_path.parent
    list_thumbnails_mock = AsyncMock(
        return_value=[
            Path("/device/path/to/thumbnail1"),
            Path("/device/path/to/thumbnail2"),
        ]
    )
    shell_cat_mock = AsyncMock(return_value=b"image_data")

    with patch.object(device_manager, "_disk_cache", disk_cache_mock):
        with patch("pathlib.Path.exists", return_value=False):
            with patch.object(device_manager, "_list_thumbnails", list_thumbnails_mock):
                with patch.object(device_manager, "_shell_cat", shell_cat_mock):
                    with patch("PIL.Image.open") as image_open_mock:
                        mock_image = MagicMock()
                        image_open_mock.return_value = mock_image
                        mock_image.rotate.return_value = mock_image
                        mock_image.save.return_value = BytesIO(b"image_data")
                        result = await device_manager.get_thumbnail_jpeg(vrs_file)

                        assert result == thumbnail_path
                        image_open_mock.assert_called_once()
                        mock_image.rotate.assert_called_once_with(-90)
                        mock_image.save.assert_called_once_with(thumbnail_path)


@pytest.mark.asyncio
async def test_get_thumbnail_jpeg_exception_handling(device_manager):
    vrs_file = Path("test.vrs")
    thumbnail_path = Path("/cache/dir/thumbnail.jpeg")
    disk_cache_mock = MagicMock()
    disk_cache_mock.get_cache_dir.return_value = thumbnail_path.parent
    list_thumbnails_mock = AsyncMock(return_value=[Path("/device/path/to/thumbnail1")])
    shell_cat_mock = AsyncMock(side_effect=Exception("Some error"))

    with patch.object(device_manager, "_disk_cache", disk_cache_mock):
        with patch("pathlib.Path.exists", return_value=False):
            with patch.object(device_manager, "_list_thumbnails", list_thumbnails_mock):
                with patch.object(device_manager, "_shell_cat", shell_cat_mock):
                    with patch(
                        "aria_studio.app.device.device_manager.logger.exception"
                    ) as logger_mock:
                        with pytest.raises(AriaException) as excinfo:
                            await device_manager.get_thumbnail_jpeg(vrs_file)
                        assert (
                            excinfo.value.args[0]
                            == f"No thumbnail found for {vrs_file}"
                        )
                        logger_mock.assert_called_once()


@pytest.mark.asyncio
async def test_get_status(device_manager):
    device_manager.check_device_connected = AsyncMock()
    device_manager._adb_command = AsyncMock()
    device_manager._copy_tasks = []

    device_manager._adb_command.side_effect = [
        (b"serial123", None),
        (b"level: 85", None),
        (b"ssid=my_wifi", None),
        (b"diskstats=Data-Free: 102419308K / 110404388K total = 92% free", None),
    ]

    status = await device_manager.get_status()

    assert status.serial_number == "serial123"
    assert status.battery_level == 85
    assert status.wifi_ssid == "my_wifi"
    assert status.import_in_progress is False

    assert device_manager._adb_command.call_count == 4


@pytest.mark.asyncio
async def test_get_status_with_exceptions(device_manager):
    device_manager.check_device_connected = AsyncMock()
    device_manager._adb_command = AsyncMock()
    device_manager._copy_tasks = []

    device_manager._adb_command.side_effect = [
        AriaException(AriaError.GET_STATUS_FAILED),
        (b"level: 85", None),
        (b"ssid=my_wifi", None),
    ]

    with pytest.raises(AriaException) as excinfo:
        await device_manager.get_status()

    assert excinfo.value.error_code == AriaError.GET_STATUS_FAILED
    assert device_manager._adb_command.call_count == 4


@pytest.mark.asyncio
async def test_get_metadata_success(device_manager):
    vrs_file = "test_file"
    metadata_content = json.dumps({"key": "value"}).encode("UTF-8")
    device_manager._shell_cat = AsyncMock(return_value=metadata_content)

    result = await device_manager.get_metadata(vrs_file)

    assert result == json.loads(metadata_content)

    device_manager._shell_cat.assert_called_once_with(
        Path(_ARIA_RECORDINGS_ROOT, f"{vrs_file}.json"), AriaError.METADATA_READ_FAILED
    )


@pytest.mark.asyncio
async def test_get_metadata_decode_error(device_manager):
    vrs_file = "test_file"
    invalid_metadata_content = b"invalid json"
    device_manager._shell_cat = AsyncMock(return_value=invalid_metadata_content)

    with pytest.raises(AriaException) as exc_info:
        await device_manager.get_metadata(vrs_file)

    assert exc_info.value.error_code == AriaError.METADATA_READ_FAILED
    assert str(exc_info.value) == "Not a valid json metadata"
    device_manager._shell_cat.assert_awaited_once_with(
        Path(_ARIA_RECORDINGS_ROOT, f"{vrs_file}.json"), AriaError.METADATA_READ_FAILED
    )


@pytest.mark.asyncio
async def test_get_metadata_shell_cat_error(device_manager):
    vrs_file = "test_file"
    error_msg = "Shell cat error"
    device_manager._shell_cat = AsyncMock(
        side_effect=AriaException(AriaError.METADATA_READ_FAILED, error_msg)
    )

    with pytest.raises(AriaException) as exc_info:
        await device_manager.get_metadata(vrs_file)

    assert exc_info.value.error_code == AriaError.METADATA_READ_FAILED
    assert str(exc_info.value) == error_msg

    device_manager._shell_cat.assert_awaited_once_with(
        Path(_ARIA_RECORDINGS_ROOT, f"{vrs_file}.json"), AriaError.METADATA_READ_FAILED
    )


@pytest.mark.asyncio
async def test_get_thumbnail_gif_success(device_manager):
    vrs_file = "test_file"
    cache_dir = Path("/fake/cache/dir")
    thumbnail_path = cache_dir / "thumbnail.gif"
    thumbnails = [Path(f"/fake/thumbnail_{i}.jpg") for i in range(3)]

    img_data = BytesIO(b"fake_image_data")
    img = Image.new("RGBA", (100, 100))

    device_manager._disk_cache.get_cache_dir = MagicMock(return_value=cache_dir)
    device_manager._list_thumbnails = AsyncMock(return_value=thumbnails)
    device_manager._shell_cat = AsyncMock(return_value=img_data.getvalue())

    with patch("PIL.Image.open", return_value=img) as mock_open, patch.object(
        img, "rotate", return_value=img
    ) as mock_rotate, patch.object(
        img, "convert", return_value=img
    ) as mock_convert, patch.object(img, "save", return_value=img) as mock_save:
        result = await device_manager.get_thumbnail_gif(vrs_file)

        assert result == thumbnail_path
        device_manager._disk_cache.get_cache_dir.assert_called_once_with(vrs_file)
        device_manager._list_thumbnails.assert_awaited_once_with(vrs_file)
        assert device_manager._shell_cat.await_count == len(thumbnails)
        mock_open.assert_called()
        mock_rotate.assert_called()
        mock_convert.assert_called()
        mock_save.assert_called_once_with(
            thumbnail_path,
            save_all=True,
            append_images=[img, img],
            duration=500,
            loop=0,
        )


@pytest.mark.asyncio
async def test_get_thumbnail_gif_no_thumbnail(device_manager):
    vrs_file = "test_file"
    device_manager._disk_cache.get_cache_dir = MagicMock(
        return_value=Path("/fake/cache/dir")
    )
    device_manager._list_thumbnails = AsyncMock(return_value=[])

    with pytest.raises(FileNotFoundError) as exc_info:
        await device_manager.get_thumbnail_gif(vrs_file)

    assert str(exc_info.value) == f"No thumbnails found for {vrs_file}"

    device_manager._disk_cache.get_cache_dir.assert_called_once_with(vrs_file)
    device_manager._list_thumbnails.assert_awaited_once_with(vrs_file)


@pytest.mark.asyncio
async def test_get_thumbnail_gif_generate_failed(device_manager):
    vrs_file = "test_file"
    thumbnails = [Path(f"/fake/thumbnail_{i}.jpg") for i in range(3)]

    device_manager._disk_cache.get_cache_dir = MagicMock(
        return_value=Path("/fake/cache/dir")
    )
    device_manager._list_thumbnails = AsyncMock(return_value=thumbnails)
    device_manager._shell_cat = AsyncMock(side_effect=Exception("Shell cat error"))

    with pytest.raises(AriaException) as exc_info:
        await device_manager.get_thumbnail_gif(vrs_file)

    assert exc_info.value.error_code == AriaError.GIF_GENERATE_FAILED
    assert str(exc_info.value) == f"Failed to generate gif for {vrs_file}"
    device_manager._disk_cache.get_cache_dir.assert_called_once_with(vrs_file)
    device_manager._list_thumbnails.assert_awaited_once_with(vrs_file)
    assert device_manager._shell_cat.await_count == len(thumbnails)


@pytest.mark.asyncio
async def test_shell_cat_success():
    DeviceManager.instance_ = None
    device_manager = DeviceManager.get_instance()

    file_path = Path("/fake/file/path")
    expected_output = "file_content"
    device_manager._adb_command = AsyncMock(return_value=(expected_output, None))

    result = await device_manager._shell_cat(file_path)

    assert result == expected_output
    device_manager._adb_command.assert_awaited_once_with(
        ["shell", "cat", file_path], error_code=None
    )


@pytest.mark.asyncio
async def test_shell_cat_error():
    file_path = Path("/fake/path/to/file")
    error_code = AriaError.GENERIC_DEVICE_ERROR
    instance = DeviceManager.get_instance()
    instance._adb_command = AsyncMock(return_value=("", "error message"))

    result = await instance._shell_cat(file_path, error_code=error_code)

    assert result == ""
    instance._adb_command.assert_awaited_once_with(
        ["shell", "cat", file_path], error_code=error_code
    )


@pytest.mark.asyncio
async def test_shell_cat_empty_output():
    file_path = Path("/fake/path/to/file")
    instance = DeviceManager.get_instance()
    instance._adb_command = AsyncMock(return_value=("", ""))

    result = await instance._shell_cat(file_path)

    assert result == ""
    instance._adb_command.assert_awaited_once_with(
        ["shell", "cat", file_path], error_code=None
    )


@pytest.mark.asyncio
async def test_list_thumbnails_success():
    vrs_file = "test_file.vrs"
    thumbnail_pattern = f"{vrs_file[:-4]}_*.jpeg"
    thumbnail_path_on_aria = Path("/sdcard/recording/thumbnails") / thumbnail_pattern
    stdout = "thumbnail_1.jpeg\nthumbnail_2.jpeg\nthumbnail_3.jpeg"
    instance = DeviceManager.get_instance()
    instance._adb_command = AsyncMock(return_value=(stdout.encode(), ""))

    result = await instance._list_thumbnails(vrs_file)

    expected_result = [
        Path("thumbnail_1.jpeg"),
        Path("thumbnail_2.jpeg"),
        Path("thumbnail_3.jpeg"),
    ]
    assert result == expected_result
    instance._adb_command.assert_awaited_once_with(
        ["shell", "ls", thumbnail_path_on_aria],
        AriaError.LIST_THUMBNAIL_FAILED,
    )


@pytest.mark.asyncio
async def test_list_thumbnails_not_found():
    vrs_file = "test_file.vrs"
    thumbnail_pattern = f"{vrs_file[:-4]}_*.jpeg"
    thumbnail_path_on_aria = Path("/sdcard/recording/thumbnails") / thumbnail_pattern
    instance = DeviceManager.get_instance()
    instance._adb_command = AsyncMock(return_value=("", ""))

    with pytest.raises(AriaException) as exc_info:
        await instance._list_thumbnails(vrs_file)

    assert exc_info.value.error_code == AriaError.THUMBNAIL_NOT_FOUND
    instance._adb_command.assert_awaited_once_with(
        ["shell", "ls", thumbnail_path_on_aria],
        AriaError.LIST_THUMBNAIL_FAILED,
    )


@pytest.mark.asyncio
async def test_list_thumbnails_empty_output():
    vrs_file = "test_file.vrs"
    thumbnail_pattern = f"{vrs_file[:-4]}_*.jpeg"
    thumbnail_path_on_aria = Path("/sdcard/recording/thumbnails") / thumbnail_pattern
    instance = DeviceManager.get_instance()
    instance._adb_command = AsyncMock(return_value=(b"", ""))

    with pytest.raises(AriaException) as exc_info:
        await instance._list_thumbnails(vrs_file)

    assert exc_info.value.error_code == AriaError.THUMBNAIL_NOT_FOUND
    instance._adb_command.assert_awaited_once_with(
        ["shell", "ls", thumbnail_path_on_aria],
        AriaError.LIST_THUMBNAIL_FAILED,
    )


@pytest.mark.asyncio
async def test_list_thumbnails_error():
    vrs_file = "test_file.vrs"
    thumbnail_pattern = f"{vrs_file[:-4]}_*.jpeg"
    thumbnail_path_on_aria = Path("/sdcard/recording/thumbnails") / thumbnail_pattern
    instance = DeviceManager.get_instance()
    instance._adb_command = AsyncMock(return_value=(b"", "error message"))

    with pytest.raises(AriaException) as exc_info:
        await instance._list_thumbnails(vrs_file)

    assert exc_info.value.error_code == AriaError.THUMBNAIL_NOT_FOUND
    instance._adb_command.assert_awaited_once_with(
        ["shell", "ls", thumbnail_path_on_aria],
        AriaError.LIST_THUMBNAIL_FAILED,
    )


def test_get_copy_progress_no_tasks():
    device_manager = DeviceManager.get_instance()
    device_manager._copy_tasks = []
    result = device_manager.get_copy_progress()

    assert result.copied_bytes == 0


def test_get_copy_progress_tasks_not_done():
    device_manager = DeviceManager.get_instance()

    task_mock = MagicMock()
    task_mock.done.return_value = False
    device_manager._copy_tasks = [task_mock]

    file_path = Path("/fake/file/path/file1.vrs")
    device_manager._vrs_files_to_copy = [file_path]
    bytes_size = 50
    with patch("pathlib.Path.exists", return_value=True), patch(
        "pathlib.Path.stat", return_value=MagicMock(st_size=bytes_size)
    ):
        status = device_manager.get_copy_progress()
        assert status.copied_bytes == bytes_size


def test_get_copy_progress_partial_file(device_manager):
    task_mock = MagicMock()
    task_mock.done.return_value = False
    device_manager._copy_tasks = [task_mock]

    file_path = Path("/fake/file/path/file1.vrs")
    device_manager._vrs_files_to_copy = [file_path]
    bytes_size = 50

    with patch("pathlib.Path.exists", return_value=True), patch(
        "pathlib.Path.stat", return_value=MagicMock(st_size=bytes_size)
    ):
        status = device_manager.get_copy_progress()
        assert status.copied_bytes == bytes_size


@pytest.mark.asyncio
async def test_get_copy_progress_tasks_done():
    device_manager = DeviceManager.get_instance()

    task_mock = MagicMock()
    task_mock.done.return_value = True
    device_manager._copy_tasks = [task_mock]
    bytes_size = 50

    with patch("pathlib.Path.exists", return_value=True), patch(
        "pathlib.Path.stat", return_value=MagicMock(st_size=bytes_size)
    ):
        status = device_manager.get_copy_progress()
        assert status.copied_bytes == bytes_size


@pytest.mark.asyncio
async def test_start_copy_vrs_files_in_progress():
    task_mock = MagicMock()
    task_mock.done.return_value = False
    device_manager = DeviceManager.get_instance()
    device_manager._copy_tasks = [task_mock]

    with pytest.raises(AriaException) as exc_info:
        await device_manager.start_copy_vrs_files(
            ["file1.vrs"], Path("/fake/destination")
        )

    assert exc_info.value.error_code == AriaError.VRS_PULL_IN_PROGRESS


@pytest.mark.asyncio
async def test_start_copy_vrs_files_not_vrs_files():
    device_manager = DeviceManager.get_instance()

    with pytest.raises(AriaException) as exc_info:
        await device_manager.start_copy_vrs_files(
            ["file1.vrs"], Path("/fake/destination")
        )

    assert exc_info.value.error_code == AriaError.VRS_PULL_IN_PROGRESS


@pytest.mark.asyncio
async def test_start_copy_vrs_files_file_exists():
    DeviceManager.instance_ = None
    device_manager = DeviceManager.get_instance()
    with patch("pathlib.Path.exists", return_value=True):
        with pytest.raises(FileExistsError):
            await device_manager.start_copy_vrs_files(
                ["file1.vrs"], Path("/fake/destination")
            )


@pytest.mark.asyncio
async def test_start_copy_vrs_files_success():
    DeviceManager.instance_ = None
    device_manager = DeviceManager.get_instance()

    fake_total_size = 100
    device_manager._get_total_size = AsyncMock(return_value=fake_total_size)
    device_manager._copy_monitor = AsyncMock()
    files = ["file1.vrs"]
    destination_path = Path("/fake/destination")
    with patch("pathlib.Path.exists", return_value=False):
        await device_manager.start_copy_vrs_files(files, destination_path)

    assert device_manager._copy_status.total_bytes == fake_total_size
    assert device_manager._copy_status.total_files == len(files)
    assert device_manager._destination == destination_path
    device_manager._copy_monitor.assert_called_once()


@pytest.mark.asyncio
async def test_get_total_size_empty_list():
    DeviceManager.instance_ = None
    instance = DeviceManager.get_instance()
    result = await instance._get_total_size([])
    assert result == 0


@pytest.mark.asyncio
async def test_get_total_size_valid_sizes():
    instance = DeviceManager.get_instance()
    instance._adb_command = AsyncMock(
        side_effect=[("100", None), ("200", None), ("300", None)]
    )

    vrs_files = [Path("/path/to/file1"), Path("/path/to/file2"), Path("/path/to/file3")]
    result = await instance._get_total_size(vrs_files)
    assert result == 600
