from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool
from util.ConfigLoarder import server_host, server_port, database_name

db_url = f'postgresql://admin:1234@{server_host}:{server_port}/{database_name}'

engine = create_engine(db_url, poolclass=QueuePool, pool_size=15, max_overflow=20)

Base = declarative_base()

Session = sessionmaker(bind=engine)

SessionScope = scoped_session(sessionmaker(bind=engine))

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()