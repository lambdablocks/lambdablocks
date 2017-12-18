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
import logging

from lb.graph import Graph
from lb.log import get_logger
from lb.plugins_manager import available_plugins, import_plugins
from lb.registry import Registry

def parse_args():
    parser = argparse.ArgumentParser(
        description='Runs a yaml-defined DAG.')
    parser.add_argument('-f', '--filename',
                        required=True,
                        help='YAML file to be executed.')
    parser.add_argument('-p', '--plugins',
                        required=False,
                        nargs='+',
                        help='List of plugins to activate. Plugins in the '
                        'standard library are lb.plugins.{{{}}}'.format(
                            ','.join(available_plugins())))
    parser.add_argument('-v', '--verbose',
                        required=False,
                        action='count',
                        default=0,
                        help='Verbose run, use up to 4 times to get more logging.')
    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    # -v for ERROR, -vv for WARNING, -VVV for INFO, -vvvv for DEBUG
    logging.disable((4 - args.verbose) * 10)

    logger = get_logger('blocks.py')

    logger.debug('Starting lambda-blocks')
    logger.debug('Creating registry')
    registry = Registry()

    logger.debug('Importing configured plugins')
    import_plugins(args.plugins)

    logger.debug('Creating and checking graph')
    g = Graph(filename=args.filename, registry=registry)
    logger.debug('Executing graph')
    g.execute()
    logger.debug('Done, exiting')

if __name__ == '__main__':
    main()
