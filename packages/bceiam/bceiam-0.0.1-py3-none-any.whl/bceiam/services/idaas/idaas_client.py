# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
This module provides a client for IDaaS.
"""
import copy
import datetime
import json
import logging
from builtins import str
from datetime import datetime as dt, timedelta

from bceiam.auth import bce_v1_signer
from bceiam.bce_base_client import BceBaseClient
from bceiam.cache.token_cache import TokenCache, Token
from bceiam.http import bce_http_client
from bceiam.http import handler
from bceiam.http import http_content_types
from bceiam.http import http_headers
from bceiam.http import http_methods
from bceiam.services import idaas

_logger = logging.getLogger(__name__)


class IDaaSClient(BceBaseClient):
    """
    sdk client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)
        self.token_cache = TokenCache()

    def auth_session(
        self,
        session_id,
        project_id,
        check_permission=None,
        user_authorization_request=None,
    ):
        """
        :type session_id: str

        :type project_id: str

        :type check_permission: bool

        :type user_authorization_request: dict

        :return:
            **HttpResponse**
        """
        user_session_request = {
            "sessionId": session_id,
            "checkPermission": check_permission,
        }
        if check_permission and user_authorization_request is None:
            user_session_request["authRequest"] = user_authorization_request
        body = json.dumps(user_session_request)
        params = {"projectName": project_id}
        response = self._send_idaas_request(
            http_methods.POST,
            b"/idgate/v1/user/authSession",
            body=body,
            headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
            params=params,
        )
        return response.result

    def user_authorization(self, user_authorization_request):
        """
        :param user_authorization_request: dict
        :return:
            **HttpResponse**
        """
        if user_authorization_request is None:
            body = None
        elif not isinstance(user_authorization_request, dict):
            raise TypeError(b"user_authorization_request should be dict")
        else:
            body = json.dumps(user_authorization_request)
        response = self._send_idaas_request(
            http_methods.POST,
            idaas.URL_PREFIX + b"/authorization/user/resource/permission",
            body=body,
            headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
        )
        return response.result

    def _get_access_token(self, app_id, client_id, client_secret, project_id=None):
        """
        :type app_id: bytes

        :type client_id: str

        :type client_secret: str

        :type project_id: str

        :return:
            **HttpResponse**
        """
        token_str = self.token_cache.get_token(token_key=idaas.TOKEN_PREFIX + client_id)
        if token_str is not None:
            return token_str
        params = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if project_id is not None:
            if isinstance(project_id, str):
                params["projectId"] = project_id

        response = self._send_idaas_request(
            http_methods.POST,
            b"/app/oauth/" + app_id + b"/token",
            body=None,
            headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
            params=params,
            need_access_token=False,
        )

        if response is None or response.access_token is None:
            _logger.error("could not get access_token, response:%s", response)
        issue_at = dt.now()
        expires_in = 1800
        if response.expires_in is not None:
            expires_in = response.expires_in
        expire_at = issue_at + datetime.timedelta(seconds=expires_in)
        self.token_cache.add_token(
            idaas.TOKEN_PREFIX + client_id,
            Token(response.access_token, issue_at, expire_at),
        )
        return response.access_token

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_idaas_request(
        self,
        http_method,
        path,
        body=None,
        headers=None,
        params=None,
        config=None,
        body_parser=None,
        need_access_token=True,
    ):
        config = self._merge_config(config)
        if need_access_token:
            access_token = self._get_access_token(
                config.idaas_credentials.app_id,
                config.idaas_credentials.client_id,
                config.idaas_credentials.client_secret,
            )
            headers[http_headers.AUTHORIZATION] = "Bearer " + access_token

        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config,
            bce_v1_signer.sign,
            [handler.parse_error, body_parser],
            http_method,
            path,
            body,
            headers,
            params,
        )
