# Copyright 2017 The Lambda-blocks developers. See AUTHORS for details.
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

"""
This module contains blocks for performing HTTP operations.
"""

import urllib.request

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry

@block(engine='http')
def read_http(url: str='', encoding: str='utf8'):
    """Performs an HTTP GET requrest, and returns its result.

    :param url: The requested URL.
    :type url: str.
    :param encoding: How the result should be decoded.
    :type encoding: str.
    :returns: A ReturnEntry containing one field, *result*.
    """
    def inner() -> ReturnType[str]:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode(encoding)
        return ReturnEntry(result=data)
    return inner
