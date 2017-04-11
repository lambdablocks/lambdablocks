import matplotlib.pyplot as plt

from lb.registry import block

@block(engine='matplotlib')
def plot_bars():
    def inner(input_: list) -> None:
        axis_y = [x[0] for x in input_]
        axis_x = range(len(axis_y))
        labels = [x[1] for x in input_]
        plt.xticks(axis_x, labels, rotation='vertical')
        plt.bar(left=range(len(axis_y)), height=axis_y)
        plt.show()
    return inner
