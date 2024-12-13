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
This module provides a client for IAM internal.
"""
import copy
import datetime
import json
import logging
from datetime import datetime as dt

from bceiam.auth import bce_v1_signer
from bceiam.bce_base_client import BceBaseClient
from bceiam.cache.token_cache import TokenCache, Token
from bceiam.http import bce_http_client
from bceiam.http import handler
from bceiam.http import http_content_types
from bceiam.http import http_headers
from bceiam.http import http_methods
from bceiam.services import iam
from bceiam.auth.bce_credentials import BceCredentials

_logger = logging.getLogger(__name__)


class IAMClient(BceBaseClient):
    """
    sdk client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)
        self.token_cache = TokenCache()

    def signature_validate(self, authorization, request, security_token=None):
        """
        :type authorization: str

        :type request: dict

        :type security_token: str

        :return:
            **HttpResponse**
        """
        signature_validator = {
            "auth": {
                "authorization": authorization,
                "request": request,
                "security_token": security_token,
            }
        }

        body = json.dumps(signature_validator)
        response = self._send_iam_request(
            http_methods.POST,
            b"/v3/BCE-CRED/accesskeys",
            body=body,
            headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
            params=None,
        )
        return response.token

    def _get_x_auth_token(self, username, password, domain=None):
        """
        :type username: str

        :type password: str

        :return:
            **HttpResponse**
        """
        token_str = self.token_cache.get_token(
            token_key=iam.TOKEN_PREFIX + username + password
        )
        if token_str is not None:
            return token_str

        if domain is None:
            domain = "Default"

        auth_body = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {"name": domain},
                            "name": str(username, "utf-8"),
                            "password": str(password, "utf-8"),
                        }
                    },
                },
                "scope": {"domain": {"name": "Default"}},
            }
        }
        body = json.dumps(auth_body)
        response = self._send_iam_request(
            http_methods.POST,
            iam.URL_PREFIX + b"/auth/tokens",
            body=body,
            headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
            params=None,
            need_x_auth_token=False,
        )

        if response is None or response.token is None:
            _logger.error("could not get x-auth-token, response:%s", response)
        issue_at = dt.now()
        expire_at = issue_at + datetime.timedelta(seconds=3600)

        x_auth_token = response.metadata.get_attribute("x_subject_token")

        self.token_cache.add_token(
            iam.TOKEN_PREFIX + username + password,
            Token(x_auth_token, issue_at, expire_at),
        )
        return x_auth_token

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_iam_request(
        self,
        http_method,
        path,
        body=None,
        headers=None,
        params=None,
        config=None,
        body_parser=None,
        need_x_auth_token=True,
        need_sign_for_sts=False,
    ):
        config = self._merge_config(config)
        if need_x_auth_token:
            x_auth_token = self._get_x_auth_token(
                config.iam_credentials.username, config.iam_credentials.password
            )
            headers[http_headers.X_AUTH_TOKEN] = x_auth_token

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
            need_sign_for_sts,
        )

    def auth_iam_session(self, session_id: str, ip: str, cookie: str):
        """
        auth session
        session_id: str
        ip: str
        cookie: str
        """
        try:
            url = b"/v4/bce/session/" + session_id.encode("utf-8")
            if ip is None:
                ip = "127.0.0.1"
            if cookie is None:
                _logger.error("cookie is None!session_id:{}".format(session_id))
                return None

            headers = {
                http_headers.BCE_IP: ip.encode("utf-8"),
                http_headers.BCE_COOKIES: cookie.encode("utf-8"),
            }
            response = self._send_iam_request(
                http_methods.GET,
                url,
                body=None,
                headers=headers,
                params=None,
                need_x_auth_token=False,
                config=None,
                need_sign_for_sts=True,
            )
            if response is None:
                _logger.error("could not auth session, response:%s", response)

            return response
        except Exception as e:
            _logger.error("iam auth session, session_id:{},e:{}".format(session_id, e))
            return None
