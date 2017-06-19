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

from typing import List

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry

@block()
def input():
    def inner() -> ReturnType[List[int]]:
        return ReturnEntry(result=[1,2,3])
    return inner

@block()
def input_str():
    def inner() -> ReturnType[List[str]]:
        return ReturnEntry(result=['a','b','c'])
    return inner

@block()
def sometimes_reverse(reverse: bool=False):
    def inner(data: List[int]) -> ReturnType[List[int]]:
        if reverse:
            res = [data[x] for x in range(len(data) - 1, -1, -1)]
        else:
            res = data
        return ReturnEntry(result=res)
    return inner

@block()
def output_screen():
    def inner(data: List[int]) -> None:
        print(data)
    return inner

@block()
def merge_lists():
    def inner(data1: List[int], data2: List[int]) -> ReturnType[List[int]]:
        return ReturnEntry(result=data1 + data2)
    return inner
