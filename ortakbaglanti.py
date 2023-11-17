from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

db_url = 'postgresql://admin:1234@localhost:5432/logstrack'
engine = create_engine(db_url, poolclass=QueuePool, pool_size=5, max_overflow=10)
Base = declarative_base()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()


SessionScope = scoped_session(sessionmaker(bind=engine))

@contextmanager
def transaction_scope():
    session = Session()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        Session.remove()