import yaml
import argparse

from DragonAggregator.connector.Gitleaks import GitleaksConnector
from DragonAggregator.db import Database


def get_parser():
    parser = argparse.ArgumentParser(description='DragonAggregator')
    parser.add_argument('--pull', action='store_true', help='Pull data from scanners')
    parser.add_argument('--export', action='store_true', help='Export data from scanners')
    parser.add_argument("--uri", type=str, help="URI to pull data from if applicable")
    parser.add_argument('--scanner', type=str, help='Scanner name', choices=['GITLEAKS', "VERACODE", "SONARQUBE"])
    parser.add_argument('--scan_type', type=str, help='Scan type', choices=['SECRETS', 'SAST', 'DAST', 'SCA'])
    parser.add_argument('--config', type=str, help='Config file', default='.dragonaggregator.yaml')
    parser.add_argument('--output', type=str, help='Output file')

    return parser


class CLIController:
    def __init__(self):
        self.parser = get_parser()
        self.args = self.parser.parse_args()

        self.config = CLIController.read_config(self.args.config)

        self.db = Database(self.config['db'])

    @staticmethod
    def read_config(path):
        with open(path) as f:
            return yaml.safe_load(f)

    def run(self):
        if self.args.pull:
            print("Pulling data from scanners")

            if self.args.scanner.upper() == "GITLEAKS":
                print("Pulling data from Gitleaks")

                gc = GitleaksConnector(self.args.uri)
                parsed = gc.pull_and_parse_data()
                self.db.save_all_vulnerabilities(parsed)

            else:
                print("Scanner {} not supported".format(self.args.scanner))
                exit(1)

        elif self.args.export:
            print("Exporting data from scanners")
        else:
            print("No action specified")
            self.parser.print_help()
