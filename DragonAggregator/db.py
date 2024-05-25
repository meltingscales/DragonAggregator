from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db_engine(sqlite_file_path="sqlite:///db.sqlite"):
    engine = create_engine(sqlite_file_path)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
