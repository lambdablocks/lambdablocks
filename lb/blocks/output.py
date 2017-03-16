import pyspark

from pprint import pprint

from lb.decorators import output_block

@output_block
def show_console():
    def inner(input_):
        if type(input_) == pyspark.rdd.PipelinedRDD:
            o = input_.collect()
        else:
            o = input_
        print('\033[92m')
        pprint(o)
        print('\033[0m')
        return None
    return inner
