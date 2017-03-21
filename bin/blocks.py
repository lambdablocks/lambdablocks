import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Runs a yaml-defined DAG.')
    parser.add_argument('-f', '--filename',
                        required=True,
                        help='YAML file to be executed.')
    parser.add_argument('-m', '--modules',
                        required=False,
                        nargs='*',
                        help='Additional Python modules containing blocks.')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # imported here to avoid creating a Spark context when not needed
    from lb.graph import compute_graph

    compute_graph(args.filename)

if __name__ == '__main__':
    main()
