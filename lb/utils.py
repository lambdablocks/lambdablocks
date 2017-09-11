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
Misc. utilities.
"""

from collections import namedtuple
from typing import Any

def ReturnEntry(**kwargs):
    R = namedtuple('R', kwargs.keys())
    return R(**kwargs)

def default_function(n: int, value: Any=None):
    """
    Creates a dummy default function to provide as default value when
    a func parameter is expected.
    `n` is the number of parameters expected.
    `value` is the default value returned by the function
    """
    if n == 0:
        return lambda: value
    elif n == 1:
        return lambda _: value
    elif n == 2:
        return lambda _,__: value
    else:
        raise Exception('Default function with {} parameters is not supported.'.format(n))
