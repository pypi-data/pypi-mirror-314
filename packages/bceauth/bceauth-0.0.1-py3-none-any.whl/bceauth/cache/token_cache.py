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
This module provide base class for token cache.
"""

from collections import OrderedDict
from datetime import datetime as dt


class TokenCache:
    """
    cache access_token in idaas or x-auth-token in iam
    """

    def __init__(self):
        self.token_map = OrderedDict()
        self.cache_size = 300
        self.enabled = True

    def get_token(self, token_key):
        """
        :type token_key: str
        :return token_str: str
        """
        if not self.enabled:
            return None
        token = self.token_map.get(token_key)
        if token is None:
            return None
        current_time = dt.now()
        expire_at = token.expire_at
        issue_at = token.issue_at
        del self.token_map[token_key]

        midpoint = issue_at + (expire_at - issue_at) / 2

        if current_time >= midpoint:
            return None
        self.add_token(token_key, token)
        return token.token_str

    def add_token(self, token_key, token):
        """
        :type token_key: str
        :type token: Token
        """
        if not self.enabled:
            return
        if len(self.token_map) >= self.cache_size:
            del self.token_map[token_key]
        self.token_map[token_key] = token


class Token:
    """
    token class, include token_str, issue_at, expire_at
    """

    def __init__(self, token_str, issue_at, expire_at):
        self.token_str = token_str
        self.issue_at = issue_at
        self.expire_at = expire_at
