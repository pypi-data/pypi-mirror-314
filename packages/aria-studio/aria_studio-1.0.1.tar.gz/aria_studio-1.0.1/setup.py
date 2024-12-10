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

#
# To build the package, run the following command:
# pip install wheel
# pip install twine (optional) # to upload to pypy/testpypi
# python setup.py sdist bdist_wheel
#

from pathlib import Path
from typing import List

from setuptools import find_packages, setup

_REQUIREMENTS_TXT: Path = Path("aria_studio") / "requirements.txt"
_VERSION_FILE: Path = Path("VERSION")


def read_requirements() -> List[str]:
    """Reads the requirements file and returns a list of dependencies"""
    with open(_REQUIREMENTS_TXT, "r") as fp:
        return [
            line.strip() for line in fp if not (line.isspace() or line.startswith("#"))
        ]


def read_version() -> str:
    """Reads the version from the VERSION file"""
    with open(_VERSION_FILE, "r") as fp:
        return fp.read().strip()


def main() -> None:
    """Main entry point for the setup script"""

    setup(
        name="aria_studio",
        version=read_version(),
        description="Aria Studio",
        long_description="A tool for managing Aria data.",
        author="Meta Reality Labs Research",
        zip_safe=True,
        packages=find_packages(),
        python_requires=">=3.8",
        include_package_data=True,
        install_requires=read_requirements(),
        package_data={
            "aria_studio": [
                "tools/linux/adb",
                "tools/darwin/adb",
                "tools/windows/adb.exe",
                "tools/windows/AdbWinApi.dll",
                "tools/windows/AdbWinUsbApi.dll",
                "frontend/**/*",
                "logging.yml",
            ],
        },
        entry_points={
            "console_scripts": [
                "aria_studio=aria_studio.main:run",
                "viewer_vrs=aria_studio.utils.viewer_vrs:main",
            ],
        },
        license="Apache-2.0",
    )


if __name__ == "__main__":
    main()
