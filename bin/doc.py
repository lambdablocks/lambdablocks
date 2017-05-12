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

from lb.registry import Registry

BOLD = '\033[1m'
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def format_boldred(msg):
    return BOLD + RED + msg + RESET

def format_red(msg):
    return RED + msg + RESET

def format_green(msg):
    return GREEN + msg + RESET

def doc_block(block_name, block_properties):
    print(format_boldred(block_name))
    for prop in block_properties.keys():
        if prop.startswith('_'):
            continue
        print('  ' + format_red(prop) + ': ' + block_properties[prop])

    for prop_name in ['parameters', 'inputs']:
        print(format_red('  {}:'.format(prop_name)))
        for item in block_properties['_' + prop_name].values():
            # import pdb; pdb.set_trace()
            print('    - '
                  + format_green(str(item.name))
                  + ' ('
                  + str(item.annotation.__name__)
                  + ')')
    output = block_properties['_output']
    if output:
        print(format_red('  output') + ': ')
        if type(output) == dict: # multi output
            for (name, type_) in output.items():
                print('    - '
                      + format_green(str(name))
                      + ' ('
                      + str(type_.__name__)
                      + ')')
        else: # single output
            print('    ' + str(output.__name__))
    print()

def main():
    registry = Registry()

    for (block_name, block_properties) in registry.items():
        doc_block(block_name, block_properties)

if __name__ == '__main__':
    main()
