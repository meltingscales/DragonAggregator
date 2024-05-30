import json
from datetime import datetime
from typing import List, Dict

from DragonAggregator.connector.Generic import GenericConnector
from veracode_api_py import Applications, Scans, Findings

from DragonAggregator.enum.ScanTool import ScanTool
from DragonAggregator.enum.ScanType import ScanType
from DragonAggregator.models import GenericVulnerability, SastVulnerability


def scan_type_to_veracode_scan_type(s: str) -> str:
    if s == "SAST":
        return "STATIC"
    else:
        raise NotImplementedError("Scan type not supported yet " + s)


class VeracodeConnector(GenericConnector):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "file_based": False
        })

        super().__init__(*args, **kwargs)

        self.app_identifier = kwargs.get('app_identifier')
        self.scan_type = kwargs.get('scan_type')
        self.mock_api = kwargs.get('mock_api')
        self.mock_api_json_path = kwargs.get('mock_api_json_path')

    def pull_raw_vulnerability_data(self):

        if self.mock_api:
            with open(self.mock_api_json_path, 'r') as fh:
                return json.load(fh)

        else:
            app = Applications().get_by_name(self.app_identifier)
            guid = app.get('guid')

            vscan_type = scan_type_to_veracode_scan_type(self.scan_type)

            findings = Findings().get_findings(app=guid, scantype=vscan_type)

            return findings

    def parse_vulnerability_data(self, raw_data: List[Dict]) -> List[GenericVulnerability]:
        vulns = []

        for datum in raw_data:
            scan_type = datum.get('scan_type')

            if scan_type == 'STATIC':

                parsed_date = datum['finding_status']['first_found_date']
                parsed_date = datetime.strptime(parsed_date, '%Y-%m-%dT%H:%M:%S%z')

                parsed_vuln = SastVulnerability(
                    id=None,
                    original_data=datum,
                    scan_date=parsed_date,
                    processed_date=datetime.now(),
                    finding_id=datum['issue_id'],
                    title=datum['finding_details']['cwe']['name'],
                    description=datum['description'],
                    severity=datum['finding_details']['severity'],
                    scan_tool=ScanTool.VERACODE.value,
                    scan_type=ScanType.SAST.value,
                    file_path=datum['finding_details']['file_path'],
                    line=datum['finding_details']['file_line_number'],
                )

                vulns.append(parsed_vuln)

            else:
                raise NotImplementedError("Scan type not supported yet " + scan_type)

        return vulns
