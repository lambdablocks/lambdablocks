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
This module manages the blocks registry.  It provides a decorator for
blocks to register themselves, and a Registry class to manage
registered blocks.
"""

import importlib
import inspect
import pkgutil

import lb.blocks
from lb.exceptions import BlockError, UnfoundModuleError

def block(**kwargs):
    """
    Decorator to define a block, so it can get added to the registry.
    Use it as follows:
    @block(engine='foo', description='bar', my_other_metadata='foobar')
    def my_block()...
    """
    def block_decorator(func):
        func._metadata = kwargs
        func._is_block = True
        return func
    return block_decorator

class Registry(object):
    """
    A registry contains a list of registered blocks, along with their
    inferred properties, such as their parameters, metadata, inputs
    and output.
    """
    def __init__(self, external_modules=[], load_internal_modules=True):
        """
        Loads Python modules containing blocks and registers them.
        """
        self.blocks = {}

        if load_internal_modules:
            # we list all local modules (lb/blocks/*)
            internal_modules = []
            local_package = lb.blocks
            prefix = local_package.__name__ + "."
            for _, module, _ in pkgutil.iter_modules(local_package.__path__, prefix):
                internal_modules.append(module)
        else:
            internal_modules = []
        for module in internal_modules + external_modules:
            try:
                mod = importlib.import_module(module)
            except ImportError:
                raise UnfoundModuleError('The module {} has not been found or could not be imported.'.format(module))
            for _, func in mod.__dict__.items():
                if hasattr(func, '_is_block') and func._is_block:
                    self._register_block(func)

    def _register_block(self, func):
        """
        Registers a Python function as a block.  It must follow block
        requirements.
        """
        name = func.__name__
        # gets the function factory parameters
        if callable(func):
            sig_outer = inspect.signature(func)
        else:
            raise BlockError('Malformed block: {}'.format(name))
        # gets the inner function  parameters
        inner = func()
        if callable(inner):
            sig_inner = inspect.signature(inner)
        else:
            raise BlockError('Malformed block: {}'.format(name))
        # registers the block
        if name in self.blocks.keys():
            raise BlockError('The registry saw a duplicated block name: {}. '
                'It means a block has been defined twice, or the same name '
                'has been used to define two blocks.'.format(name))
        else:
            self.blocks[name] = {
                '_func':   func,
                '_parameters': sig_outer.parameters,
                '_inputs': sig_inner.parameters,
                '_output': sig_inner.return_annotation,
                '_metadata': func._metadata,
                }

    def __getitem__(self, block_name):
        """
        Returns the registered block block_name.
        """
        return self.blocks[block_name]

    def items(self):
        """
        Iterates through the registered blocks.
        Throw a list of tuples (block_name, block_properties).
        """
        return self.blocks.items()

    def keys(self):
        """
        Returns the list of registered block names.
        """
        return self.blocks.keys()
