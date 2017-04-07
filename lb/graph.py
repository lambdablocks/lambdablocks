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
            # we still want to have an empty list to avoid KeyErrors
            block['inputs'] = []

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
        # do the block inputs have been computed yet?
        for input_ in vertices[block_name]['inputs']:
            if input_ not in results.keys():
                fun_queue.append(block_name)
                break
        else: # ok, all inputs have been computed, we proceed
            comp_fun = block_functions[vertices[block_name]['block']]['_func']
            try:
                comp_args = vertices[block_name]['args']
            except KeyError:
                comp_args = {}
            try:
                comp_inputs = [results[x] for x in vertices[block_name]['inputs']]
            except KeyError as e:
                raise Exception('%s was scheduled for execution, but lacks some inputs: %s'
                                % (block_name, str(vertices[block_name]['inputs'])))
            results[block_name] = comp_fun(**comp_args)(*comp_inputs)
            # we add this block's destinations to the queue,
            # if they are not there already
            for destination in edges[block_name]:
                if destination not in fun_queue:
                    fun_queue.append(destination)

def compute_graph(filename):
    blocks = parse_yaml(filename)
    inputs, vertices, edges = build_graph(blocks)
    execute(inputs, vertices, edges)
