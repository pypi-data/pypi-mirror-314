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
This module provides a middleware to check the session of user.
"""

import socket
import bcelogger
from typing import Union
from bceiam.middleware.auth import const
from bceiam.middleware.auth.utils import (
    convert_cookie_to_dict,
    dict_to_cookie_str_safe,
)
from bceiam.services.iam.iam_client import IAMClient
from bceserver.context.singleton_context import SingletonContext
from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware


class IAMSessionError(Exception):
    """
    IAMSessionError
    """

    pass


def iam_session_handler(
    cookies: Union[str, dict[str, str]],
    iam_client: IAMClient,
    auth_info_context: dict[str, str],
) -> Union[IAMSessionError, dict[str, str]]:
    """
    iam session handler
    :param cookies: cookies
    :param iam_client: IAMClient
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

    session_id = cookie_dict.get(const.IAM_SESSION_ID)
    if session_id is None:
        bcelogger.error(f"[IAMSessionHandler]cookie.{const.IAM_SESSION_ID} is empty")
        return IAMSessionError(f"cookie.{const.IAM_SESSION_ID} is empty")

    auth_info_context = {const.AUTH_MODE: const.IAM_SESSION}
    ip = get_ip_address()
    if ip is None:
        ip = "127.0.0.1"

    res = iam_client.auth_iam_session(session_id, ip, cookies)
    if res is None or res.session_context.login_user_info.bce_user_id is None:
        bcelogger.error(
            f"[IAMSessionHandler]session validate failure,{const.IAM_SESSION_ID}:{session_id}, ip:{ip}"
        )
        return IAMSessionError(
            f"session validate failure,{const.IAM_SESSION_ID}:{session_id}, ip:{ip}"
        )

    auth_info_context[const.USER_ID] = res.session_context.login_user_info.bce_user_id
    auth_info_context[const.ORG_ID] = res.session_context.login_user_info.bce_account_id
    auth_info_context[const.USER_NAME] = (
        res.session_context.login_user_info.login_user_name
    )
    auth_info_context[const.PROJECT_ID] = const.IAM_DEFAULT_PROJECT_ID

    context_manager.set_var_value("auth_info", auth_info_context)

    return auth_info_context


def get_ip_address():
    """
    get ip address
    """
    try:
        # 获取本机主机名
        host_name = socket.gethostname()
        # 获取本机 IP 地址
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except Exception as e:
        bcelogger.warning(f"[IAMSessionHandler]get ip address error:{e}")
        return None


class IAMSessionMiddleware(BaseHTTPMiddleware):
    """
    IAMSessionMiddleware
    """

    async def dispatch(self, request, call_next):
        """
        Dispatch
        :param request:
        :param call_next:
        :return:
        """
        if len(request.cookies) == 0:
            bcelogger.error(f"[IAMSessionMiddleware]request.cookies is empty")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": const.ERROR_CODE_UNAUTHORIZED,
                    "message": "[IAMSessionMiddleware]request.cookies is empty",
                },
            )

        context_manager = SingletonContext.instance()

        iam_client = context_manager.get_var_value("iam_client")
        if iam_client is None:
            bcelogger.error(f"[IAMSessionMiddleware]iam client is None")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": const.ERROR_CODE_UNAUTHORIZED,
                    "message": "[IAMSessionMiddleware]iam client is None",
                },
            )

        exist_auth_info = getattr(request.state, "auth_info", {})
        auth_info = iam_session_handler(request.cookies, iam_client, exist_auth_info)
        if isinstance(auth_info, IAMSessionError):
            bcelogger.error(
                f"[IAMSessionMiddleware]session validate failed: {str(auth_info)}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": const.ERROR_CODE_UNAUTHORIZED,
                    "message": f"[IAMSessionMiddleware]session validate failed: {str(auth_info)}",
                },
            )

        setattr(request.state, "auth_info", auth_info)

        return await call_next(request)
