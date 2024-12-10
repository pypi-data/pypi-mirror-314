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
from threading import Event
from typing import List, Mapping

from aria_studio.app.common.types import Group, VisualizationException
from aria_studio.app.constants import (
    CLOSED_LOOP_TRAJECTORY_FILE,
    SEMI_DENSE_POINTS_FILE,
)
from aria_studio.app.groups.group_manager import GroupManager
from aria_studio.app.local.local_log_manager import (
    LocalLogEvent,
    LocalLogManager,
    LocalLogScreen,
)
from aria_studio.utils.rerun_manager import RerunTaskBase

from projectaria_tools.utils.viewer_mps import log_to_rerun


class MpsMultiRerunTask(RerunTaskBase):
    """
    A task to log MPS multi recording feature data to rerun.
    Visualizes all the streams present in the vrs file and overlays available MPS data.

    This task is intended to be used with the RerunManager class.
    """

    def __init__(
        self,
        group_name: str,
    ):
        self._group_name: str = group_name

    def log_to_rerun(self, stop_event: Event) -> None:
        group: Group = asyncio.run(self.get_group())
        closed_loop_trajectories: List[str] = [
            str(x) for x in group.path_on_device.rglob(CLOSED_LOOP_TRAJECTORY_FILE)
        ]
        semi_dense_points: List[str] = [
            str(x) for x in group.path_on_device.rglob(SEMI_DENSE_POINTS_FILE)
        ]

        log_to_rerun(
            vrs_path=None,
            trajectory_files=closed_loop_trajectories,
            points_files=semi_dense_points,
            eye_gaze_file=None,
            wrist_and_palm_poses_file=None,
        )

    async def get_group(self) -> Group:
        """
        Gets the group provided for task from the group manager.

        Returns:
            Group: The group provided for task.
        Raises:
            VisualizationException: If the group is not found in the group manager.
        """

        group_manager: GroupManager = await GroupManager.get_instance()
        groups: Mapping[str, Group] = await group_manager.get_all()
        if self._group_name not in groups:
            await LocalLogManager.log(
                event=LocalLogEvent.VISUALIZATION,
                screen=LocalLogScreen.GROUPS,
                message=f"Group {self._group_name} provided for viewer_mps was not found",
            )
            raise VisualizationException(
                f"Group {self._group_name} provided for viewer_mps was not found"
            )

        return groups[self._group_name]

    def __str__(self):
        return f"MpsMultiRerunTask: (group_name: {self._group_name})"
