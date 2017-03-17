import inspect
import yaml

from collections import defaultdict, deque

import lb.blocks.input
import lb.blocks.middle
import lb.blocks.output

def get_block_functions():
    block_functions = {}
    for name, module in [('input', lb.blocks.input),
                         ('middle', lb.blocks.middle),
                         ('output', lb.blocks.output)]:
        block_functions[name] = {}
        functions = inspect.getmembers(module, inspect.isfunction)
        for function in functions:
            block_functions[name][function[0]] = function[1]
    return block_functions

def build_graph(blocks):
    vertices = {}
    inputs = []
    for block in blocks:
        vertices[block['name']] = block
        if block['type'] == 'input':
            inputs.append(block['name'])

    edges = defaultdict(list)
    for k,v in vertices.items():
        if 'inputs' in v.keys():
            for input_ in v['inputs']:
                edges[input_].append(k)

    return inputs, vertices, edges

def parse_yaml(filename):
    with open(filename) as f:
        blocks = yaml.load(f)
    return blocks

def execute(inputs, vertices, edges):
    results = {}
    block_functions = get_block_functions()
    fun_queue = deque(inputs)

    while len(fun_queue) > 0:
        block_name = fun_queue.popleft()
        # we compute this block
        comp_fun = block_functions[vertices[block_name]['type']][vertices[block_name]['block']]
        try:
            comp_args = vertices[block_name]['args']
        except KeyError:
            comp_args = {}
        try:
            comp_inputs = [results[x] for x in vertices[block_name]['inputs']]
        except KeyError:
            comp_inputs = [None]
        results[block_name] = comp_fun(**comp_args)(*comp_inputs)
        # we add this block's destinations to the queue
        fun_queue.extend(edges[block_name])

def compute_graph(filename):
    blocks = parse_yaml(filename)
    inputs, vertices, edges = build_graph(blocks)
    execute(inputs, vertices, edges)
