# enum for scan type
from enum import Enum


class ScanType(Enum):
    SAST = 'SAST'
    DAST = 'DAST'
    SCA = 'SCA'
    SECRETS = 'SECRETS'
