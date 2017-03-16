import yaml
import pyspark

from pprint import pprint

from lb.blocks.input import *
from lb.blocks.middle import *
from lb.blocks.output import *

sc = pyspark.SparkContext('local', 'testing stuff')

# foo = None
# for fun in [readfile(spark_context=sc, filename='examples/longtext'),
#             text_to_words(),
#             map_with_one(),
#             add(),
#             swap(),
#             sort(),
#             first_n(5),
#             show_console()]:
#     foo = fun(foo)

def build_graph(data):
    vertices = {}
    for block in data:
        vertices[block['name']] = block

    edges = {}
    for k,v in vertices.items():
        if 'inputs' in v.keys():
            edges[k] = []
            for input_ in v['inputs']:
                edges[k].append(input_)

    return vertices, edges

def main():
    with open('examples/foo.yml') as f:
        content = yaml.load(f)

    # pprint(content)
    vertices, edges = build_graph(content)
    pprint(vertices)
    pprint(edges)


if __name__ == '__main__':
    main()