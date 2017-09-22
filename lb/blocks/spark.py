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

import typing

import pyspark

from lb.registry import block
from lb.types import ReturnType
from lb.utils import ReturnEntry, default_function

def get_spark_context():
    """
    Creates a Spark context.  Useful to have it in a function,
    otherwise within a module it will be created at import time, even
    if not used.
    """
    return pyspark.SparkContext('local', 'lambdablocks')

### Standard Spark programming library

# Transformations

@block(engine='spark')
def spark_readfile(filename: str=None):
    """
    Reads a file and returns an RDD ready to act on it.
    """
    def inner() -> ReturnType[pyspark.rdd.RDD]:
        spark_context = get_spark_context()
        o = spark_context.textFile(filename)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_text_to_words(lowercase: bool=False):
    """
    Converts a line of text into a list of words.
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
    """
    Spark's map
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.map(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_filter(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """
    Spark's filter
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.filter(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_flatMap(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """
    Spark's flatMap
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.flatMap(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_mapPartitions(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """
    Spark's mapPartitions
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.mapPartitions(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_sample(withReplacement: bool=False, fraction: float=0.1, seed: int=1):
    """
    Spark's sample
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.sample(withReplacement, fraction, seed)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_union():
    """
    Spark's union
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.union(data2)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_intersection():
    """
    Spark's intersection
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.intersection(data2)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_distinct(numTasks=None):
    """
    Spark's distinct
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.distinct(numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_groupByKey(numTasks=None):
    """
    Spark's groupByKey
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.groupByKey(numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_reduceByKey(func: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1),
                numTasks=None):
    """
    Spark's reduceByKey
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
    """
    Spark's aggregateByKey
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.aggregateByKey(zeroValue, seqFunc, combFunc, numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_sortByKey(ascending=True):
    """
    Spark's sortByKey
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.sortByKey(ascending=ascending)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_join(numTasks=None):
    """
    Spark's join
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.join(data2, numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_cogroup(numTasks=None):
    """
    Spark's cogroup
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.cogroup(data2, numTasks)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_cartesian():
    """
    Spark's cartesian
    """
    def inner(data1: pyspark.rdd.RDD, data2: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data1.cartesian(data2)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_pipe(command: str=''):
    """
    Spark's pipe
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.pipe(command)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_coalesce(numPartitions: int=1):
    """
    Spark's coalesce
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.coalesce(numPartitions)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_repartition(numPartitions: int=1):
    """
    Spark's repartition
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
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.reduce(func)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_collect():
    """
    Spark's collect
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.collect()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_count():
    """
    Spark's count
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[int]:
        o = data.count()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_first():
    """
    Spark's first
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[typing.Any]:
        o = data.first()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_take(n: int=0):
    """
    Spark's take
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.take(n)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_takeSample(withReplacement: bool=False, num: int=0, seed: int=None):
    """
    Spark's takeSample
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.takeSample(withReplacement, num, seed)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_takeOrdered(num: int=0, key: typing.Callable[[pyspark.rdd.RDD], pyspark.rdd.RDD]=default_function(1)):
    """
    Spark's takeOrdered
    """
    def inner(data: pyspark.rdd.RDD) -> ReturnType[list]:
        o = data.takeOrdered(num, key=key)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_saveAsTextFile(path: str=''):
    """
    Spark's saveAsTextFile
    """
    def inner(data: pyspark.rdd.RDD):
        data.saveAsTextFile(path)
    return inner

@block(engine='spark')
def spark_countByKey():
    """
    Spark's countByKey
    """
    def inner(data: pyspark.rdd.RDD) -> typing.Mapping[typing.Any, int]:
        o = data.countByKey()
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_foreach(func: typing.Callable=default_function(1)):
    """
    Spark's foreach
    """
    def inner(data: pyspark.rdd.RDD) -> typing.Any:
        o = data.foreach(func)
        return ReturnEntry(result=o)
    return inner

### Helpers on top of Spark's library

@block(engine='spark')
def spark_add():
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.reduceByKey(lambda a,b: a+b)
        return ReturnEntry(result=o)
    return inner

@block(engine='spark')
def spark_swap():
    def inner(data: pyspark.rdd.RDD) -> ReturnType[pyspark.rdd.RDD]:
        o = data.map(lambda x: (x[1],x[0]))
        return ReturnEntry(result=o)
    return inner
