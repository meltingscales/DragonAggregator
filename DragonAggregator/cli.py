import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='DragonAggregator')
    parser.add_argument('command', help='Command to execute')
    return parser
