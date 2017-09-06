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

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry

from typing import List

@block(engine='unixlike')
def cat(filename: str=None):
    def inner() -> ReturnType[List[str]]:
        data = None
        with open(filename) as f:
            data = f.readlines()
        return ReturnEntry(result=data)
    return inner

@block(engine='unixlike')
def grep(pattern: str=None):
    def inner(data: List[str]) -> ReturnType[List[str]]:
        data = list(filter(lambda x: pattern in x, data))
        return ReturnEntry(result=data)
    return inner

@block(engine='unixlike')
def cut(sep: str=None, fields: List[int]=[]):
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
    def inner(data: List[str]) -> ReturnType[List[str]]:
        data = data[:n]
        return ReturnEntry(result=data)
    return inner

@block(engine='unixlike')
def tail(n: int=0):
    def inner(data: List[str]) -> ReturnType[List[str]]:
        data = data[-n:]
        return ReturnEntry(result=data)
    return inner
