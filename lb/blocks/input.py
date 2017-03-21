import pyspark

from lb.registry import block

spark_context = pyspark.SparkContext('local', 'testing stuff')

@block(inputs=[], outputs=['spark_rdd'])
def readfile(filename=None):
    def inner(dummy):
        o = spark_context.textFile(filename)
        return o
    return inner
