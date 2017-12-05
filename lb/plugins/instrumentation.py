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
The instrumentation plugin measures the time taken by blocks to
execute, and reports them at the end.  This is useful to spot
bottlenecks, in order to optimize slow blocks.
"""

import time

from lb.plugins_manager import before_block_execution, \
     after_block_execution, \
     after_graph_execution

timing_by_block = {}

@before_block_execution
def store_begin_time(block, results):
    name = block.fields['name']
    timing_by_block[name] = {}
    timing_by_block[name]['begin'] = time.time()

@after_block_execution
def store_end_time(block, results):
    name = block.fields['name']
    timing_by_block[name]['end'] = time.time()
    timing_by_block[name]['duration'] = timing_by_block[name]['end'] - timing_by_block[name]['begin']

@after_graph_execution
def show_times(results):
    longest_first = sorted(timing_by_block.keys(),
                           key=lambda x: timing_by_block[x]['duration'],
                           reverse=True)
    print('######################################################')
    print('###             Instrumentation report             ###')
    print('######################################################')
    print('block\tduration (ms)\tbegin\tend')
    for blockname in longest_first:
        print('{}\t{}\t{}\t{}'.format(
            blockname,
            1000 * timing_by_block[blockname]['duration'],
            timing_by_block[blockname]['begin'],
            timing_by_block[blockname]['end']))
    print('######################################################')
    print('###                   End report                   ###')
    print('######################################################')
