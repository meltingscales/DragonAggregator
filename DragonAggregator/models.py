



@dataclass
class User:
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenericVulnerability:
    id: int
    software_application_ref: str
    scanner: str
    scan_type: str

@dataclass
class SastVulnerability(GenericVulnerability):
    id: int
    software_application_id: int
    scanner: str
    severity: str
    cwe: str
    description: str
    file_path: str
    line_number: int
    created_at: datetime
    updated_at: datetime

class DastVulnerability:
    id: int
    software_application_id: int
    scanner: str
    severity: str
    cwe: str
    description: str
    file_path: str
    line_number: int
    created_at: datetime
    updated_at: datetime

class ScaVulnerability:
    id: int
    software_application_id: int
    scanner: str
    severity: str
    cwe: str
    cve: str
    description: str
    file_path: str
    line_number: int
    created_at: datetime
    updated_at: datetime