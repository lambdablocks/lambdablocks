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

"""
This modules provides facilities to build and run a topology graph out
of a YAML file.
"""

import yaml

from collections import defaultdict, deque

from lb.registry import Registry

def build_graph(blocks):
    vertices = {}
    entry_points = []
    for block in blocks:
        vertices[block['name']] = block
        if 'inputs' not in block.keys() or block['inputs'] == []:
            entry_points.append(block['name'])
            # we still want to have an empty list to avoid KeyErrors
            block['inputs'] = []

    edges = defaultdict(lambda: {'prev': [],
                                 'next': []})

    for block2, block2_props in vertices.items():
        for input_ in block2_props['inputs']:
            # we add the vertice between block1 and block2, in both directions
            if '.' in input_:
                # named output, when a block outputs multiple values
                try:
                    block1, value = input_.split('.')
                except ValueError as e:
                    print('Wrong input: ' + input_)
                    raise e
            else:
                # the block outputs a single value
                block1, value = input_, None

            edges[block1]['next'].append({'name': block2, 'value': value})
            edges[block2]['prev'].append({'name': block1, 'value': value})

    return entry_points, vertices, edges

def parse_yaml(filename):
    with open(filename) as f:
        blocks = yaml.load(f)
    return blocks

def execute(registry, inputs, vertices, edges):
    results = {}
    fun_queue = deque(inputs)

    while len(fun_queue) > 0:
        block_name = fun_queue.popleft()
        # do the block inputs have been computed yet?
        for input_ in edges[block_name]['prev']:
            if input_['name'] not in results.keys():
                fun_queue.append(block_name)
                break
        else: # ok, all inputs have been computed, we proceed
            comp_fun = registry[vertices[block_name]['block']]['_func']
            try:
                comp_args = vertices[block_name]['args']
            except KeyError:
                comp_args = {}

            # we prepare the block's input values
            comp_inputs = []
            for input_ in edges[block_name]['prev']:
                if input_['value'] is None:
                    # no named value, single output from previous block
                    get_input = lambda results: results[input_['name']]
                else:
                    get_input = lambda results: results[input_['name']][input_['value']]
                try:
                    comp_inputs.append(get_input(results))
                except KeyError as e:
                    raise Exception('%s was scheduled for execution, but lacks some inputs: %s'
                                    % (block_name, str(vertices[block_name]['inputs'])))
            results[block_name] = comp_fun(**comp_args)(*comp_inputs)
            # we add this block's destinations to the queue,
            # if they are not there already
            for destination in edges[block_name]['next']:
                if destination['name'] not in fun_queue:
                    fun_queue.append(destination['name'])

def compute_graph(filename):
    registry = Registry()
    blocks = parse_yaml(filename)
    inputs, vertices, edges = build_graph(blocks)
    execute(registry, inputs, vertices, edges)
