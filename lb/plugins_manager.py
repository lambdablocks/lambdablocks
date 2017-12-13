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

import glob
import os

from lb.log import get_logger
logger = get_logger(__name__)

here = os.path.abspath(os.path.dirname(__file__))

# global variable (singleton) containing the registered hooks
# happening at different execution times
HOOKS = {
    'before_block_execution': [],
    'after_block_execution': [],
    'before_graph_execution': [],
    'after_graph_execution': [],
    }

def available_plugins():
    """List plugins available from lb/plugins/.
    """
    path = os.path.join(here, 'plugins')
    plugins = glob.glob('{}/*.py'.format(path))
    return [os.path.basename(x).split('.')[0] for x in plugins]

def import_plugins(plugins):
    """Imports the activated plugins, which will trigger their hooks
    registration.
    """
    if plugins is not None:
        for plugin in plugins:
            try:
                __import__(plugin)
            except ImportError as e:
                logger.error('Plugin {} could not be found. Is it in the '
                             'Python path?'.format(plugin))
                raise e

def _register_hook(f, hookname):
    logger.debug('Registering function {} from {} to hook {}'.format(
        f.__name__, f.__module__, hookname))
    HOOKS[hookname].append(f)

def before_block_execution(f):
    _register_hook(f, 'before_block_execution')

def after_block_execution(f):
    _register_hook(f, 'after_block_execution')

def before_graph_execution(f):
    _register_hook(f, 'before_graph_execution')

def after_graph_execution(f):
    _register_hook(f, 'after_graph_execution')
