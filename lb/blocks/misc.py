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

from lb.graph import Graph
from lb.registry import block, Registry

import typing

@block()
def topology(filename: str=None):
    def inner(*input_: typing.Any) -> typing.Mapping[str, typing.Any]:
        registry = Registry(load_internal_modules=True)
        g = Graph(filename, registry)
        return g.execute()
    return inner
