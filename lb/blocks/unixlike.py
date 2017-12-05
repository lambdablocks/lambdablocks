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
This module contains various blocks, which look like their UNIX
friends.
"""


from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry

from typing import List, Any

@block(engine='unixlike')
def cat(filename: str=None):
    """Reads a file.

    :param str filename: The file to read.
    :output List[str] result: The lines of the file.
    """
    def inner() -> ReturnType[List[str]]:
        data = None
        with open(filename) as f:
            data = f.readlines()
        return ReturnEntry(result=data)
    return inner

@block(engine='unixlike')
def grep(pattern: str=None):
    """Greps content.

    :param str pattern: The pattern to grep for.
    :input List[str] data: The data to grep.
    :input List[str] result: The grepped list of string.
    """
    def inner(data: List[str]) -> ReturnType[List[str]]:
        data = list(filter(lambda x: pattern in x, data))
        return ReturnEntry(result=data)
    return inner

@block(engine='unixlike')
def cut(sep: str=None, fields: List[int]=[]):
    """Cuts content.

    :param str sep: The separator.
    :param List[int] fields: The fields to extract.
    :input List[str] data: The list of strings to cut.
    :output List[str] result: The cut list of string.
    """
    def inner(data: List[str]) -> ReturnType[List[str]]:
        fields_ = [y - 1 for y in fields] # 'cut' fields are indexed from 1
        result = []
        for item in data:
            item = item.split(sep)
            result.append(sep.join([item[x] for x in fields_]))
        return ReturnEntry(result=result)
    return inner

@block(engine='unixlike')
def head(n: int=0):
    """Keeps the beginning.

    :input int n: How many items to keep.
    :input List[Any] data: Input data.
    :output List[Any] result: Shortened output.
    """
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        data = data[:n]
        return ReturnEntry(result=data)
    return inner

@block(engine='unixlike')
def tail(n: int=0):
    """Keeps the end.

    :input int n: How many items to keep.
    :input List[Any] data: Input data.
    :output List[Any] result: Shortened output.
    """
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        data = data[-n:]
        return ReturnEntry(result=data)
    return inner
