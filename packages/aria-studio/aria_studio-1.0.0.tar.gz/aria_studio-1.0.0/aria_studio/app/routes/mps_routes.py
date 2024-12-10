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


import logging

from dataclasses import asdict
from http import HTTPStatus
from pathlib import Path

from typing import Annotated, Dict, List, Mapping, Optional, Set, Tuple

import jsons

from aria_studio.app.common.types import FeatureStatus, VisualizationException
from aria_studio.app.constants import MESSAGE_MPS_PREPARING
from aria_studio.app.groups.group_manager import GroupManager
from aria_studio.app.local.local_log_manager import (
    LocalLogEvent,
    LocalLogManager,
    LocalLogScreen,
)
from aria_studio.app.mps.group_mps_request_manager import GroupMpsRequestManager
from aria_studio.app.mps.individual_mps_request_manager import (
    IndividualMpsRequestManager,
)
from aria_studio.app.return_codes import (
    FILE_NOT_FOUND_ERROR_CODE,
    MULTI_REQUEST_FAILED_ERROR_CODE,
    MULTI_STATUS_FAILED_ERROR_CODE,
    NO_GROUPS_PROVIDED_ERROR_CODE,
    NO_VRS_FILES_OR_GROUP_PROVIDED_ERROR_CODE,
    NO_VRS_FILES_PROVIDED_ERROR_CODE,
    SINGLE_REQUEST_FAILED_ERROR_CODE,
)
from aria_studio.app.utils import CliHttpHelper, login_required, MpsConfigParser
from aria_studio.utils.mps_multi_rerun_task import MpsMultiRerunTask
from aria_studio.utils.mps_single_rerun_task import MpsSingleRerunTask
from aria_studio.utils.rerun_manager import RerunManager

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from projectaria_tools.aria_mps_cli.cli_lib.constants import CONFIG_FILE
from projectaria_tools.aria_mps_cli.cli_lib.types import MpsFeature, MpsRequest

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router: APIRouter = APIRouter()

logging_counter: int = 0


class MpsIndividualModel(BaseModel):
    """
    Arguments for MPS single feature processing mode.
    See MPS CLI argument list for more details:
    https://facebookresearch.github.io/projectaria_tools/docs/ARK/mps/request_mps/mps_cli_guide#command-line-reference
    """

    features: Set[MpsFeature]
    input: List[Path]

    retry_failed: Optional[bool] = None
    force: Optional[bool] = None


class MpsMultiFeatureModel(BaseModel):
    """
    Arguments for MPS multi feature processing mode.
    See MPS CLI argument list for more details:
    https://facebookresearch.github.io/projectaria_tools/docs/ARK/mps/request_mps/mps_cli_guide#command-line-reference
    """

    groups: List[str]

    retry_failed: Optional[bool] = None
    force: Optional[bool] = None


class MultiRecordingRequestModel(BaseModel):
    force: bool = False
    suffix: str = ""
    retry_failed: bool = False
    output_dir: Path = ""


class IndividualStatusModel(BaseModel):
    vrs_paths: List[Path]


class IndividualRetryRequest(BaseModel):
    vrs_paths: List[Path] = Field(..., min_items=1)


class GroupHighLevelStatusModel(BaseModel):
    groups: List[str]


class ViewMpsRequest(BaseModel):
    vrs_path: Optional[Path] = None
    mps_path: Optional[Path] = None
    group_name: Optional[str] = None


class SingleRequestResponse(BaseModel):
    message: str


class MultiRequestResponse(BaseModel):
    message: str


def remove_none_values(d):
    """
    Recursively remove None values from a dictionary and empty lists.
    """

    if isinstance(d, dict):
        for key in list(d.keys()):
            if d[key] is None:
                del d[key]
            elif isinstance(d[key], list) and not d[key]:
                del d[key]
            else:
                remove_none_values(d[key])
    return d


