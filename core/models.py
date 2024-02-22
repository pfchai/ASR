# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


DATABASE_URI = 'sqlite:///results.db'
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class ResultModel(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(36), unique=True)
    result = Column(String)

    def __init__(self, task_id=None, result=None):
        self.task_id = task_id
        self.result = result

# 创建表
Base.metadata.create_all(bind=engine)
