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
TimingGraph is an example of a Graph extension: it measures the time
taken by blocks to execute, and reports them at the end.
"""

import time
from pprint import pprint

from lb.graph import Graph

class TimingGraph(Graph):
    def __init__(self, *args, **kwargs):
        self._timing_by_block = {}
        super().__init__(*args, **kwargs)

    def before_graph_execution(self):
        pass

    def after_graph_execution(self):
        pprint(self._timing_by_block)

    def before_block_execution(self, blockname):
        self._timing_by_block[blockname] = {}
        self._timing_by_block[blockname]['begin'] = time.time()

    def after_block_execution(self, blockname):
        this_block_times = self._timing_by_block[blockname]
        this_block_times['end'] = time.time()
        this_block_times['duration'] = this_block_times['end'] - this_block_times['begin']
