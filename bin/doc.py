from lb.graph import get_block_functions

BOLD = '\033[1m'
RED = '\033[91m'
RESET = '\033[0m'

PROPERTIES = ['inputs', 'outputs']

def format_title(msg):
    return BOLD + RED + msg + RESET

def format_subtitle(msg):
    return RED + msg + RESET

def doc_block(block_name, block_properties):
    print(format_title(block_name))
    for prop in PROPERTIES:
        print('  ' + format_subtitle(prop) + ': ' + ', '.join(block_properties[prop]))
    print()

def main():
    blocks = get_block_functions()
    for (block_name, block_properties) in blocks.items():
        doc_block(block_name, block_properties)

if __name__ == '__main__':
    main()
