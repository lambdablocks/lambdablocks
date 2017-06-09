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

import typing

from lb.graph import Graph
from lb.registry import block, Registry
from lb.types import ReturnType
from lb.utils import ReturnEntry

@block()
def topology(filename: str=None,
             bind_out: typing.Mapping[str, str]={}):
    def inner(**inputs: typing.Any) -> ReturnType[typing.Any]:
        registry = Registry(load_internal_modules=True)
        g = Graph(filename, registry, inputs=inputs)
        results = g.execute()
        filtered_results = {}
        for k, v in bind_out.items():
            blockname, value = v.split('.')
            filtered_results[k] = getattr(results[blockname], value)
        return ReturnEntry(**filtered_results)
    return inner
