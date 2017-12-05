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
Provides a cache through disk.

.. WARNING:: This is not safe from attacks.  As it uses the `pickle`
   module, it could be led to unpickle unsafe data, if an attacker got an
   access to the filesystem.  Use at your own risk.

.. NOTE:: This cache is functional, but will prevent blocks with
   side-effects to compute.  Keep that in mind.
"""

import os
import pickle
import tempfile

from lb.cache import CacheProvider
from lb.plugins_manager import before_block_execution, \
     after_block_execution, \
     after_graph_execution
from lb.signature import sign

# initiates the folder containing the cache, in a temporary location
TMPPATH = os.path.join(tempfile.gettempdir(), 'lb-cache')
if not os.path.exists(TMPPATH):
    os.mkdir(TMPPATH)

class DiskCacheProvider(CacheProvider):
    def set(self, key, value):
        with open(os.path.join(TMPPATH, key), 'wb') as f:
            pickle.dump(value, f, pickle.HIGHEST_PROTOCOL)

    def get(self, key):
        path = os.path.join(TMPPATH, key)
        if not os.path.exists(path):
            raise KeyError('The key {} is not cached.'.format(key))
        with open(path, 'rb') as f:
            value = pickle.load(f)
            return value

this_cache = DiskCacheProvider()

@before_block_execution
def skip_exec_if_cached(block, results):
    s = sign(block)
    try:
        value = this_cache.get(s)
        results[block] = value
    except KeyError:
        pass

@after_block_execution
def store_in_cache(block, results):
    s = sign(block)
    this_cache.set(s, results[block])
