import pyspark

from lb.decorators import input_block

spark_context = pyspark.SparkContext('local', 'testing stuff')

@input_block
def readfile(filename=None):
    def inner(dummy):
        o = spark_context.textFile(filename)
        return o
    return inner
