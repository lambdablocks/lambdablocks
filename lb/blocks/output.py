import matplotlib.pyplot as plt
import pyspark

from pprint import pprint

from lb.registry import block

@block(inputs=['list'], outputs=[''])
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

@block(inputs=['list'], outputs=[''])
def plot_bars():
    def inner(input_):
        axis_y = [x[0] for x in input_]
        axis_x = range(len(axis_y))
        labels = [x[1] for x in input_]
        plt.xticks(axis_x, labels, rotation='vertical')
        plt.bar(left=range(len(axis_y)), height=axis_y)
        plt.show()
    return inner
