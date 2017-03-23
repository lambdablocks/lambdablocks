import pyspark

from lb.registry import block

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
    def inner(input_: pyspark.rdd.RDD) -> pyspark.rdd.RDD:
        o = input_.take(n)
        return o
    return inner
