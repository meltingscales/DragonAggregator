from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DragonAggregator.models import Base, GenericVulnerability


def get_db_engine(sqlite_file_path="sqlite:///db.sqlite"):
    engine = create_engine(sqlite_file_path)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class Database:
    def __init__(self, sqlite_file_path: str):
        self.engine = get_db_engine(sqlite_file_path)
        self.session = get_session(self.engine)

        # Create tables if they don't exist
        if not inspect(self.engine).has_table(GenericVulnerability.__name__):
            Base.metadata.create_all(self.engine)

    def save_all_vulnerabilities(self, parsed: List[GenericVulnerability]):
        for vuln in parsed:

            # Check if vulnerability already exists
            is_vuln_already_saved = (
                self.session.query(GenericVulnerability)
                .filter(GenericVulnerability.finding_id == vuln.finding_id)
                .filter(GenericVulnerability.scan_tool == vuln.scan_tool)
                .filter(GenericVulnerability.scan_type == vuln.scan_type)
                .first()
            )

            if is_vuln_already_saved:
                print("skipping: Already saved: Vulnerability type {} {}, finding_id '{}'".format(
                    vuln.scan_tool,
                    vuln.scan_type,
                    vuln.finding_id,
                ))
                continue

            self.session.add(vuln)
        self.session.commit()
        print("Processed {} {} vulnerabilities".format(len(parsed), parsed[0].scan_tool))
