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

from pprint import pprint
from typing import Any, List

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry


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
