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

import matplotlib.pyplot as plt

from lb.registry import block

@block(engine='matplotlib')
def plot_bars():
    def inner(input_: list) -> None:
        axis_y = [x[0] for x in input_]
        axis_x = range(len(axis_y))
        labels = [x[1] for x in input_]
        plt.xticks(axis_x, labels, rotation='vertical')
        plt.bar(left=range(len(axis_y)), height=axis_y)
        plt.show()
    return inner
