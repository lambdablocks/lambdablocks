import inspect
import pkgutil
import yaml

from collections import defaultdict, deque

import lb.blocks

def get_block_functions(external_modules=[]):
    # we list all local modules (lb/blocks/*)
    local_modules = []
    local_package = lb.blocks
    prefix = local_package.__name__ + "."
    for _, module, _ in pkgutil.iter_modules(local_package.__path__, prefix):
        local_modules.append(module)

    # we import all modules, so they get registered through the decorator
    for module in local_modules + external_modules:
        __import__(module)

    from lb.registry import all_blocks
    return all_blocks

def build_graph(blocks):
    vertices = {}
    entry_points = []
    for block in blocks:
        vertices[block['name']] = block
        if 'inputs' not in block.keys() or block['inputs'] == []:
            entry_points.append(block['name'])

    edges = defaultdict(list)
    for k,v in vertices.items():
        if 'inputs' in v.keys():
            for input_ in v['inputs']:
                edges[input_].append(k)

    return entry_points, vertices, edges

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
        comp_fun = block_functions[vertices[block_name]['block']]['func']
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
