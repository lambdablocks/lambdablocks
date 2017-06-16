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
Defines some exceptions used throughout the framework.
"""

class NotBoundError(Exception):
    """
    When a subtopology value is accessed, but has not been defined
    (bound).
    """

class YAMLError(Exception):
    """
    An error in a user-defined YAML topology.
    """

class ExecutionError(Exception):
    """
    Error thrown while executing a topology.
    """

class BlockError(Exception):
    """
    Error in a block definition.
    """
