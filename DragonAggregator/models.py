from typing import Optional

from sqlalchemy import Column, Integer, String
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

    finding_id = Column(String)

    title = Column(String)
    description = Column(String)

    severity = Column(String)

    application_ref = Column(String)

    file_path = Column(String)
    line = Column(Integer)

    git_commit = Column(String)
    git_commit_author = Column(String)
    git_commit_email = Column(String)
    git_commit_date = Column(String)
    
    recommendation = Column(String)

    scan_tool = Column(String)
    scan_type = Column(String)


class SastVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'SastVulnerability'
    }
    cwe_id = Column(Integer)
    code_snippet = Column(String)


class DastVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'DastVulnerability'
    }
    url = Column(String)
    http_method = Column(String)
    parameter = Column(String)
    attack_vector = Column(String)


class ScaVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'ScaVulnerability'
    }
    package_name = Column(String)
    package_version = Column(String)
    fix_version = Column(String)
    license = Column(String)


class SecretsVulnerability(GenericVulnerability):
    __mapper_args__ = {
        'polymorphic_identity': 'SecretsVulnerability'
    }
    secret_type = Column(String)
    secret_value = Column(String)


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
