from typing import Optional

from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class GenericVulnerability(Base):
    __tablename__ = "GenericVulnerability"

    id = Column(Integer, primary_key=True)

    scan_date = Column(DateTime)
    """Date and time when the scan was performed."""

    processed_date = Column(DateTime)
    """Date and time when the vulnerability was processed by DragonAggregator."""

    original_data = Column(JSON)
    """Original data from the scan tool. This is useful for debugging and 
    for storing data that does not fit in the schema."""

    finding_id = Column(String)
    """Tool-specific finding ID."""

    title = Column(String)
    """Title of the vulnerability."""

    description = Column(String)
    """Description of the vulnerability."""

    severity = Column(String)
    """Severity of the vulnerability."""

    application_ref = Column(String)
    """Reference to the application that the vulnerability was found in."""

    file_path = Column(String)
    """Path to the file where the vulnerability was found."""

    line = Column(Integer)
    """Line number in the file where the vulnerability was found."""

    git_commit = Column(String)
    git_commit_author = Column(String)
    git_commit_email = Column(String)
    git_commit_date = Column(String)

    recommendation = Column(String)
    """Recommendation to fix the vulnerability."""

    scan_tool = Column(String)
    scan_type = Column(String)

    def to_json(self):
        return {
            "id": self.id,
            "scan_date": self.scan_date,
            "processed_date": str(self.processed_date),
            "original_data": str(self.original_data),
            "finding_id": self.finding_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "application_ref": self.application_ref,
            "file_path": self.file_path,
            "line": self.line,
            "git_commit": self.git_commit,
            "git_commit_author": self.git_commit_author,
            "git_commit_email": self.git_commit_email,
            "git_commit_date": self.git_commit_date,
            "recommendation": self.recommendation,
            "scan_tool": self.scan_tool,
            "scan_type": self.scan_type
        }


class SastVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'SastVulnerability'
    }
    cwe_id = Column(Integer)
    code_snippet = Column(String)

    def to_json(self):
        json_data = super().to_json()

        json_data.update({
            "cwe_id": self.cwe_id,
            "code_snippet": self.code_snippet
        })

        return json_data


class DastVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'DastVulnerability'
    }
    url = Column(String)
    http_method = Column(String)
    parameter = Column(String)
    attack_vector = Column(String)

    def to_json(self):
        json_data = super().to_json()

        json_data.update({
            "url": self.url,
            "http_method": self.http_method,
            "parameter": self.parameter,
            "attack_vector": self.attack_vector
        })

        return json_data


class ScaVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'ScaVulnerability'
    }
    package_name = Column(String)
    package_version = Column(String)
    fix_version = Column(String)
    license = Column(String)

    def to_json(self):
        json_data = super().to_json()

        json_data.update({
            "package_name": self.package_name,
            "package_version": self.package_version,
            "fix_version": self.fix_version,
            "license": self.license
        })

        return json_data


class SecretsVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'SecretsVulnerability'
    }
    secret_type = Column(String)
    secret_value = Column(String)

    def to_json(self):
        json_data = super().to_json()

        json_data.update({
            "secret_type": self.secret_type,
            "secret_value": self.secret_value
        })

        return json_data


def example():
    # Example usage for Veracode
    veracode_sast_vuln = SastVulnerability(
        id="V001",
        title="SQL Injection",
        description="Unsanitized input used in SQL query.",
        severity="High",
        file_path="/app/models/user.rb",
        line=42,
        recommendation="Use parameterized queries to prevent SQL injection.",
        cwe_id=89,
        code_snippet="User.find_by_sql(\"SELECT * FROM users WHERE name = '#{name}'\")"
    )

    # Example usage for Snyk
    snyk_sca_vuln = ScaVulnerability(
        id="S001",
        title="Vulnerable Dependency",
        description="The package 'lodash' is vulnerable to Prototype Pollution.",
        severity="Medium",
        package_name="lodash",
        package_version="4.17.15",
        fix_version="4.17.19",
        license="MIT"
    )

    print(veracode_sast_vuln)
    print(snyk_sca_vuln)
