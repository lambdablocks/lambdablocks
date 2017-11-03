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

from collections import deque

import collections
import inspect
import os.path
import typing
import yaml

import lb.types
from lb.exceptions import NotBoundError, YAMLError, ExecutionError
from lb.log import get_logger
from lb.plugins_manager import HOOKS

logger = get_logger(__name__)

def type_or_any(type_):
    """
    Returns the type if it is not inspect._empty (undeclared type),
    typing.Any otherwise.
    """
    if type_ == inspect._empty:
        return typing.Any
    return type_

class _Section(object):
    """
    Container for a section of the YAML file, containing its fields.
    """
    def __init__(self, fields):
        self.fields = fields

class Vertice(_Section):
    """
    Container for a vertice, a block as defined in YAML.  Also holds
    its directed edges with other blocks.
    """
    def __init__(self, fields):
        super().__init__(fields)

        if 'inputs' not in self.fields.keys():
            self.fields['inputs'] = {}
        if 'args' not in self.fields.keys():
            self.fields['args'] = {}

        self.prev_vertices = []
        self.next_vertices = []

    def add_prev(self, connector):
        self.prev_vertices.append(connector)

    def add_next(self, connector):
        self.next_vertices.append(connector)

class Topology(_Section):
    """
    Container for a topology, as defined in YAML.  Mainly used to
    encapsulate a Graph.
    """
    def __init__(self, fields, registry):
        super().__init__(fields)

        if 'bind_in' not in self.fields.keys():
            self.fields['bind_in'] = {}
        if 'bind_out' not in self.fields.keys():
            self.fields['bind_out'] = {}

        # we create the subgraph
        self.graph = Graph(filename=self.fields['topology'], registry=registry, skip_check=True)

    def get_outbound(self, value):
        """
        Given a bind_out value, returns the associated block along
        with its wanted result.
        """
        if value not in self.fields['bind_out']:
            raise NotBoundError('The value {} is not bound for topology {}.'.format(
                value, self.fields['name']))
        producer, value = self.fields['bind_out'][value].split('.')
        producer = self.graph.vertices[producer]

        return producer, value

    def vertices(self):
        """
        Returns the vertices of the encapsulated graph.
        """
        return self.graph.vertices

    def topology_inputs(self):
        """
        Returns the topology_inputs ($inputs.*) of the encapsulated graph.
        """
        return self.graph.topology_inputs

class Connector(object):
    """
    Represents a connection in a block.

    A connection links an output block and one of its return value (a
    field name of the returned dict) with an input block and one of
    its input value (a parameter name).
    """
    def __init__(self, block_from, value_from, block_dest, value_dest):
        self.block_from = block_from
        self.value_from = value_from
        self.block_dest = block_dest
        self.value_dest = value_dest

    def __repr__(self):
        return '{}.{} -> {}.{}'.format(
            self.block_from.fields['name'], self.value_from, self.block_dest.fields['name'], self.value_dest)


