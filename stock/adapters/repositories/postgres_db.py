from typing import Optional
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


class PostgresDB:

    Base = declarative_base()

    def __init__(
        self,
        host: str,
        port: str,
        username: str,
        password: str,
        database: str
    ):
        self._engine = create_engine(
            'postgresql://{}:{}@{}:{}/{}'.format(
                username, password, host, port, database
            ))
        self._Session = sessionmaker(bind=self._engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self._Session()
        logging.debug("PostgresDB.session_scope:Session was started")
        try:
            yield session
            session.commit()
            logging.debug(
                "PostgresDB.session_scope:Session was committed")
        except Exception as e:
            logging.error(
                "PostgresDB.session_scope:Session rollback because of exception")
            session.rollback()
            logging.debug(
                "PostgresDB.session_scope:Exception occured and session rollback occured")
            raise
        finally:
            session.close()
            logging.debug(
                "PostgresDB.session_scope:Session was closed")

    def setup_database_tables(self):
        PostgresDB.Base.metadata.drop_all(self._engine)
        PostgresDB.Base.metadata.create_all(self._engine)
        logging.info('PostgresDB.setup_database_tables:Completed')
