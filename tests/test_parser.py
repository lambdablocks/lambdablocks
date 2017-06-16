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
from lb.registry import Registry

import textwrap
import unittest

class TestParser(unittest.TestCase):
    def setUp(self):
        self.registry = Registry(load_internal_modules=True)

    def tearDown(self):
        pass

    def test_one_yaml_section(self):
        content = textwrap.dedent("""
        ---
        name: foo
        """)
        with self.assertRaisesRegex(AssertionError, 'must contain 2 documents'):
            g = Graph(filecontent = content, registry=self.registry)

    def test_empty_yaml(self):
        content = textwrap.dedent("""
        ---
        ---
        """)
        with self.assertRaisesRegex(AssertionError, "topology doesn't define any block"):
            g = Graph(filecontent = content, registry=self.registry)

    def test_malformed_section(self):
        content = textwrap.dedent("""
        ---
        ---
        foo: bar
        """)
        with self.assertRaisesRegex(AssertionError, 'malformed: foo'):
            g = Graph(filecontent = content, registry=self.registry)

    def test_unnamed_section(self):
        content = textwrap.dedent("""
        ---
        ---
        - block: foo
        """)
        with self.assertRaisesRegex(AssertionError, "doesn't have a name"):
            g = Graph(filecontent = content, registry=self.registry)

    def test_not_topology_or_block(self):
        content = textwrap.dedent("""
        ---
        ---
        - name: foo
          whatami: even
        """)
        with self.assertRaisesRegex(AssertionError, 'not a block nor a topology'):
            g = Graph(filecontent = content, registry=self.registry)

