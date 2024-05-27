from typing import List, Dict

from sqlalchemy.orm import Session

from DragonAggregator.models import GenericVulnerability, SecretsVulnerability, SastVulnerability, DastVulnerability, \
    ScaVulnerability


class GenericConnector:
    def __init__(self, uri, file_based=False):
        self.uri = uri
        self.file_based = file_based

    def pull_raw_vulnerability_data(self) -> List[Dict]:
        # Pull vulnerabilities from the generic API
        return []

    @staticmethod
    def parse_vulnerability_data(raw_data: List[Dict]) -> List[GenericVulnerability]:
        return []

    def pull_and_parse_data(self) -> List[GenericVulnerability]:
        raw_data = self.pull_raw_vulnerability_data()
        return self.parse_vulnerability_data(raw_data)
