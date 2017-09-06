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
This module makes tests about the YAML parser/graph builder.

If you're reading this, cheers!  You're either curious or you're
adding tests to lambda blocks.  That's great.  Here's a joke for your
trouble: "There are two difficult problems in computer science: cache
invalidation, naming things, and off-by-one errors."
"""

from lb.exceptions import YAMLError
from lb.graph import Graph
from lb.registry import Registry

import textwrap
import unittest

class TestParser(unittest.TestCase):
    def setUp(self):
        self.registry = Registry(load_internal_modules=False, external_modules=['tests.blocks'])

    def tearDown(self):
        pass

    def test_one_yaml_section(self):
        content = textwrap.dedent("""
        ---
        name: foo
        """)
        with self.assertRaisesRegex(AssertionError, 'must contain 2 documents'):
            g = Graph(filecontent=content, registry=self.registry)

    def test_empty_yaml(self):
        content = textwrap.dedent("""
        ---
        ---
        """)
        with self.assertRaisesRegex(AssertionError, "topology doesn't define any block"):
            g = Graph(filecontent=content, registry=self.registry)

    def test_malformed_section(self):
        content = textwrap.dedent("""
        ---
        ---
        foo: bar
        """)
        with self.assertRaisesRegex(AssertionError, 'Malformed section: foo'):
            g = Graph(filecontent=content, registry=self.registry)

    def test_unnamed_section(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: foo
        """)
        with self.assertRaisesRegex(AssertionError, "doesn't have a name"):
            g = Graph(filecontent=content, registry=self.registry)

    def test_not_topology_or_block(self):
        content = textwrap.dedent("""
        ---
        ---
        - name: foo
          whatami: even
        """)
        with self.assertRaisesRegex(AssertionError, 'not a block nor a topology'):
            g = Graph(filecontent=content, registry=self.registry)

    def test_unexisting_block(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: to_be_or_not_to_be
          name: foo
        """)
        with self.assertRaisesRegex(AssertionError, "doesn't exist"):
            g = Graph(filecontent=content, registry=self.registry)

    def test_unknown_input(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: sometimes_reverse
          name: sometimes_reverse
          inputs:
            data: foo.bar
        """)
        with self.assertRaisesRegex(YAMLError, 'unknown input: data=foo.bar'):
            g = Graph(filecontent=content, registry=self.registry)

    def test_correct_graph(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: input
          name: input
        - block: sometimes_reverse
          name: sometimes_reverse
          args:
            reverse: true
          inputs:
            data: input.result
        - block: output_screen
          name: output_screen
          inputs:
            data: sometimes_reverse.result
        """)
        g = Graph(filecontent=content, registry=self.registry)
        assert g.topology_inputs == []
        assert len(g.vertices) == 3
        assert len(g.entry_points) == 1
        assert len(g.vertices['sometimes_reverse'].prev_vertices) == 1
        assert g.vertices['sometimes_reverse'].prev_vertices[0].block_from == g.vertices['input']
        assert len(g.vertices['sometimes_reverse'].next_vertices) == 1
        assert g.vertices['sometimes_reverse'].next_vertices[0].block_dest == g.vertices['output_screen']

    def test_dag_loop(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: input
          name: input
        - block: merge_lists
          name: merge_lists
          inputs:
            data1: input.result
            data2: sometimes_reverse.result
        - block: sometimes_reverse
          name: sometimes_reverse
          inputs:
            data: merge_lists.result
        """)
        with self.assertRaisesRegex(AssertionError, 'There is a loop'):
            g = Graph(filecontent=content, registry=self.registry)

    def test_dag_wrong_types(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: input_str
          name: input_str
        - block: sometimes_reverse
          name: sometimes_reverse
          inputs:
            data: input_str.result
        """)
        with self.assertRaisesRegex(AssertionError, 'Block sometimes_reverse has signature'):
            g = Graph(filecontent=content, registry=self.registry)

    def test_trivial_execution(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: input
          name: input
        - block: sometimes_reverse
          name: sometimes_reverse
          args:
            reverse: true
          inputs:
            data: input.result
        """)
        g = Graph(filecontent=content, registry=self.registry)
        results = g.execute()
        sr_results = results[g.vertices['sometimes_reverse']]
        assert getattr(sr_results, 'result') == [3,2,1]

# todo, missing: test embedded topologies
