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
Debug plugin, prints an excerpt of each block's result after its
execution.
"""

import sys

from lb.plugins_manager import after_block_execution

def shorten(item, length=100):
    s = repr(item)
    length = min(length, len(s))
    result = s[:length]
    if length < len(s):
        result += '…'
    return result

@after_block_execution
def show_current_data(block, results):
    print('For block {}'.format(block.fields['name']))
    if results:
        for field, result in results._asdict().items():
            print('  {}'.format(field))
            sys.stdout.write('    ')
            if isinstance(result, list):
                if isinstance(result[0], list):
                    sys.stdout.write('[')
                    if isinstance(result[0][0], list):
                        sys.stdout.write("That's quite a nested list (FIXME)")
                    else:
                        sys.stdout.write('{}'.format(shorten(result[0][0:3])))
                    sys.stdout.write(']')
                else:
                    sys.stdout.write('{}'.format(shorten(result[0:3])))
            else:
                sys.stdout.write('{}'.format(shorten(result)))
            sys.stdout.write('\n\n')
    else:
        print('  No results for this block.')
