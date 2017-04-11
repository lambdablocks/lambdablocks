# Copyright 2017 Matthieu Caneill
# Copyright 2017 Univ. Grenoble Alpes
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

import inspect

all_blocks = {}

def block(**kwargs):
    def block_decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        # registers the function
        name = func.__name__
        # gets the function factory parameters
        sig_outer = inspect.signature(func)
        # gets the inner function  parameters
        sig_inner = inspect.signature(func())
        all_blocks[name] = {
            '_func':   func,
            '_parameters': sig_outer.parameters,
            '_inputs': sig_inner.parameters,
            '_output': sig_inner.return_annotation,
            **kwargs}

        return inner
    return block_decorator
