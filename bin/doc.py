from lb.graph import get_block_functions

BOLD = '\033[1m'
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def format_boldred(msg):
    return BOLD + RED + msg + RESET

def format_red(msg):
    return RED + msg + RESET

def format_green(msg):
    return GREEN + msg + RESET

def doc_block(block_name, block_properties):
    print(format_boldred(block_name))
    for prop in block_properties.keys():
        if prop.startswith('_'):
            continue
        print('  ' + format_red(prop) + ': ' + block_properties[prop])

    for prop_name in ['parameters', 'inputs']:
        print(format_red('  {}:'.format(prop_name)))
        for item in block_properties['_' + prop_name].values():
            # import pdb; pdb.set_trace()
            print('    - '
                  + format_green(str(item.name))
                  + ' ('
                  + str(item.annotation.__name__)
                  + ')')
    if block_properties['_output']:
        print(format_red('  output') + ': ' + block_properties['_output'].__name__)
    print()

def main():
    blocks = get_block_functions()
    for (block_name, block_properties) in blocks.items():
        doc_block(block_name, block_properties)

if __name__ == '__main__':
    main()
