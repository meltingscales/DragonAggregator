from typing import List, Dict

from DragonAggregator.models import GenericVulnerability


class GenericConnector:
    def __init__(self, *args, **kwargs):
        self.uri = kwargs.get('uri')
        self.file_based = kwargs.get('file_based')
        self.api_key = kwargs.get('api_key')

    def pull_raw_vulnerability_data(self) -> List[Dict]:
        # Pull vulnerabilities from the generic API
        return []

    def parse_vulnerability_data(self, raw_data: List[Dict]) -> List[GenericVulnerability]:
        return []

    def pull_and_parse_data(self) -> List[GenericVulnerability]:
        raw_data = self.pull_raw_vulnerability_data()
        return self.parse_vulnerability_data(raw_data)
