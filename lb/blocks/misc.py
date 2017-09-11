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

import itertools

from pprint import pprint
from typing import Any, Callable, List, Tuple

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry, default_function


@block(engine='all')
def show_console():
    """
    Pretty prints in green on the console.
    """
    def inner(data: Any):
        print('\033[92m') # green
        pprint(data)
        print('\033[0m')
    return inner

@block(engine='all')
def write_line(filename: str=''):
    def inner(data: str):
        with open(filename, 'w') as f:
            f.write(data)
    return inner

@block(engine='all')
def write_lines(filename: str=''):
    def inner(data: List[str]):
        with open(filename, 'w') as f:
            for line in data:
                line += '\n'
                f.write(line)
    return inner

@block(engine='all')
def split(sep: str='\n'):
    def inner(data: str) -> ReturnType[List[str]]:
        return ReturnEntry(result=data.split(sep))
    return inner

@block(engine='all')
def concatenate(sep: str='\n'):
    def inner(data: List[Any]) -> ReturnType[Any]:
        return ReturnEntry(result=sep.join(data))
    return inner

@block(engine='all')
def map_list(func: Callable[[Any], Any]=default_function(1)):
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        return ReturnEntry(result=list(map(func, data)))
    return inner

@block(engine='all')
def flatMap(func: Callable[[Any], List[Any]]=default_function(1, [])):
    """
    Applies a map function to every item, and then flattens the result.
    [a,b,c] -> [[x,y],[z],[]] -> [x,y,z]
    """
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        result = []
        for item in data:
            result.extend(func(item))
        return ReturnEntry(result=result)
    return inner

@block(engine='all')
def flatten_list():
    def inner(data: List[List[Any]]) -> ReturnType[List[Any]]:
        result = []
        for item in data:
            result.extend(item)
        return ReturnEntry(result=result)
    return inner

@block(engine='all')
def group_by_count():
    """
    Groups items in a similar manner as SQL's `COUNT()…GROUP BY()`.
    """
    def inner(data: List[Any]) -> ReturnType[List[Tuple[Any,int]]]:
        grouped = itertools.groupby(sorted(data))
        result = map(lambda x: (x[0], len(list(x[1]))), grouped)
        return ReturnEntry(result=list(result))
    return inner

@block(engine='unixlike')
def sort(key: Callable[[Any], Any]=default_function(1),
         reverse: bool=False):
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        result = sorted(data, key=key, reverse=reverse)
        return ReturnEntry(result=result)
    return inner
