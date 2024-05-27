from typing import List, Dict

from DragonAggregator.models import GenericVulnerability


class GenericConnector:
    def __init__(self, uri, file_based=False, api_key=None):
        self.uri = uri
        self.file_based = file_based
        self.api_key = None

    def pull_raw_vulnerability_data(self) -> List[Dict]:
        # Pull vulnerabilities from the generic API
        return []

    @staticmethod
    def parse_vulnerability_data(raw_data: List[Dict]) -> List[GenericVulnerability]:
        return []

    def pull_and_parse_data(self) -> List[GenericVulnerability]:
        raw_data = self.pull_raw_vulnerability_data()
        return self.parse_vulnerability_data(raw_data)
