from typing import Dict, List

from DragonAggregator.connector.Generic import GenericConnector
from sonarqube import SonarQubeClient

from DragonAggregator.models import GenericVulnerability


class SonarQubeConnector(GenericConnector):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "file_based": False
        })

        super().__init__(*args, **kwargs)

        self.project_key = kwargs.get('project_key')
        self.sonar_client = SonarQubeClient(self.uri, token=self.api_key)

    def pull_raw_vulnerability_data(self) -> Dict:
        issues = self.sonar_client.issues.search_issues(componentKeys=self.project_key)

        return issues

    @classmethod
    def parse_vulnerability_data(cls, raw_data: Dict) -> List[GenericVulnerability]:
        vulns = raw_data['issues']
        parsed = []

        for vuln in vulns:
            parsed_vuln = GenericVulnerability(
                finding_id=vuln['key'],
                application_ref=vuln['project'],
                title=vuln['message'],
                description=vuln['component'],
                severity=vuln['severity'],
                scan_tool='SONARQUBE',
                scan_type='STATIC',
                file_path=vuln['component'],
                line=vuln['line'],
                git_commit_author=vuln['author'],
                git_commit_email=vuln['author'],

            )

            parsed.append(parsed_vuln)

        return parsed
