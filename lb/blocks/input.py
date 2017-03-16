from lb.decorators import input_block

@input_block
def readfile(spark_context=None, filename=None):
    def inner(dummy):
        o = spark_context.textFile(filename)
        return o
    return inner
