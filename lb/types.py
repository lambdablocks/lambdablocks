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
Types manipulation.  This module defines functions to check for types
compatibility.
"""

from typing import Any, Mapping, Tuple, TupleMeta, TypeVar

T = TypeVar('T')
ReturnType = Mapping[str, T]

def is_subtype(left, right):
    """
    Checks if left is a subtype of right, i.e. if they are compatible.
    Currently implemented: basic types, Tuple
    """
    if left is Any or right is Any:
        # Any is compatible with everything, on both sides
        return True

    if isinstance(left, TupleMeta) and isinstance(right, TupleMeta):
        # in case of tuples on both sides, we check their items
        if hasattr(left, '__tuple_params__'): # Python 3.5.2
            tuple_params = '__tuple_params__'
        else: # Python 3.5.3, 3.6
            tuple_params = '__args__'
        left_items = getattr(left, tuple_params)
        right_items = getattr(right, tuple_params)

        if len(left_items) != len(right_items):
            return False
        return all([is_subtype(left_item, right_item)
                    for (left_item, right_item)
                    in zip(left_items, right_items)])

    if isinstance(left, TupleMeta) != isinstance(right, TupleMeta):
        # tuple only on one side, not compatible
        return False

    # either a base type, or something else not supported
    return issubclass(left, right)

def is_sig_compatible(left, right):
    """
    Checks if signature left is compatible with signature right, i.e.
    if the types in signature left can be fed to a function accepting
    the types in signature right.

    left and right are tuples of types (`tuple` as in Python built-in,
    not as in typing.Tuple)
    """
    def to_tuple_type(tup): # sadly we can't do Tuple[*tup]
        if len(tup) > 5:
            raise Exception(
                "Due to Python's limitation regarding typing, it is currently "
                "not possible to have more than 5 inputs for a single block.")
        if len(tup) == 0:
            return type(None) # NoneType
        elif len(tup) == 1:
            return Tuple[tup[0]]
        elif len(tup) == 2:
            return Tuple[tup[0], tup[1]]
        elif len(tup) == 3:
            return Tuple[tup[0], tup[1], tup[2]]
        elif len(tup) == 4:
            return Tuple[tup[0], tup[1], tup[2], tup[3]]
        elif len(tup) == 5:
            return Tuple[tup[0], tup[1], tup[2], tup[3], tup[4]]

    return is_subtype(to_tuple_type(left), to_tuple_type(right))

def is_instance(var, type_):
    """
    Checks if the type of a variable is compatible with another type.

    Currently it is only a wrapper around built-in isinstance, but we
    might add different type-checking later, e.g. with the types
    returned by the yaml parser.
    """
    if hasattr(type_, '__origin__') and type_.__origin__ is not None:
        # this is to avoid "TypeError: Parameterized generics cannot
        # be used with class or instance checks", so we we don't
        # currently check the parameterized types
        type_ = type_.__origin__
    return isinstance(var, type_)

def type_of_mapping_values(type_):
    """
    Given a Mapping type, returns the type of its values.
    """
    assert is_subtype(type_, Mapping), \
      'Not a Mapping subtype: {}'.format(type_)
    return type_.__args__[0]
