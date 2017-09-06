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

# global variable (singleton) containing the registered hooks
# happening at different execution times
HOOKS = {
    'before_block_execution': [],
    'after_block_execution': [],
    'before_graph_execution': [],
    'after_graph_execution': [],
    }

def _register_hook(f, hookname):
    HOOKS[hookname].append(f)

def before_block_execution(f):
    _register_hook(f, 'before_block_execution')

def after_block_execution(f):
    _register_hook(f, 'after_block_execution')

def before_graph_execution(f):
    _register_hook(f, 'before_graph_execution')

def after_graph_execution(f):
    _register_hook(f, 'after_graph_execution')