class Graph(object):
    """
    Builds, stores, checks and executes a DAG from a YAML topology
    file.
    """
    def __init__(self, filename=None, filecontent=None, registry=None, skip_check=False):
        """
        Initializes a DAG for execution, provided a YAML file
        containing it, and a blocks registry.

        skip_check allows to skip the checks: it is usually not
        recommended, but can come handy when e.g. working with
        subgraphs and avoiding to check partial graphs.
        """
        assert filename is None or filecontent is None, \
          'Either filename or filecontent must be provided, not both.'

        assert filename is not None or filecontent is not None, \
          'You must provide at least a filename or filecontent when initializing a graph.'

        self.filename = filename
        self.filecontent = filecontent
        self.registry = registry
        logger.debug('Parsing YAML data')
        self._parse_file()
        logger.debug('Checking YAML data')
        self._check_yaml()
        logger.debug('Building grah')
        self._build_dag()
        if not skip_check:
            logger.debug('Checking graph edges and types')
            self._check_dag_inputs()
            logger.debug('Checking graph has no loops')
            self._check_dag_no_loops()

    def _parse_file(self):
        """
        Parses a YAML file defining a DAG.
        """
        def parse(content):
            # Make YAML parser use OrderedDict instead of dict, to
            # keep e.g. the order of inputs correct
            _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
            def dict_constructor(loader, node):
                return collections.OrderedDict(loader.construct_pairs(node))
            yaml.add_constructor(_mapping_tag, dict_constructor)

            documents = list(yaml.load_all(content))
            assert len(documents) == 2, \
                'YAML file must contain 2 documents: metadata, and DAG description.'
            self.dag_metadata = documents[0]
            assert documents[1] != None, \
                "The topology doesn't define any block."

            # every argument beginning with 'lambda' is considered a
            # function and transformed as such
            for section in documents[1]:
                # happens at least when a file contains only "foo: bar":
                assert type(section) is not str, \
                  'Malformed section: {}'.format(section)
                for key, value in section.get('args', {}).items():
                    if isinstance(value, str):
                        if value.startswith('lambda'):
                            section['args'][key] = eval(value)

            self.dag_as_yaml = documents[1]

        if self.filename is not None:
            with open(self.filename) as f:
                parse(f)
        else:
            parse(self.filecontent)

    def _build_dag(self):
        """
        Creates the DAG associated to the YAML file, recursively
        merging the subgraphs it encounters.
        """
        def create_edge(block_from, value_from, block_dest, value_dest):
            c = Connector(block_from, value_from, block_dest, value_dest)
            block_from.add_next(c)
            block_dest.add_prev(c)

        # assuming all names are unique, even in subgraphs, because
        # the primary key is a block name at the moment

        vertices = {}        # holds the vertices of the graph
        subgraphs = {}       # holds the subgraphs
        topology_inputs = [] # holds the graph global inputs ($inputs)
        entry_points = []    # DAG entry points, i.e. vertices without any input

        # we create all the vertices and subgraphs
        for section in self.dag_as_yaml:
            assert 'topology' in section.keys() or 'block' in section.keys(), \
              'Malformed section, must be a block or a topology:\n{}' \
                .format(section)
            if 'topology' in section.keys(): # composition with a sub-topology
                subgraphs[section['name']] = Topology(section, self.registry)
            elif 'block' in section.keys(): # normal block
                vertices[section['name']] = Vertice(section)

        # we create the edges
        for block_dest in vertices.values():
            if len(block_dest.fields['inputs'].items()) == 0:
                entry_points.append(block_dest)
                continue
            for value_dest, pair in block_dest.fields['inputs'].items():
                try:
                    block_from, value_from = pair.split('.')
                except ValueError:
                    raise YAMLError(
                        'An input must contain a block/topology name and a value, '
                        'such as my_block.foo. Got {} in block {}'.format(pair, block_dest.fields['name']))
                if block_from == '$inputs':
                    # topology input
                    topology_inputs.append({'block_dest': block_dest,
                                            'value_dest': value_dest,
                                            'value_from': value_from})
                else:
                    if block_from not in vertices.keys() and block_from not in subgraphs.keys():
                        raise YAMLError('Block {} has an unknown input: {}={} (no block {})'
                                        .format(block_dest.fields['name'], value_dest, pair, block_from))

                    if block_from in subgraphs.keys():
                        # result of a subgraph
                        block_from, value_from = subgraphs[block_from].get_outbound(value_from)
                    else:
                        block_from = vertices[block_from]

                    create_edge(block_from, value_from, block_dest, value_dest)

        # we now merge all the subgraphs
        for subgraph in subgraphs.values():
            for ti in subgraph.topology_inputs():
                block_from, value_from = subgraph.fields['bind_in'][ti['value_from']].split('.')
                block_from = vertices[block_from]
                create_edge(block_from, value_from, ti['block_dest'], ti['value_dest'])
            vertices.update(subgraph.vertices())

        # we're done
        self.topology_inputs = topology_inputs
        self.vertices = vertices
        self.entry_points = entry_points

    def show_dag(self):
        for v in self.vertices.values():
            print(v.fields['name'])
            print(' from:')
            for prev in v.prev_vertices:
                print('  {} -> {}'.format(prev.block_from.fields['name'], prev.value_from))
            print(' to:')
            for to in v.next_vertices:
                print('  {} -> {}'.format(to.block_dest.fields['name'], to.value_dest))
            print('____________________')

    def _check_yaml(self):
        """
        Checks that the YAML file is correctly typed.
        """
        def assert_dict(section, key):
            if key in section.keys():
                assert isinstance(section[key], dict), \
                  "Block {}'s {} is not a dict".format(section['name'], key)

        section_names = []
        for section in self.dag_as_yaml:
            # be sure every block has a name (unique) and is
            # associated to a registered block
            assert isinstance(section, dict), \
              'Section is malformed: {}'.format(str(section))
            assert 'name' in section.keys(), \
              "Section doesn't have a name: {}".format(str(section))
            assert section['name'] not in section_names, \
              'Section name is duplicated: {}'.format(section['name'])
            section_names.append(section['name'])

            assert 'block' in section.keys() or 'topology' in section.keys(), \
              'Section is not a block nor a topology: {}'.format(section)
            if 'block' in section.keys(): # regular block
                assert section['block'] in self.registry.keys(), \
                    "Block doesn't exist: {}".format(section['block'])
                assert_dict(section, 'inputs')

            else: # topology
                assert os.path.isfile(section['topology']), \
                  "Topology file doesn't exist: {}".format(section['topology'])
                assert_dict(section, 'bind_in')
                assert_dict(section, 'bind_out')

            # check arguments types
            if 'args' in section.keys():
                for name, value in section['args'].items():
                    expected_type = self.registry[section['block']]['_parameters'][name].annotation
                    assert lb.types.is_instance(value, type_or_any(expected_type)), \
                      'Arg {} for block {} is of type {}, expected {}'.format(
                          name, section['name'], type(value), expected_type)

    def _check_dag_inputs(self):
        """
        Checks that every output has the same name and type as the
        inputs where it's consumed.
        """
        for block in self.vertices.values():
            block_name = block.fields['block']

            # we collect the actual var names and types this block receives
            received_names = []
            received_types = []
            for input_ in block.prev_vertices:
                # the connected block producing this value:
                # we want to know the type of the dict values
                try:
                    received_type = lb.types.type_of_mapping_values(
                        self.registry[input_.block_from.fields['block']]['_output'])
                except AssertionError as e:
                    print("Warning: {} doesn't seem to return a ReturnEntry of type ReturnType." \
                          .format(input_.block_from.fields['name']))
                    raise e
                received_names.append(input_.value_dest)
                received_types.append(type_or_any(received_type))

            # we collect from the registry the list of expected names
            # and types this block is supposed to receive
            expected_names = []
            expected_types = []
            for expected_input in self.registry[block_name]['_inputs'].values():
                if expected_input.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    # "normal" parameter
                    expected_names.append(expected_input.name)
                    expected_types.append(type_or_any(expected_input.annotation))
                elif expected_input.kind == inspect.Parameter.VAR_KEYWORD:
                    # "tuple" parameter, *args
                    # We fill all the remaining types with this one,
                    # considering the number of supplied parameters is correct
                    missing = len(received_types) - len(expected_types)
                    expected_names.extend([None] * missing) # no names
                    expected_types.extend([type_or_any(expected_input.annotation)] * missing)
                else:
                    # keyword parameter or something else, we ignore the rest
                    break

            # we check that the types are compatible
            assert lb.types.is_sig_compatible(
                tuple(received_types), tuple(expected_types)), \
                'Block {} has signature\n{}\nbut has inputs\n{}'.format(
                    block.fields['block'], expected_types, received_types)

            # we check that the names are the same
            # precondition: the tables have the same len()
            for x, y in zip(received_names, expected_names):
                assert x == y or y is None, \
                  'Wrong input name "{}" for block {}, expected "{}"'.format(x, block.fields['name'], y)

    def _check_dag_no_loops(self):
        """
        Checks that the DAG doesn't contain loops.
        """
        def loop_in_path(path):
            names = [x.fields['name'] for x in path]
            assert len(set(names)) == len(names),\
                'There is a loop in your DAG, occuring with the block {}' \
                .format(names[-1])

        self.loop_vertices(loop_in_path)

    def loop_vertices(self, fun, depth=False):
        """
        Implements a breadth-first search on the DAG, and applies
        function `fun` to every vertice.

        `fun` must accept one argument, a list of vertices
        representing the path taken.  The last element of this list is
        the current vertice.

        If `depth` is True, do a depth-first search instead.
        """
        # initial paths are [[entrypoint1],[entrypoint2],…]
        queue_to_visit = deque([[x] for x in self.entry_points])
        while len(queue_to_visit) > 0:
            current_path = queue_to_visit.popleft()
            current_vertice = current_path[-1]
            fun(current_path)
            # add linked vertices to the queue
            for dest in current_vertice.next_vertices:
                if depth:
                    queue_to_visit.appendleft(current_path + [dest.block_dest])
                else:
                    queue_to_visit.append(current_path + [dest.block_dest])

    def execute(self):
        """
        Executes a DAG, beginning with all its entry points and giving
        their outputs to their consumers, iteratively.
        """
        self.before_graph_execution()

        results = {}
        fun_queue = deque(self.entry_points)

        while len(fun_queue) > 0:
            block = fun_queue.popleft()
            # do the block inputs have been computed yet?
            for input_ in block.prev_vertices:
                if input_.block_from not in results.keys():
                    fun_queue.append(block) # TODO: beware of endless loops loops loop loops…
                    break
            else: # ok, all inputs have been computed, we proceed
                comp_fun = self.registry[block.fields['block']]['_func']
                comp_args = block.fields['args']

                # we prepare the block's input values
                comp_inputs = {}
                for input_ in block.prev_vertices:
                    try:
                        this_res = getattr(results[input_.block_from], input_.value_from)
                    except AttributeError:
                        raise ExecutionError('{} was scheduled for execution, but lacks some inputs: {}'
                                        .format(block.fields['name'], input_.value_from))

                    comp_inputs[input_.value_dest] = this_res

                self.before_block_execution(block)
                results[block] = comp_fun(**comp_args)(**comp_inputs)
                self.after_block_execution(block, results[block])

                # we add this block's destinations to the queue,
                # if they are not there already
                for destination in block.next_vertices:
                    if destination.block_dest not in fun_queue:
                        fun_queue.append(destination.block_dest)

        self.after_graph_execution(results)

        return results

    def before_graph_execution(self):
        print(self.entry_points)
        for f in HOOKS['before_graph_execution']:
            f(self.vertices, self.entry_points)

    def after_graph_execution(self, results):
        for f in HOOKS['after_graph_execution']:
            f(results)

    def before_block_execution(self, block):
        for f in HOOKS['before_block_execution']:
            f(block)

    def after_block_execution(self, block, results):
        for f in HOOKS['after_block_execution']:
            f(block, results)
