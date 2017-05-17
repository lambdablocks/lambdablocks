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
This modules provides facilities to build and run a topology graph out
of a YAML file.
"""

import inspect
import typing
import yaml

from collections import defaultdict, deque

import lb.types

def type_or_any(type_):
    """
    Returns the type if it is not inspect._empty (undeclared type),
    typing.Any otherwise.
    """
    if type_ == inspect._empty:
        return typing.Any
    return type_

class Graph(object):
    def __init__(self, filename, registry):
        """
        Initializes a DAG for execution, provided a YAML file
        containing it, and a blocks registry.
        """
        self.filename = filename
        self.registry = registry
        self._parse_file()
        self._check_yaml()
        self._build_dag()
        self._check_dag_types()
        self._check_dag_no_loops()

    def _parse_file(self):
        """
        Parses a YAML file defining a DAG.
        """
        with open(self.filename) as f:
            documents = list(yaml.safe_load_all(f))
            assert len(documents) == 2, \
                'YAML file must contain 2 documents: metadata, and DAG description.'
            self.dag_metadata = documents[0]
            self.blocks = documents[1]

    def _build_dag(self):
        """
        Builds a DAG from a list of blocks and their inputs.
        """
        vertices = {}
        entry_points = []
        for block in self.blocks:
            vertices[block['name']] = block
            # is it a DAG entry point?
            if 'inputs' not in block.keys() or block['inputs'] == []:
                entry_points.append(block['name'])
                # we still want to have an empty list to avoid KeyErrors
                block['inputs'] = []

        if len(entry_points) == 0:
            raise Exception(
                "Your topology doesn't have any entry point (a block "
                "without any input). Nothing to execute.")

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

                if block1 not in vertices.keys():
                    raise Exception('Block {} has an unknown input: {}'
                                    .format(block2, input_))

                edges[block1]['next'].append({'name': block2, 'value': value})
                edges[block2]['prev'].append({'name': block1, 'value': value})

        self.entry_points = entry_points
        self.vertices = vertices
        self.edges = edges

    def _check_yaml(self):
        """
        Checks that the YAML file is correctly typed.
        """
        block_names = []
        for block in self.blocks:
            # be sure every block has a name (unique) and is
            # associated to a registered block
            assert type(block) == dict, 'Block is malformed: ' + str(block)
            assert 'name' in block.keys(), "Block doesn't have a name: " + str(block)
            assert 'block' in block.keys(), "Block doesn't have a block: " + str(block)
            assert block['name'] not in block_names, 'Block name is duplicated: ' + block['name']
            block_names.append(block['name'])
            assert block['block'] in self.registry.keys(), "Block doesn't exist: " + block['block']
            # check arguments' types
            if 'args' in block.keys():
                for name, value in block['args'].items():
                    expected_type = self.registry[block['block']]['_parameters'][name].annotation
                    assert lb.types.is_instance(value, type_or_any(expected_type)), \
                      'Arg {} for block {} is of type {}, expected {}'.format(
                          name, block['name'], type(value), expected_type)

    def _check_dag_types(self):
        """
        Checks that every output has the same type as the inputs where
        it's consumed.
        """
        for block, props in self.vertices.items():
            # we collect the actual types this block receives
            received_types = []
            for input_ in props['inputs']:
                if '.' in input_: # multiple output
                    # the connected block producing this value:
                    producer_name = input_.split('.')[0]
                    producer_block = self.vertices[producer_name]['block']
                    # in case of multiple output, a dict is returned,
                    # and we want to know the type of the dict values
                    received_type = lb.types.type_of_mapping_values(
                        self.registry[producer_block]['_output'])

                else: # single output
                    # the connected block producing this value:
                    producer_block = self.vertices[input_]['block']
                    received_type = self.registry[producer_block]['_output']
                received_types.append(type_or_any(received_type))

            # we collect from the registry the list of expected types this
            # block is supposed to receive
            expected_types = []
            for expected_input in self.registry[props['block']]['_inputs'].values():
                if expected_input.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    # "normal" parameter
                    expected_types.append(type_or_any(expected_input.annotation))
                elif expected_input.kind == inspect.Parameter.VAR_POSITIONAL:
                    # "tuple" parameter, *args
                    # We fill all the remaining types with this one,
                    # considering the number of supplied parameters is correct
                    missing = len(received_types) - len(expected_types)
                    expected_types.extend([type_or_any(expected_input.annotation)] * missing)
                else:
                    # keyword parameter or something else, we ignore the rest
                    break

            # and we check that they are compatible
            assert lb.types.is_sig_compatible(
                tuple(received_types), tuple(expected_types)), \
                'Block {} has signature\n{}\nbut has inputs\n{}'.format(
                    block, expected_types, received_types)

    def _check_dag_no_loops(self):
        """
        Checks that the DAG doesn't contain loops.
        """
        for entry in self.entry_points:
            visited = []
            to_visit = deque([entry])
            while len(to_visit) > 0:
                current_block = to_visit.popleft()
                assert current_block not in visited, \
                    'There is a loop in your DAG, occuring with the block {}'.format(current_block)
                visited.append(current_block)
                for dest in self.edges[current_block]['next']:
                    to_visit.append(dest['name'])

    def execute(self):
        """
        Executes a DAG, beginning with all its entry points and giving
        their outputs to their consumers, iteratively.
        """
        results = {}
        final_results = {}
        fun_queue = deque(self.entry_points)

        while len(fun_queue) > 0:
            block_name = fun_queue.popleft()
            # do the block inputs have been computed yet?
            for input_ in self.edges[block_name]['prev']:
                if input_['name'] not in results.keys():
                    fun_queue.append(block_name)
                    break
            else: # ok, all inputs have been computed, we proceed
                comp_fun = self.registry[self.vertices[block_name]['block']]['_func']
                try:
                    comp_args = self.vertices[block_name]['args']
                except KeyError:
                    comp_args = {}

                # we prepare the block's input values
                comp_inputs = []
                for input_ in self.edges[block_name]['prev']:
                    if input_['value'] is None:
                        # no named value, single output from previous block
                        get_input = lambda results: results[input_['name']]
                    else:
                        get_input = lambda results: results[input_['name']][input_['value']]
                    try:
                        comp_inputs.append(get_input(results))
                    except KeyError as e:
                        raise Exception('%s was scheduled for execution, but lacks some inputs: %s'
                                        % (block_name, str(self.vertices[block_name]['inputs'])))
                results[block_name] = comp_fun(**comp_args)(*comp_inputs)

                # if this block has no destination, it is a final block, we store its result
                if not self.edges[block_name]['next']:
                    final_results[block_name] = results[block_name]

                # we add this block's destinations to the queue,
                # if they are not there already
                for destination in self.edges[block_name]['next']:
                    if destination['name'] not in fun_queue:
                        fun_queue.append(destination['name'])

        return final_results
