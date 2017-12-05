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
This plugin allows for a very basic representation of the graph,
showing for each vertice its inner and outer links.
"""

from lb.plugins_manager import before_graph_execution

@before_graph_execution
def show_dag(vertices, entry_points):
    for v in vertices.values():
        print(v.fields['name'])
        print(' from:')
        for prev in v.prev_vertices:
            print('  {} -> {}'.format(prev.block_from.fields['name'], prev.value_from))
        print(' to:')
        for to in v.next_vertices:
            print('  {} -> {}'.format(to.block_dest.fields['name'], to.value_dest))
        print('____________________')
