import sys
from DragonAggregator.cli import get_parser

if __name__ == '__main__':
    parser = get_parser()

    # if we don't have any arguments, print help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
