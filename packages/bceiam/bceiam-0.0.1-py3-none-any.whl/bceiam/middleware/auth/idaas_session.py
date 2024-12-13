# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
idaas session handle
"""
import bcelogger
from typing import Union
from bceiam.middleware.auth import const
from bceiam.middleware.auth.utils import (
    convert_cookie_to_dict,
    dict_to_cookie_str_safe,
)
from bceiam.services.idaas.idaas_client import IDaaSClient
from bceserver.context.singleton_context import SingletonContext
from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware


class IDaaSSessionError(Exception):
    """
    IDaaSSessionError
    """

    pass


def idaas_session_handler(
    cookies: Union[str, dict[str, str]],
    idaas_client: IDaaSClient,
    auth_info_context: dict[str, str],
) -> Union[IDaaSSessionError, dict[str, str]]:
    """
    idaas  session handler
    :param cookies:
    :param idaas_client:
    :param auth_info_context:
    """

    context_manager = SingletonContext.instance()
    if len(auth_info_context) == 0:
        auth_info_context = context_manager.get_var_value("auth_info")

    if auth_info_context is not None:
        if (
            auth_info_context.get(const.ORG_ID) is not None
            and auth_info_context.get(const.USER_ID) is not None
        ):
            return auth_info_context

    cookie_dict = {}
    if isinstance(cookies, str):
        cookie_dict = convert_cookie_to_dict(cookies)

    if isinstance(cookies, dict):
        cookie_dict = cookies
        cookies = dict_to_cookie_str_safe(cookie_dict)

    session_id = cookie_dict.get(const.IDAAS_SESSION_ID)
    project_name = cookie_dict.get(const.IDAAS_PROJECT_NAME)

    if session_id is None or project_name is None:
        bcelogger.error(
            f"[IDaaSSessionHandler]cookie.{const.IDAAS_SESSION_ID} or cookie.{const.IDAAS_PROJECT_NAME} is empty"
        )
        return IDaaSSessionError(
            f"cookie.{const.IDAAS_SESSION_ID} or cookie.{const.IDAAS_PROJECT_NAME} is empty"
        )

    auth_info_context = {const.AUTH_MODE: const.IDAAS_SESSION}

    result = idaas_client.auth_session(session_id, project_name)
    if result is None:
        bcelogger.error(
            f"[IDaaSSessionHandler]session validate failure.{const.IDAAS_SESSION_ID}:{session_id}, {const.IDAAS_PROJECT_NAME}:{project_name}"
        )
        return IDaaSSessionError(
            f"session validate failure.{const.IDAAS_SESSION_ID}:{session_id}, {const.IDAAS_PROJECT_NAME}:{project_name}"
        )

    auth_info_context[const.USER_ID] = result.user.id
    auth_info_context[const.ORG_ID] = result.organization_unit.id
    auth_info_context[const.USER_NAME] = result.user.name
    auth_info_context[const.PROJECT_ID] = result.user.project_id

    context_manager.set_var_value("auth_info", auth_info_context)

    return auth_info_context


class IDaasSessionMiddleware(BaseHTTPMiddleware):
    """
    IDaasSessionMiddleware
    """

    async def dispatch(self, request, call_next):
        """
        Dispatch
        :param request:
        :param call_next:
        :return:
        """
        if len(request.cookies) == 0:
            bcelogger.error(f"[IDaasSessionMiddleware]request.cookies is empty")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": const.ERROR_CODE_UNAUTHORIZED,
                    "message": "[IDaasSessionMiddleware]request.cookies is empty",
                },
            )

        context_manager = SingletonContext.instance()

        idaas_client = context_manager.get_var_value("idaas_client")
        if idaas_client is None:
            bcelogger.error(f"[IDaasSessionMiddleware]idaas client is None")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": const.ERROR_CODE_UNAUTHORIZED,
                    "message": "[IDaasSessionMiddleware]idaas client is None",
                },
            )

        exist_auth_info = getattr(request.state, "auth_info", {})
        auth_info = idaas_session_handler(
            request.cookies, idaas_client, exist_auth_info
        )
        if isinstance(auth_info, IDaaSSessionError):
            bcelogger.error(
                f"[IDaasSessionMiddleware]session validate failed: {str(auth_info)}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": const.ERROR_CODE_UNAUTHORIZED,
                    "message": f"[IDaasSessionMiddleware]session validate failed: {str(auth_info)}",
                },
            )

        setattr(request.state, "auth_info", auth_info)

        return await call_next(request)
