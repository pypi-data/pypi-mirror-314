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

from http import HTTPStatus

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
    AUTHENTICATION_ERROR_CODE,
    LOGIN_SUCCESS_CODE,
    LOGOUT_FAILED_CODE,
    LOGOUT_SUCCESS_CODE,
)
from aria_studio.app.utils import CliAuthHelper, CliHttpHelper, login_required
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from projectaria_tools.aria_mps_cli.cli_lib.authentication import AuthenticationError
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str
    save_token: bool = False


logger = logging.getLogger(__name__)

router = APIRouter()


class LoginResponse(BaseModel):
    """Response from the login endpoint"""

    message: str = Field(..., description="Login message")


class LogoutResponse(BaseModel):
    """Response from the logout endpoint"""

    message: str = Field(..., description="Logout message")


class IsLoggedInResponse(BaseModel):
    """Response for endpoint checking, if user is logged in"""

    logged_in: bool = Field(
        ..., description="True, if user is logged in, false otherwise"
    )


class CurrentUserResponse(BaseModel):
    """Response to a query for logged in user's name"""

    user: str = Field(..., description="Logged in user's name")


@router.post(
    "/login",
    status_code=HTTPStatus.OK,
    summary="API to log in user",
    response_model=LoginResponse,
)
async def login(login: LoginRequest) -> LoginResponse:
    try:
        await CliAuthHelper.get().login(
            username=login.username,
            password=login.password,
            save_token=login.save_token,
        )
        CliHttpHelper.get().set_auth_token(CliAuthHelper.get().auth_token)

        await LocalLogManager.log(
            event=LocalLogEvent.LOGIN,
            screen=LocalLogScreen.LOGIN,
            message="User logged in successfully",
        )
        return LoginResponse(message=LOGIN_SUCCESS_CODE)
    except AuthenticationError:
        await LocalLogManager.log(
            event=LocalLogEvent.LOGIN,
            screen=LocalLogScreen.LOGIN,
            message="Login failed",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTHENTICATION_ERROR_CODE
        )


@router.get(
    "/logout",
    status_code=HTTPStatus.OK,
    summary="API to log out user",
    response_model=LogoutResponse,
)
async def logout() -> LogoutResponse:
    # We get the objects before logging out. To get the objects we need to be logged in.
    group_manager: GroupManager = await GroupManager.get_instance()
    individual_mps_request_manager: IndividualMpsRequestManager = (
        await IndividualMpsRequestManager.get_instance()
    )
    group_mps_request_manager: GroupMpsRequestManager = (
        await GroupMpsRequestManager.get_instance()
    )
    if await CliAuthHelper.get().logout():
        await group_manager.reset()
        await individual_mps_request_manager.reset()
        await group_mps_request_manager.reset()

        logger.info("Logged out successfully.")
        await LocalLogManager.log(
            event=LocalLogEvent.LOGIN,
            screen=LocalLogScreen.LOGIN,
            message="User logged out successfully",
        )
        return LogoutResponse(message=LOGOUT_SUCCESS_CODE)
    else:
        await LocalLogManager.log(
            event=LocalLogEvent.LOGIN,
            screen=LocalLogScreen.LOGIN,
            message="Logout failed",
        )
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=LOGOUT_FAILED_CODE
        )


@router.get(
    "/is-logged-in",
    status_code=HTTPStatus.OK,
    summary="API to check if user is logged in",
    response_model=IsLoggedInResponse,
)
async def is_logged_in() -> Response:
    return IsLoggedInResponse(logged_in=CliAuthHelper.get().is_logged_in())


@login_required
@router.get(
    "/current-user",
    status_code=HTTPStatus.OK,
    summary="API to get the current user's name",
    response_model=CurrentUserResponse,
)
async def current_user() -> CurrentUserResponse:
    return CurrentUserResponse(user=CliAuthHelper.get().user)
