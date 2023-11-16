from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://admin:1234@localhost:5432/logstrack')
Base = declarative_base()