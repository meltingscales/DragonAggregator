import os
import unittest
from pathlib import Path

import yaml

from DragonAggregator.connector.Sonarqube import SonarQubeConnector

# get path
file_path = os.path.dirname(os.path.realpath(__file__))


class TestSonarqube(unittest.TestCase):

    def setUp(self):
        # if os.path.exists("test-gitleaks.sqlite3"):
        #     os.remove("test-gitleaks.sqlite3")

        config_path = Path(file_path).parent.parent / '.dragonaggregator.yaml'
        config_path = os.path.abspath(config_path)

        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def testSimple(self):
        sqc = SonarQubeConnector(
            uri=self.config['sonarqube']['url'],
            api_key=self.config['sonarqube']['api_key'],
            app_identifier='vulnado'
        )

        data = sqc.pull_raw_vulnerability_data()
        parsed = sqc.parse_vulnerability_data(data)

        self.assertEqual(parsed[0].git_commit_author, "ryan@scalesec.com")
