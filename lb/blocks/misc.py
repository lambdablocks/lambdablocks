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
    """Pretty prints in green on the console.

    :input Any data: The field you want to display.
    """
    def inner(data: Any):
        print('\033[92m') # green
        pprint(data)
        print('\033[0m')
    return inner

@block(engine='all')
def write_line(filename: str=''):
    """Writes a string in a file.

    :param str filename: The file you want to write to.
    :input str data: The value to write in the file.
    """
    def inner(data: str):
        with open(filename, 'w') as f:
            f.write(data)
    return inner

@block(engine='all')
def write_lines(filename: str=''):
    """Writes strings in a file, all on a new line.

    :param str filename: The file you want to write to.
    :input List[str] data: The values to write in the file.
    """
    def inner(data: List[str]):
        with open(filename, 'w') as f:
            for line in data:
                line += '\n'
                f.write(line)
    return inner

@block(engine='all')
def split(sep: str='\n'):
    """Splits a string.

    :param str sep: The separator on which to split.
    :input str data: The string you want to split.
    :output List[str] result: The list of splits.
    """
    def inner(data: str) -> ReturnType[List[str]]:
        return ReturnEntry(result=data.split(sep))
    return inner

@block(engine='all')
def concatenate(sep: str='\n'):
    """Joins a list of strings.

    :param str sep: What will separate the strings in the result.
    :input List[Any] data: The list of items you want to join.
    :output Any result: The joined result.
    """
    def inner(data: List[Any]) -> ReturnType[Any]:
        return ReturnEntry(result=sep.join(data))
    return inner

@block(engine='all')
def map_list(func: Callable[[Any], Any]=default_function(1)):
    """Applies a function to every element of a list and returns the
    resulting list.

    :param Callable func: The function to apply.
    :input List[Any] data: The input list.
    :output List[Any] result: The mapped list.
    """
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        return ReturnEntry(result=list(map(func, data)))
    return inner

@block(engine='all')
def flatMap(func: Callable[[Any], List[Any]]=default_function(1, [])):
    """Applies a map function to every item, and then flattens the result.

    ``[a,b,c] -> [[x,y],[z],[]] -> [x,y,z]``

    :param Callable func: The function to apply.
    :input List[Any] data: The input list.
    :output List[Any] result: The mapped list.
    """
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        result = []
        for item in data:
            result.extend(func(item))
        return ReturnEntry(result=result)
    return inner

@block(engine='all')
def flatten_list():
    """Flattens a list of lists.

    ``[[a,b],[c,d]] -> [a,b,c,d]``

    :input List[List[Any]] data: The list to flatten.
    :output List[Any] result: The flattened list.
    """
    def inner(data: List[List[Any]]) -> ReturnType[List[Any]]:
        result = []
        for item in data:
            result.extend(item)
        return ReturnEntry(result=result)
    return inner

@block(engine='all')
def group_by_count():
    """Groups items in a similar manner as SQL's ``COUNT()…GROUP BY()``.

    :input List[Any] data: The list to group and count.
    :output List[Tuple[Any,int]] result: A list of tuples (item, count).
    """
    def inner(data: List[Any]) -> ReturnType[List[Tuple[Any,int]]]:
        grouped = itertools.groupby(sorted(data))
        result = map(lambda x: (x[0], len(list(x[1]))), grouped)
        return ReturnEntry(result=list(result))
    return inner

@block(engine='unixlike')
def sort(key: Callable[[Any], Any]=default_function(1),
         reverse: bool=False):
    """Sorts a list.

    :param Callable key: A function to select the element to sort on, similar to Python's key argument to list.sort.
    :param bool reverse: Set to true to return the inverted result.
    :input List[Any] data: The list to sort.
    :output List[Any] result: The sorted list.
    """
    def inner(data: List[Any]) -> ReturnType[List[Any]]:
        result = sorted(data, key=key, reverse=reverse)
        return ReturnEntry(result=result)
    return inner
