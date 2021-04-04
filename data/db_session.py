"""Module for working with database sessions"""

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import os

# This is a module for working with SQLAlchemy
# - database initialization and session creation

SqlAlchemyBase = dec.declarative_base()

__factory = None


# Function for creating folder for database
def create_folder_for_database(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)


# Database initialization function
def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify the database file.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Connecting to the database at {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import models

    SqlAlchemyBase.metadata.create_all(engine)


# Session creation function
def create_session() -> Session:
    global __factory
    return __factory()
