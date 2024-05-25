import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='DragonAggregator')
    parser.add_argument('--pull', action='store_true', help='Pull data from scanners')
    parser.add_argument('--export', action='store_true', help='Export data from scanners')
    parser.add_argument('--scanner', type=str, help='Scanner name', choices=['GITLEAKS', "VERACODE", "SONARQUBE"])
    parser.add_argument('--scan_type', type=str, help='Scan type', choices=['SECRETS', 'SAST', 'DAST', 'SCA'])
    parser.add_argument('--config', type=str, help='Config file', default='.dragonaggregator.yaml')
    parser.add_argument('--output', type=str, help='Output file')

    return parser
