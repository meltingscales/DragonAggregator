import os.path
import unittest

from sqlalchemy import select

from DragonAggregator.connector.Gitleaks import GitleaksConnector
from DragonAggregator.db import Database
from DragonAggregator.models import GenericVulnerability, SecretsVulnerability


class TestGitLeaks(unittest.TestCase):

    def setUp(self):
        if os.path.exists("test-gitleaks.sqlite3"):
            os.remove("test-gitleaks.sqlite3")

    def test_parse_gitleaks(self):
        filepath = "../../data/sample-api/gitleaks/juiceshop.json"

        gc = GitleaksConnector(filepath)

        data = gc.pull_raw_vulnerability_data()

        vulns = GitleaksConnector.parse_vulnerability_data(data)

        print(vulns)

        self.assertEqual(vulns[0].finding_id,
                         "4e1b04d8043428b71cab5ad020c18b3db42b4361:test/api/web3Spec.ts:generic-api-key:36")

        self.assertIn("Generic API Key", vulns[0].title, )

        db = Database("sqlite:///test-gitleaks.sqlite3")

        for vuln in vulns:
            db.session.add(vuln)

        db.session.commit()

        result = db.session.query(SecretsVulnerability).filter(
            SecretsVulnerability.finding_id == vulns[0].finding_id).all()

        print(result)

        db.session.close()
