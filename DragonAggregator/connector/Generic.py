from typing import List, Dict

from DragonAggregator.models import GenericVulnerability, SecretsVulnerability, SastVulnerability, DastVulnerability, \
    ScaVulnerability


class GenericConnector:
    def __init__(self, uri, file_based=False):
        self.uri = uri
        self.file_based = file_based

    def pull_raw_vulnerability_data(self) -> List[Dict]:
        # Pull vulnerabilities from the generic API
        return []

    @classmethod
    def parse_secrets_vulnerability_data(self, raw_data: List[Dict]) -> List[SecretsVulnerability]:
        return []

    @classmethod
    def parse_sast_vulnerability_data(self, raw_data: List[Dict]) -> List[SastVulnerability]:
        return []

    @classmethod
    def parse_dast_vulnerability_data(self, raw_data: List[Dict]) -> List[DastVulnerability]:
        return []

    @classmethod
    def parse_sca_vulnerability_data(self, raw_data: List[Dict]) -> List[ScaVulnerability]:
        return []
