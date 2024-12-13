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
Provides access to the IAM internal credentials used for accessing IAM internal service: Username and password for token
x-auth-token: {tokenId}
These credentials are used to securely sign requests to IAM internal service.
"""
from bceiam import compat


class IAMCredentials(object):
    """
    Provides access to the iam internal credentials used for accessing iam internal service:
    password and username.
    """

    def __init__(self, username, password):
        self.username = compat.convert_to_bytes(username)
        self.password = compat.convert_to_bytes(password)