@login_required
@router.get("/get-all-requests/")
async def get_all_requests() -> JSONResponse:
    requests: List[MpsRequest] = await CliHttpHelper.get().query_all_mps_requests()
    await LocalLogManager.log(
        event=LocalLogEvent.MPS_STATUS,
        screen=LocalLogScreen.SERVICES,
        message=f"Listing all {len(requests)} past user's MPS requests",
    )

    return {"requests": [remove_none_values(asdict(req)) for req in requests]}


@login_required
@router.post(
    "/view_mps",
    status_code=HTTPStatus.OK,
    summary="API to view MPS results along with the vrs file",
)
async def view_mps(request: ViewMpsRequest):
    """
    Execute a system call to open a file with viewer_mps.
    """

    if request.vrs_path:
        task: MpsSingleRerunTask = MpsSingleRerunTask(vrs=str(request.vrs_path))
    elif request.group_name:
        task: MpsMultiRerunTask = MpsMultiRerunTask(group_name=request.group_name)

        try:
            await task.get_group()
        except VisualizationException:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Group not found"
            )
    else:
        await LocalLogManager.log(
            event=LocalLogEvent.VISUALIZATION,
            screen=LocalLogScreen.FILES,
            message="Neither VRS file nor group provided for viewer_mps",
        )
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NO_VRS_FILES_OR_GROUP_PROVIDED_ERROR_CODE,
        )
    manager: RerunManager = RerunManager()
    await manager.start_frozen_rerun()
    await manager.start_viewer(task)


@login_required
# TODO: T188502985 Remove old endpoint after the demo
# @router.post("/single/request")
@router.post(
    "/request-single/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="API to request single MPS feature",
    response_model=SingleRequestResponse,
)
async def single_request(request: MpsIndividualModel):
    if not request.input:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=NO_VRS_FILES_PROVIDED_ERROR_CODE
        )
    for vrs_path in request.input:
        if not vrs_path.is_file():
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=FILE_NOT_FOUND_ERROR_CODE
            )
        try:
            individual_request_manager: IndividualMpsRequestManager = (
                await IndividualMpsRequestManager.get_instance()
            )
            await individual_request_manager.create_request(
                vrs_path, request.features, request.force, request.retry_failed
            )
        except Exception as e:
            logger.exception(e)
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=SINGLE_REQUEST_FAILED_ERROR_CODE,
            )

    return SingleRequestResponse(message=MESSAGE_MPS_PREPARING)


@login_required
@router.post(
    "/individual/retry",
    status_code=status.HTTP_201_CREATED,
    summary="API to retry failed inidividual MPS feature requests",
)
async def single_retry(request: IndividualRetryRequest):
    retried: bool = False
    logger.debug(f"Individual retry request for {request}")
    for vrs_path in set(request.vrs_paths):
        individual_request_manager: IndividualMpsRequestManager = (
            await IndividualMpsRequestManager.get_instance()
        )
        retried = await individual_request_manager.retry_if_failed(vrs_path) or retried
    return status.HTTP_201_CREATED if retried else status.HTTP_204_NO_CONTENT


