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
Wrappers around `Apache Spark <http://spark.apache.org/>`_ API.  To
use this module, you need to install Spark and pyspark.
"""

import typing

import pyspark

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry, default_function

# Spark Context
# Initialised on demand to avoid losing time when this file is imported but not used.
SC = None

def get_spark_context(master, appname='lambdablocks'):
    """Creates a Spark context. Useful to have it in a function,
    otherwise within a module it will be created at import time, even
    if not used.

    Not a block; not for use in a graph.
    """
    global SC
    if SC is None:
        SC = pyspark.SparkContext(master, appname)
    return SC

### Standard Spark programming library

# Transformations

@block(engine='spark')
def spark_readfile(master: str='local[4]', appname: str='lambdablocks', filename: str=None):
    """Reads a file and returns an RDD ready to act on it.

    :param str master: Spark's master.
    :param str appname: Spark's application name.
    :param str filename: The file to be read.
    :output RDD result: The resulting RDD.
    """
    def inner() -> ReturnType[pyspark.rdd.RDD]:
        spark_context = get_spark_context(master, appname)
        o = spark_context.textFile(filename)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_text_to_words(lowercase: bool=False):
    """Converts a line of text into a list of words.

    :param bool lowercase: If the text should also be converted to lowercase.
    :input RDD line: The line to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(line: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        if lowercase:
            o = line.map(lambda x: x.lower())
        else:
            o = line

        for sep in [',', '.', '!', '?', ';', '"', "'"]:
            o = o.map((lambda sep: lambda x: x.replace(sep, ''))(sep))

        o = o.flatMap(lambda x: x.split())
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_map(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """Spark's map

    :param Callable func: The function to apply.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.map(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_filter(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """Spark's filter

    :param Callable func: The function to apply.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.filter(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_flatMap(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """Spark's flatMap

    :param Callable func: The function to apply.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.flatMap(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_mapPartitions(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """Spark's mapPartitions

    :param Callable func: The function to apply.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.mapPartitions(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_sample(withReplacement: bool=False, fraction: float=0.1, seed: int=1):
    """Spark's sample

    :param bool withReplacement: Default to false.
    :param float fraction: The quantity to sample.
    :param int seed: Seed.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.sample(withReplacement, fraction, seed)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_union():
    """Spark's union

    :input RDD data1: The first RDD.
    :input RDD data2: The second RDD.
    :output RDD result: The resulting RDD.
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.union(data2)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_intersection():
    """Spark's intersection

    :input RDD data1: The first RDD.
    :input RDD data2: The second RDD.
    :output RDD result: The resulting RDD.
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.intersection(data2)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_distinct(numTasks=None):
    """Spark's distinct

    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.distinct(numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_groupByKey(numTasks=None):
    """Spark's groupByKey

    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.groupByKey(numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_reduceByKey(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1),
                numTasks=None):
    """Spark's reduceByKey

    :param Callable func: The function to apply.
    :param numTasks: Number of tasks.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.reduceByKey(func, numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_aggregateByKey(zeroValue: typing.Any=None,
                   seqFunc: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1),
                   combFunc: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1),
                   numTasks=None):
    """Spark's aggregateByKey

    :param Any zeroValue:
    :param Callable seqFunc:
    :param Callable combFunc:
    :param numTasks:
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.aggregateByKey(zeroValue, seqFunc, combFunc, numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_sortByKey(ascending=True):
    """Spark's sortByKey

    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.sortByKey(ascending=ascending)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_join(numTasks=None):
    """Spark's join

    :input RDD data1: The first RDD.
    :input RDD data2: The second RDD.
    :output RDD result: The resulting RDD.
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.join(data2, numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_cogroup(numTasks=None):
    """Spark's cogroup

    :input RDD data1: The first RDD.
    :input RDD data2: The second RDD.
    :output RDD result: The resulting RDD.
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.cogroup(data2, numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_cartesian():
    """Spark's cartesian

    :input RDD data1: The first RDD.
    :input RDD data2: The second RDD.
    :output RDD result: The resulting RDD.
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.cartesian(data2)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_pipe(command: str=''):
    """
    Spark's pipe

    :param str command: The command to pipe to.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.pipe(command)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_coalesce(numPartitions: int=1):
    """Spark's coalesce

    :param int numPartitions:
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.coalesce(numPartitions)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_repartition(numPartitions: int=1):
    """Spark's repartition

    :param int numPartitions:
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.coalesce(numPartitions)
        return ReturnEntry(result=o)
    return inner

# Actions

@block(engine='spark')
def spark_reduce(func: typing.Callable[[pyspark.rdd.RDD, pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(2)):
    """
    Spark's reduce

    :param Callable func: The function to apply.
    :input RDD data: The RDD to convert.
    :output RDD result: The resulting RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.reduce(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_collect():
    """Spark's collect

    :input RDD data: The RDD to collect.
    :output list result: The collected list.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.collect()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_count():
    """Spark's count

    :input RDD data: The RDD to count.
    :output int result: The number of items in the RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[int]:
        o = data.count()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_first():
    """Spark's first

    :input RDD data: The RDD to convert.
    :output Any result: The first item of the RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[typing.Any]:
        o = data.first()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_take(n: int=0):
    """Spark's take

    :param int n: The number of items to take
    :input RDD data: The RDD to convert.
    :output Any result: The first *n* item of the RDD.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.take(n)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_takeSample(withReplacement: bool=False, num: int=0, seed: int=None):
    """Spark's takeSample

    :param bool withReplacement:
    :param int num:
    :param int seed:
    :input RDD data: The RDD to convert.
    :output list result: The resulting list.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.takeSample(withReplacement, num, seed)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_takeOrdered(num: int=0, key: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """Spark's takeOrdered

    :param int num:
    :param int key:
    :input RDD data: The RDD to convert.
    :output list result: The resulting list.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.takeOrdered(num, key=key)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_saveAsTextFile(path: str=''):
    """Spark's saveAsTextFile

    :param str path: The file path.
    :input RDD data: The RDD to save.
    """
    def inner(data: pyspark.rdd.RDD):
        data.saveAsTextFile(path)
    return inner

@block(engine='spark')
def spark_countByKey():
    """Spark's countByKey

    :input RDD data: The RDD to convert.
    :output Mapping(Any, int) result: The mapping of the elements to their number of occurences.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[typing.Mapping[typing.Any, int]]:
        o = data.countByKey()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_foreach(func: typing.Callable=default_function(1)):
    """Spark's foreach

    :param Callable func: The function to apply.
    :input RDD data: The RDD to convert.
    :output Any result: The result.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[typing.Any]:
        o = data.foreach(func)
        return ReturnEntry(result=o)
    return inner

### Helpers on top of Spark's library

@block(engine='spark')
def spark_add():
    """ReduceByKey with the addition function.

    :input RDD data: The RDD to convert.
    :output Any result: The result.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.reduceByKey(lambda a,b: a+b)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_swap():
    """Swaps pairs.

    ```[(a,b),(c,d)] -> [(b,a),(d,c)]```

    :input RDD data: The RDD to convert.
    :output Any result: The result.
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.map(lambda x: (x[1],x[0]))
        return ReturnEntry(result=o)
    return inner
