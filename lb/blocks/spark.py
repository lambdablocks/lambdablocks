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

from pprint import pprint
import pyspark

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry

### INPUT BLOCKS ###

@block(engine='spark')
def readfile(filename: str=None):
    def inner() -> ReturnType[pyspark.rdd.RDD]:
        spark_context = pyspark.SparkContext('local', 'lambdablocks')
        o = spark_context.textFile(filename)
        return ReturnEntry(result=o)
    return inner

### MIDDLE BLOCKS ###

@block(engine='spark',
       description='Converts a line of text into a list of lower-case words.')
def text_to_words():
    def inner(line: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = line.map(lambda x: x.lower())

        for sep in [',', '.', '!', '?', ';', '"', "'"]:
            o = o.map((lambda sep: lambda x: x.replace(sep, ''))(sep))

        o = o.flatMap(lambda x: x.split())
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def map_with_one():
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.map(lambda el: (el, 1))
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def add():
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.reduceByKey(lambda a,b: a+b)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def swap():
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.map(lambda x: (x[1],x[0]))
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def sort():
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.sortByKey(ascending=False)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def first_n(n: int=0):
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.take(n)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def union():
    def inner(first: pyspark.rdd.RDD, second: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        return ReturnEntry(result=first.union(second))
    return inner

@block(engine='spark')
def split(ratio: float=0.5):
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        first = data.filter(lambda x: x[1][0] == 's') # todo
        second = data.filter(lambda x: x[1][0] != 's')
        return ReturnEntry(first=first, second=second)
    return inner

### OUTPUT BLOCKS ###

@block(engine='spark')
def show_console():
    def inner(struct: list) -> None:
        o = struct
        print('\033[92m')
        pprint(o)
        print('\033[0m')
        return None
    return inner