@login_required
# TODO: T188502985 Remove old endpoint after the demo
# @router.post("/single/status")
@router.post("/check-processing-status/")
async def single_status(request: IndividualStatusModel):
    global logging_counter
    if logging_counter % 30 == 0:
        logging_counter = 0

    if not request.vrs_paths:
        await LocalLogManager.log(
            event=LocalLogEvent.MPS_STATUS,
            screen=LocalLogScreen.FILES,
            message="Cannot get MPS status for Recordings without providing their paths",
        )
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=NO_VRS_FILES_PROVIDED_ERROR_CODE
        )
    status_per_file: Mapping[Path, Mapping[MpsFeature, FeatureStatus]] = {}
    for vrs_path in set(request.vrs_paths):
        if not vrs_path.is_file():
            await LocalLogManager.log(
                event=LocalLogEvent.MPS_STATUS,
                screen=LocalLogScreen.FILES,
                message=f"Cannot get MPS status for Recording {vrs_path}",
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=FILE_NOT_FOUND_ERROR_CODE
            )
        individual_request_manager: IndividualMpsRequestManager = (
            await IndividualMpsRequestManager.get_instance()
        )
        status_per_file[vrs_path] = await individual_request_manager.check_status(
            vrs_path
        )
    # TODO: T188502985 Remove old endpoint after the demo and fix the output schema
    # return status_per_file
    output_old_schema = {}
    for vrs_path, feature_status in status_per_file.items():
        last_request_time = 0
        for _, feature_status_item in feature_status.items():
            if feature_status_item and feature_status_item.creation_time:
                last_request_time = max(
                    last_request_time, feature_status_item.creation_time
                )

        output_old_schema[vrs_path] = {
            "features": feature_status,
            "last_request_date": last_request_time if last_request_time > 0 else None,
        }

        if logging_counter == 0:
            # check is performed about every 2 seconds, log it every minute
            await LocalLogManager.log(
                event=LocalLogEvent.MPS_STATUS,
                screen=LocalLogScreen.FILES,
                message=f"MPS status for {vrs_path} is: {', '.join([f'{k}: {v.status}' for k, v in feature_status.items()])}",
            )
            logger.debug(jsons.dump(output_old_schema, indent=2))

    logging_counter += 1
    return output_old_schema


@login_required
@router.post(
    "/multi/request",
    status_code=HTTPStatus.ACCEPTED,
    response_model=MultiRequestResponse,
    summary="API to request multi MPS feature",
)
async def multi_request(request: MpsMultiFeatureModel):
    try:
        if not request.groups:
            raise Exception("No groups provided")

        group_mps_manager: GroupMpsRequestManager = (
            await GroupMpsRequestManager.get_instance()
        )
        for g in request.groups:
            await group_mps_manager.create_request(
                g, request.force, request.retry_failed
            )
        return MultiRequestResponse(message=MESSAGE_MPS_PREPARING)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=MULTI_REQUEST_FAILED_ERROR_CODE
        )


def _get_high_level_status(
    status: Mapping[Path, Mapping[MpsFeature, FeatureStatus]],
) -> Tuple[Optional[str], Optional[int]]:
    logger.debug(f"Status is {status}")
    if not status:
        return None, None
    processing: bool = False
    for _, feature_feature_status in status.items():
        feature_status = feature_feature_status[MpsFeature.MULTI_SLAM]
        if feature_status.status == "Error":
            return "Failed", feature_status.error_code
        elif feature_status.status != "Success":
            processing = True
    s = "Processing" if processing else "Success"
    return s, None


@login_required
# TODO: T188502985 Remove old endpoint after the demo
# @router.post("/multi/status_summary")
@router.post("/multi/high_level_status")
async def multi_status_summary(request: GroupHighLevelStatusModel):
    ## TODO: strongly type the response
    global logging_counter
    if logging_counter % 30 == 0:
        logging_counter = 0

    status_by_group: Dict[str, str] = {}
    if not request.groups:
        await LocalLogManager.log(
            event=LocalLogEvent.MPS_STATUS,
            screen=LocalLogScreen.GROUPS,
            message="Cannot get MPS status for groups without providing their names",
        )
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=NO_GROUPS_PROVIDED_ERROR_CODE
        )
    group_mps_manager: GroupMpsRequestManager = (
        await GroupMpsRequestManager.get_instance()
    )
    for group in request.groups:
        status = await group_mps_manager.check_status(group)
        status_by_group[group], err_code = _get_high_level_status(status)

        if logging_counter == 0:
            # check is performed about every 2 seconds, log it every minute
            await LocalLogManager.log(
                event=LocalLogEvent.MPS_STATUS,
                screen=LocalLogScreen.GROUPS,
                message=f"MPS status for {group} is: {status_by_group[group]}",
            )
            logger.info(f"MPS status for {group} is: {status_by_group[group]}")

    logging_counter += 1
    return JSONResponse(status_code=HTTPStatus.OK, content=jsons.dump(status_by_group))


