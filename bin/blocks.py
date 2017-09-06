#!/usr/bin/env python3

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

import argparse
import glob
import os

from lb.graph import Graph
from lb.registry import Registry

def parse_args():
    parser = argparse.ArgumentParser(
        description='Runs a yaml-defined DAG.')
    parser.add_argument('-f', '--filename',
                        required=True,
                        help='YAML file to be executed.')
    parser.add_argument('-m', '--modules',
                        required=False,
                        nargs='*',
                        default=[],
                        help='Additional Python modules containing blocks.')
    parser.add_argument('--no-internal-modules',
                        required=False,
                        action='store_false',
                        help='Do not load lambda-blocks predefined modules.')
    parser.add_argument('-p', '--plugins',
                        required=False,
                        nargs='+',
                        help='List of plugins to activate. Available plugins: {}'.format(
                            ','.join(available_plugins())))
    args = parser.parse_args()
    return args

def available_plugins():
    """
    List plugins available from lb/plugins/
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'lb',
                        'plugins')
    plugins = glob.glob('{}/*.py'.format(path))
    return [os.path.basename(x).split('.')[0] for x in plugins]

def import_plugins(plugins):
    """
    Imports the activated plugins, which will register their hooks.
    """
    if plugins is not None:
        for plugin in plugins:
            try:
                __import__('lb.plugins.{}'.format(plugin))
            except ImportError as e:
                print('Plugin {} could not be found. Is it in the folder `lb/plugins/`?'.format(plugin))
                raise e

def main():
    args = parse_args()

    registry = Registry(external_modules=args.modules,
                       load_internal_modules=args.no_internal_modules)

    import_plugins(args.plugins)

    g = Graph(filename=args.filename, registry=registry)
    g.execute()

if __name__ == '__main__':
    main()
