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

import pyspark
from pprint import pprint

from lb.registry import block

spark_context = pyspark.SparkContext('local', 'testing stuff')

### INPUT BLOCKS ###

@block(engine='spark')
def readfile(filename: str=None):
    def inner() -> pyspark.rdd.RDD:
        o = spark_context.textFile(filename)
        return o
    return inner

### MIDDLE BLOCKS ###

@block(engine='spark',
       description='Converts a line of text into a list of lower-case words.')
def text_to_words():
    def inner(line: pyspark.rdd.RDD) -> pyspark.rdd.RDD:
        o = line.map(lambda x: x.lower())

        for sep in [',', '.', '!', '?', ';', '"', "'"]:
            o = o.map((lambda sep: lambda x: x.replace(sep, ''))(sep))

        o = o.flatMap(lambda x: x.split())
        return o
    return inner

@block(engine='spark')
def map_with_one():
    def inner(input_: pyspark.rdd.RDD) -> pyspark.rdd.RDD:
        o = input_.map(lambda el: (el, 1))
        return o
    return inner

@block(engine='spark')
def add():
    def inner(input_: pyspark.rdd.RDD) -> pyspark.rdd.RDD:
        o = input_.reduceByKey(lambda a,b: a+b)
        return o
    return inner

@block(engine='spark')
def swap():
    def inner(input_: pyspark.rdd.RDD) -> pyspark.rdd.RDD:
        o = input_.map(lambda x: (x[1],x[0]))
        return o
    return inner

@block(engine='spark')
def sort():
    def inner(input_: pyspark.rdd.RDD) -> pyspark.rdd.RDD:
        o = input_.sortByKey(ascending=False)
        return o
    return inner

@block(engine='spark')
def first_n(n: int=0):
    def inner(input_: pyspark.rdd.RDD) -> list:
        o = input_.take(n)
        return o
    return inner

@block(engine='spark')
def union():
    def inner(first: pyspark.rdd.RDD, second: pyspark.rdd.RDD) -> pyspark.rdd.RDD:
        return first.union(second)
    return inner

@block(engine='spark')
def split(ratio=0.5):
    def inner(input_: pyspark.rdd.RDD) -> {'first': pyspark.rdd.RDD, 'second': pyspark.rdd.RDD}:
        first = input_.filter(lambda x: x[1][0] == 's') # todo
        second = input_.filter(lambda x: x[1][0] != 's')
        return {'first': first, 'second': second}
    return inner

### OUTPUT BLOCKS ###

@block(engine='spark')
def show_console():
    def inner(input_: list) -> None:
        o = input_
        print('\033[92m')
        pprint(o)
        print('\033[0m')
        return None
    return inner