@login_required
@router.get("/multi/status")
async def multi_status(group: str, vrs_path: Annotated[Path | None, Query()] = None):
    try:
        ## TODO: strongly type the response
        group_mps_manager: GroupMpsRequestManager = (
            await GroupMpsRequestManager.get_instance()
        )
        status_by_file = await group_mps_manager.check_status(group)
        output_old_schema = {}
        if status_by_file and vrs_path:
            if status_by_file and vrs_path not in status_by_file:
                await LocalLogManager.log(
                    event=LocalLogEvent.MPS_STATUS,
                    screen=LocalLogScreen.GROUPS,
                    message=f"Requested MPS status for VRS file {vrs_path} not found in group {group}",
                )
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="File not found"
                )
            # TODO: T188502985 Remove old endpoint after the demo and fix the output schema
            # return status_per_file
            # return status.get(vrs_path, {})
            if vrs_path not in status_by_file:
                await LocalLogManager.log(
                    event=LocalLogEvent.MPS_STATUS,
                    screen=LocalLogScreen.GROUPS,
                    message=f"Requested MPS status for VRS file {vrs_path} not found in group {group}",
                )
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="File not found"
                )
            feature_status = status_by_file[vrs_path]
            last_request_time = 0
            for _, f_status in feature_status.items():
                last_request_time = max(last_request_time, f_status.creation_time or 0)

            output_old_schema[vrs_path] = {
                "features": feature_status,
                "last_request_date": (
                    last_request_time if last_request_time > 0 else None
                ),
            }
        elif status_by_file:
            group_status, err_code = _get_high_level_status(status_by_file)
            last_request_time = 0
            for _, feature_status in status_by_file.items():
                for _, feature_status_item in feature_status.items():
                    last_request_time = max(
                        last_request_time, feature_status_item.creation_time or 0
                    )
            last_request_time = last_request_time if last_request_time > 0 else None
            group_manager: GroupManager = await GroupManager.get_instance()
            output_old_schema[group] = {
                "features": {
                    MpsFeature.MULTI_SLAM: FeatureStatus(
                        status=group_status,
                        # Error code is a string for more flexibility.
                        error_code=err_code,
                        creation_time=last_request_time,
                        output_path=(await group_manager.get(group)).path_on_device,
                    ),
                },
                "last_request_date": last_request_time,
            }

        try:
            status: str = output_old_schema[
                vrs_path if vrs_path is not None else group
            ]["features"][MpsFeature.MULTI_SLAM].status
        except KeyError:
            # it group not in the output schema, it means that it has not been requested yet
            status: str = "None"

        await LocalLogManager.log(
            event=LocalLogEvent.MPS_STATUS,
            screen=LocalLogScreen.GROUPS,
            message=f"MPS status for group {group} is {status}",
        )
        return output_old_schema
    except Exception as e:
        await LocalLogManager.log(
            event=LocalLogEvent.MPS_STATUS,
            screen=LocalLogScreen.GROUPS,
            message=f"Cannot get MPS status for group {group}",
        )
        logger.exception(e)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=MULTI_STATUS_FAILED_ERROR_CODE
        )


class DefaultConfig(BaseModel):
    """Default section of MPS CLI settings response"""

    log_dir: Optional[str] = Field(
        None, description="The local path to stroe logs from MPS CLI"
    )
    status_check_interval: Optional[int] = Field(
        None, description="Status check interval in seconds"
    )


class HashConfig(BaseModel):
    """Hash section of MPS CLI settings response"""

    concurrent_hashes: Optional[int] = Field(
        None, description="Number of concurrent hashes"
    )
    chunk_size: Optional[int] = Field(None, description="Hash chunk size")


class HealthCheckConfig(BaseModel):
    """Health check section of MPS CLI settings response"""

    concurrent_health_checks: Optional[int] = Field(
        None, description="Number of concurrent health checks"
    )


