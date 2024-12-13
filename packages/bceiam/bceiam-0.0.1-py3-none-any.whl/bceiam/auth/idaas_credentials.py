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
Provides access to the IAM internal credentials used for accessing IDaaS service:
app info for access_token
authorization: Bearer {access_token}
These credentials are used to securely sign requests to IDaaS service.
"""
from bceiam import compat


class IDaaSCredentials(object):
    """
    Provides access to the iam internal credentials used for accessing iam internal service:
    password and username.
    """

    def __init__(self, app_id, client_id, client_secret):
        self.app_id = compat.convert_to_bytes(app_id)
        self.client_id = compat.convert_to_bytes(client_id)
        self.client_secret = compat.convert_to_bytes(client_secret)
