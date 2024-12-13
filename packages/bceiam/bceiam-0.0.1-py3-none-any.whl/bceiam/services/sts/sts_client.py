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
This module provides a client for STS.
"""

from future.utils import iteritems
import copy
import http.client
import os
import json
import logging
import shutil
from builtins import str
from builtins import bytes

import bceiam
from bceiam import bce_client_configuration
from bceiam import utils
from bceiam.auth import bce_v1_signer
from bceiam.bce_base_client import BceBaseClient
from bceiam.exception import BceClientError
from bceiam.exception import BceServerError
from bceiam.exception import BceHttpClientError
from bceiam.http import bce_http_client
from bceiam.http import handler
from bceiam.http import http_content_types
from bceiam.http import http_headers
from bceiam.http import http_methods
from bceiam.services import sts
from bceiam.utils import required

_logger = logging.getLogger(__name__)


class StsClient(BceBaseClient):
    """
    sdk client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    def assume_role(self, account_id, sts_role_name, duration_seconds=None, acl=None):
        """
        :type account_id: str, in idaas, account_id is project_id or user_id
        :param

        :type sts_role_name: str,   such as: sts_role_name=IOT_DEFAULT_ROLE

        :type duration_seconds: int
        :param duration_seconds: None

        :type id: string
        :param id: None
        :acl id

        :type acl: dict
        :param acl: None
        :acl

        :return:
            **HttpResponse**
        """
        params = {}

        if duration_seconds is not None:
            if isinstance(duration_seconds, int):
                params = {b"durationSeconds": duration_seconds}
        params["assumeRole"] = ""
        params["accountId"] = account_id
        params["roleName"] = sts_role_name

        if acl is None:
            body = None
        else:
            if not isinstance(acl, dict):
                raise TypeError(b"acl should be dict")
            if "id" in acl:
                body = json.dumps(acl)
            else:
                body = json.dumps(acl, default=self._dump_acl_object)

        return self._send_sts_request(
            http_methods.POST,
            path=sts.URL_PREFIX + b"/credential",
            body=body,
            headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
            params=params,
        )

    def get_session_token(self, acl=None, duration_seconds=None):
        """
        :type duration_seconds: int
        :param duration_seconds: None
        :token effective period

        :type id: string
        :param id: None
        :acl id

        :type acl: dict
        :param acl: None
        :acl

        :return:
            **HttpResponse**
        """

        params = {}

        if duration_seconds is not None:
            if isinstance(duration_seconds, int):
                params = {b"durationSeconds": duration_seconds}
        else:
            params = {b"durationSeconds": 1800}
        if acl is None:
            body = None
        else:
            if not isinstance(acl, dict):
                raise TypeError(b"acl should be dict")
            if "id" in acl:
                body = json.dumps(acl)
            else:
                body = json.dumps(acl, default=self._dump_acl_object)

        return self._send_sts_request(
            http_methods.POST,
            sts.URL_PREFIX + b"/sessionToken",
            body=body,
            headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
            params=params,
        )

    @staticmethod
    def _dump_acl_object(acl):
        result = {}
        for k, v in iteritems(acl.__dict__):
            if not k.startswith("_"):
                result[k] = v
        return result

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_sts_request(
        self,
        http_method,
        path,
        body=None,
        headers=None,
        params=None,
        config=None,
        body_parser=None,
    ):
        config = self._merge_config(config)

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
            need_sign_for_sts=True,
        )