class EncryptionConfig(BaseModel):
    """Encryption section of MPS CLI settings response"""

    chunk_size: Optional[int] = Field(None, description="Encryption chunk size")
    concurrent_encryptions: Optional[int] = Field(
        None, description="Number of concurrent encryptions"
    )
    delete_encrypted_files: Optional[bool] = Field(
        None, description="Delete encrypted files"
    )


class UploadConfig(BaseModel):
    """Upload section of MPS CLI settings response"""

    backoff: Optional[float] = Field(None, description="Backoff time in seconds")
    concurrent_uploads: Optional[int] = Field(
        None, description="Number of concurrent uploads"
    )
    interval: Optional[int] = Field(None, description="Upload interval in seconds")
    max_chunk_size: Optional[int] = Field(None, description="Max chunk size")
    min_chunk_size: Optional[int] = Field(None, description="Min chunk size")
    retries: Optional[int] = Field(None, description="Number of retries")
    smoothing_window_size: Optional[int] = Field(
        None, description="Smoothing window size"
    )
    target_chunk_upload_secs: Optional[int] = Field(
        None, description="Target chunk upload time in seconds"
    )


class DownloadConfig(BaseModel):
    """Download section of MPS CLI settings response"""

    backoff: Optional[float] = Field(None, description="Backoff factor")
    chunk_size: Optional[int] = Field(None, description="Chunk size")
    concurrent_downloads: Optional[int] = Field(
        None, description="Number of concurrent downloads"
    )
    delete_zip: Optional[bool] = Field(None, description="Delete zip file")
    interval: Optional[int] = Field(None, description="Download interval in seconds")
    retries: Optional[int] = Field(None, description="Number of retries")


class GraphQLConfig(BaseModel):
    """GraphQL section of MPS CLI settings response"""

    backoff: Optional[float] = Field(None, description="Backoff factor")
    interval: Optional[int] = Field(None, description="GraphQL interval in seconds")
    retries: Optional[int] = Field(None, description="Number of retries")


class MPSConfig(BaseModel):
    """MPS CLI settings response model"""

    DEFAULT: Optional[DefaultConfig] = Field(
        None, description="Default section of MPS CLI settings response"
    )
    HASH: Optional[HashConfig] = Field(
        None, description="Hash section of MPS CLI settings response"
    )
    HEALTH_CHECK: Optional[HealthCheckConfig] = Field(
        None, description="Health check section of MPS CLI settings response"
    )
    ENCRYPTION: Optional[EncryptionConfig] = Field(
        None, description="Encryption section of MPS CLI settings response"
    )
    UPLOAD: Optional[UploadConfig] = Field(
        None, description="Upload section of MPS CLI settings response"
    )
    DOWNLOAD: Optional[DownloadConfig] = Field(
        None, description="Download section of MPS CLI settings response"
    )
    GRAPHQL: Optional[GraphQLConfig] = Field(
        None, description="GraphQL section of MPS CLI settings response"
    )


@router.get(
    "/settings",
    response_model=MPSConfig,
    status_code=status.HTTP_200_OK,
    summary="API to read the mps.ini file for MPS CLI configuration",
)
def get_mps_settings() -> MPSConfig:
    if not CONFIG_FILE.is_file():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Config file not found"
        )
    try:
        config = MpsConfigParser(inline_comment_prefixes="#")
        config.read(CONFIG_FILE)
        json_data = config.ini_to_json()
        return MPSConfig(**json_data)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Unable to read config"
        )


@router.post(
    "/settings",
    status_code=status.HTTP_200_OK,
    summary="API to update the mps.ini file",
)
def update_mps_config(request: MPSConfig) -> JSONResponse:
    if not CONFIG_FILE.is_file():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Config file not found"
        )
    try:
        config = MpsConfigParser(inline_comment_prefixes="#")
        config.read(CONFIG_FILE)
        # remove the unset values from the request model
        updated_config = request.model_dump(exclude_unset=True)
        config.update_to_ini(updated_config)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"message": "Config updated successfully"},
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Failed to update config"
        )
