import pyspark

from lb.registry import block

spark_context = pyspark.SparkContext('local', 'testing stuff')

@block(engine='spark')
def readfile(filename: str=None):
    def inner(dummy) -> pyspark.rdd.RDD:
        o = spark_context.textFile(filename)
        return o
    return inner
