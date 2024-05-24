import json
from typing import Dict, List

from DragonAggregator.connector.Generic import GenericConnector
from DragonAggregator.models import SecretsVulnerability


class GitleaksConnector(GenericConnector):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "file_based": True
        })

        super().__init__(*args, **kwargs)

    def pull_raw_vulnerability_data(self) -> List[Dict]:
        # Pull vulnerabilities from a gitleaks file

        # open json file
        with open(self.uri) as f:
            data = json.load(f)

        return data

    @classmethod
    def parse_secrets_vulnerability_data(cls, raw_data: List[Dict]) -> List[SecretsVulnerability]:
        parsed = []

        for raw_datum in raw_data:
            single_vuln = SecretsVulnerability(
                id=None,
                finding_id=raw_datum['Fingerprint'],
                title="todo",
                description=raw_datum['Description'],
                secret_type=raw_datum['RuleID'],
                secret_value=raw_datum['Secret'],
                file_path=raw_datum['File'],
                scan_tool='GITLEAKS',
                git_commit=raw_datum['Commit'],
                git_commit_author=raw_datum['Author'],
                git_commit_email=raw_datum['Email'],
                git_commit_date=raw_datum['Date'],
                severity='HIGH',  # Gitleaks does not provide severity, we can assume it is high
            )

            parsed.append(single_vuln)

        return parsed
