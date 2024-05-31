import json
from typing import Dict, List

from DragonAggregator.connector.Generic import GenericConnector
from sonarqube import SonarQubeClient

from DragonAggregator.enum.ScanTool import ScanTool
from DragonAggregator.enum.ScanType import ScanType
from DragonAggregator.models import GenericVulnerability


class SonarQubeConnector(GenericConnector):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "file_based": False
        })

        super().__init__(*args, **kwargs)

        self.app_identifier = kwargs.get('app_identifier')
        self.mock_api = kwargs.get('mock_api')
        self.mock_api_json_path = kwargs.get('mock_api_json_path')

        self.sonar_client = SonarQubeClient(self.uri, token=self.api_key)

    def pull_raw_vulnerability_data(self) -> Dict:

        if self.mock_api:
            print("SonarQube: Using mock API data")
            with open(self.mock_api_json_path) as f:
                return json.load(f)

        issues = self.sonar_client.issues.search_issues(componentKeys=self.app_identifier)

        return issues

    def parse_vulnerability_data(self, raw_data: Dict) -> List[GenericVulnerability]:
        vulns = raw_data['issues']
        parsed = []

        for vuln in vulns:
            parsed_vuln = GenericVulnerability(
                finding_id=vuln['key'],
                application_ref=vuln['project'],
                title=vuln['message'],
                description=vuln['component'],
                severity=vuln['severity'],
                scan_tool=ScanTool.SONARQUBE.value,
                scan_type=ScanType.SAST.value,
                file_path=vuln['component'],
                line=vuln['line'],
                git_commit_author=vuln['author'],
                git_commit_email=vuln['author'],
                original_data=vuln,

            )

            parsed.append(parsed_vuln)

        return parsed
