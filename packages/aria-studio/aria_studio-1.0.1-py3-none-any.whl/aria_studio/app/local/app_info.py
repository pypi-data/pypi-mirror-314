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
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Final

logger = logging.getLogger(__name__)

try:
    from aria_studio.app.local.meta_app_info import get_version_file_path

    __VERSION_FILE: Final[Path] = get_version_file_path()
except ImportError:
    __VERSION_FILE: Final[Path] = Path("VERSION")

__PREFIX_VERSION: Final[str] = "Version: "
__SUFFIX_DEVELOPMENT: Final[str] = "-development"
__DEFAULT_VERSION: Final[str] = "unknown"
__SUFFIX_ELECTRON: Final[str] = "S"


async def get_app_version() -> str:
    """
    Gets the Aria Studio Version
    """

    version: str = __DEFAULT_VERSION

    if __VERSION_FILE.is_file():
        with open(__VERSION_FILE, "r") as fp:
            version = f"{fp.read().strip()}{__SUFFIX_DEVELOPMENT}"
            logger.info(f"Read version from file {version}")
    elif getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Running from a PyInstaller bundle, so we need to read the version from the bundled file
        version_file = os.path.join(sys._MEIPASS, "aria_studio", "VERSION")
        with open(version_file, "r") as fp:
            version = f"{fp.read().strip()}{__SUFFIX_ELECTRON}"
            logger.info(f"Read Electron version from file {version}")
    else:
        process = await asyncio.create_subprocess_exec(
            *["pip3", "show", "aria_studio"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.error(f'"pip3 show aria_studio" failed with {process.returncode}')
            logger.error(f"Read package version failed {stderr.decode()}")
            logger.error(f"Running from directory {Path.cwd()}")
        else:
            """
            Sample output of "pip3 show aria_studio" command:

            Name: aria_studio
            Version: 0.1.0b1
            Summary: Aria Studio
            Home-page:
            Author: Meta Reality Labs Research
            Author-email:
            License: Apache-2.0
            Location: /Users/brzyski/venv/aria_studio/lib/python3.11/site-packages
            Requires: aiofiles, aiohttp, aioredis, aiosqlite, annotated-types, anyio, async-timeout, attrs, certifi, charset-normalizer, click, dataclasses, dnspython, email-validator, exceptiongroup, fastapi, fastapi-cache, fastapi-cli, h11, hiredis, httpcore, httptools, httpx, idna, imageio, iniconfig, Jinja2, jsons, markdown-it-py, MarkupSafe, mdurl, numpy, orjson, packaging, pillow, pluggy, projectaria-tools, pyarrow, pycryptodome, pydantic, pydantic-core, Pygments, pytest, python-dotenv, python-multipart, PyYAML, requests, rerun-sdk, rich, shellingham, sniffio, soupsieve, starlette, textual, tomli, tqdm, transitions, typer, typing, typing-extensions, typish, ujson, urllib3, uvicorn, uvloop, vrs, watchfiles, websockets, xxhash
            Required-by:
            """

            output: str = stdout.decode()
            try:
                version = next(
                    x[len(__PREFIX_VERSION) :]
                    for x in output.splitlines()
                    if x.startswith(__PREFIX_VERSION)
                )
                logger.info(f"Read version from package {version}")
            except StopIteration:
                logger.error("Read package version failed")

    return version
