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
Signature is an algorithm which permits to uniquely identify a
particular block (instance) in a particular graph.

For that purpose, we hash the block name, the block parameters, and
the signatures of the block inputs (recursively).  This is similar to
a Merkle tree, in that a change in one of the block predecessors will
raise a different block signature.

Let H the signature algorithm, and h a cryptographically secure hash
function.

B is a block, whose inputs are:
  - right: bar.result
  - left: foo.result
and args are:
  - abc: 123
  - cba: ['x', 'y']

H(block) = h([
  block.blockname,                 <--- the *block* name, not the *instance* name
  [
    ('abc', 123),                  <--+ ordered by arg name
    ('cba', ['x', 'y'])            <--|
  ],
  [
    ('left', H(foo), 'result'),    <--+ ordered by input name
    ('right', H(bar), 'result')    <--|
  ]
])
"""

import hashlib

signatures = {} # we keep the signatures cached
                # keys are block instance names, unique in a graph
                # might break if many DAGs are executed in the same python process

def sign(block):
    """
    Returns a unique signature for a block instance within a graph,
    and keeps it cached to speed-up the recursive aspect.
    """
    instance_name = block.fields['name']

    # is it cached?
    if instance_name in signatures.keys():
        return signatures[instance_name]

    name = block.fields['block']

    args = []
    for arg in sorted(block.fields['args'].keys()):
        args.append((arg, block.fields['args'][arg]))

    inputs = []
    for input_ in sorted(block.prev_vertices, key=lambda x: x.value_dest):
        # input_ is a Connector
        inputs.append((input_.value_dest,
                       sign(input_.block_from),
                       input_.value_from))

    r = [name, args, inputs]
    s = hashlib.sha256(repr(r).encode('utf8')).hexdigest()

    # we cache it
    signatures[instance_name] = s

    return s
