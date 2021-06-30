from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base

from configs import DB_CONFIG

engine = create_engine(DB_CONFIG, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.metadata.create_all(bind=engine)
