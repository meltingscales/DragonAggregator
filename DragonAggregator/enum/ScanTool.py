from enum import Enum


class ScanTool(Enum):
    VERACODE = 'VERACODE'
    SONARQUBE = 'SONARQUBE'
    GITLEAKS = 'GITLEAKS'
