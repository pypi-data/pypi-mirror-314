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
This module contains some utility functions for auth middleware.
"""
from http.cookies import SimpleCookie
from typing import Dict
from urllib.parse import quote


def parse_cookie_str(cookie_str) -> Dict:
    """
    Parse a cookie string into a dictionary.
    """
    # 创建一个 SimpleCookie 对象
    cookie = SimpleCookie(cookie_str)

    # 从 SimpleCookie 对象中获取字典形式的 Cookie
    cookie_dict = {key: value.value for key, value in cookie.items()}
    return cookie_dict


def convert_cookie_to_dict(cookie_str) -> Dict:
    """
    Convert a cookie string to a dictionary.
    :param cookie_str: The cookie string.
    :return: A dictionary of cookie.
    """
    cookie_dict = {}
    for item in cookie_str.split("; "):
        parts = item.split("=", 1)
        if len(parts) == 2:
            key, value = parts
            cookie_dict[key] = value
    return cookie_dict


def dict_to_cookie_str_safe(cookie_dict: dict) -> str:
    """
    Convert a dictionary to a cookie string.
    :param cookie_dict:
    :return:
    """
    return "; ".join(f"{key}={quote(str(value))}" for key, value in cookie_dict.items())
