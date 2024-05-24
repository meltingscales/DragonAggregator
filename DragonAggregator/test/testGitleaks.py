import unittest

from DragonAggregator.connector.Gitleaks import GitleaksConnector


class MyTestCase(unittest.TestCase):
    def test_something(self):
        filepath = "../../data/sample-api/gitleaks/juiceshop.json"

        gc = (GitleaksConnector(filepath))

        data = gc.pull_raw_vulnerability_data()

        vulns = GitleaksConnector.parse_secrets_vulnerability_data(data)

        print(vulns)

        self.assertEqual(vulns[0].finding_id,
                         "4e1b04d8043428b71cab5ad020c18b3db42b4361:test/api/web3Spec.ts:generic-api-key:36")
