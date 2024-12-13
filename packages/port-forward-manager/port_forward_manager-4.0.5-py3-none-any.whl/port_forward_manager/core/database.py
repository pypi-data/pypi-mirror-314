import os
from sqlmodel import create_engine, Session, SQLModel

from port_forward_manager.core import tools

database_path = os.path.join(tools.base_path, "database.db")
database_url = f"sqlite:///{database_path}"
engine = create_engine(database_url)


def get_session():
    return Session(engine)
