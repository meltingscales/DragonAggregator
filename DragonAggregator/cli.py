import json

import yaml
import argparse

from DragonAggregator.connector.Gitleaks import GitleaksConnector
from DragonAggregator.connector.Sonarqube import SonarQubeConnector
from DragonAggregator.db import Database
from DragonAggregator.models import GenericVulnerability, SastVulnerability, DastVulnerability, SecretsVulnerability, \
    ScaVulnerability


def get_parser():
    parser = argparse.ArgumentParser(description='DragonAggregator')
    parser.add_argument('--pull', action='store_true', help='Pull data from scanners')
    parser.add_argument('--export', action='store_true', help='Export data from scanners')
    parser.add_argument("--uri", type=str, help="URI to pull data from if applicable")
    parser.add_argument('--scanner', type=str, help='Scanner name',
                        choices=['GITLEAKS', "VERACODE", "SONARQUBE", 'all'])
    parser.add_argument('--scan_type', type=str, help='Scan type', choices=['SECRETS', 'SAST', 'DAST', 'SCA', 'all'])
    parser.add_argument('--project_key', type=str, help='Project key for scanning tool')
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

    def pull_data(self):
        print(f"Pulling data from {self.args.scanner}")

        if self.args.scanner.upper() == "GITLEAKS":
            connector = GitleaksConnector(self.args.uri)
            parsed = connector.pull_and_parse_data()
            self.db.save_all_vulnerabilities(parsed)

        elif self.args.scanner.upper() == "SONARQUBE":
            connector = SonarQubeConnector(
                uri=self.args.uri,
                api_key=self.config['sonarqube']['api_key'],
                project_key=self.args.project_key
            )
            parsed = connector.pull_and_parse_data()
            self.db.save_all_vulnerabilities(parsed)

        else:
            print("Scanner {} not supported".format(self.args.scanner))
            exit(1)

    def export_data(self):
        print("Exporting data from scanners into " + self.args.output + "...")

        # vulns = self.db.session.query(SastVulnerability, DastVulnerability, SecretsVulnerability, ScaVulnerability)
        vulns = self.db.session.query(GenericVulnerability)

        if self.args.scanner.upper() == 'ALL':
            pass
        else:
            vulns = vulns.filter(GenericVulnerability.scan_tool == self.args.scanner)

        if self.args.scan_type.upper() == 'ALL':
            pass
        else:
            vulns = vulns.filter(GenericVulnerability.scan_type == self.args.scan_type)

        vulns = vulns.all()
        json_vulns = []

        for vuln in vulns:
            vuln: GenericVulnerability
            json_vulns.append(vuln.to_json())

        with open(self.args.output, 'w') as f:
            json.dump(json_vulns, f)

        print("Wrote {} records to {}".format(len(json_vulns), self.args.output))

    def run(self):
        if self.args.pull:
            self.pull_data()

        elif self.args.export:
            self.export_data()
        else:
            print("No action specified")
            self.parser.print_help()
