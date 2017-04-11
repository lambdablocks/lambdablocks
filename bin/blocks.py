# Copyright 2017 Matthieu Caneill
# Copyright 2017 Univ. Grenoble Alpes
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

def parse_args():
    parser = argparse.ArgumentParser(
        description='Runs a yaml-defined DAG.')
    parser.add_argument('-f', '--filename',
                        required=True,
                        help='YAML file to be executed.')
    parser.add_argument('-m', '--modules',
                        required=False,
                        nargs='*',
                        help='Additional Python modules containing blocks.')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # imported here to avoid creating a Spark context when not needed
    from lb.graph import compute_graph

    compute_graph(args.filename)

if __name__ == '__main__':
    main()
