# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Text, SmallInteger, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI, echo=False)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class TaskStatus():
    ERROR = -1
    TO_BE_DOWNLOADED = 0
    TO_BE_PROCESSED = 1
    FINISHED = 2


class ResultModel(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(32), nullable=False)
    audio_url = Column(String(256))
    filename = Column(String(64))
    status = Column(SmallInteger, default=TaskStatus.TO_BE_DOWNLOADED)
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, onupdate=func.now())
    result = Column(Text)


def add_task(task_id, audio_url):
    try:
        new_task = ResultModel(task_id=task_id, audio_url=audio_url, status=TaskStatus.TO_BE_DOWNLOADED)
        db_session.add(new_task)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.remove()


def update_download_info(task_id, filename):
    try:
        task = db_session.query(ResultModel).filter_by(task_id=task_id).first()
        if task:
            task.filename = filename
            task.status = TaskStatus.TO_BE_PROCESSED
            db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.remove()


def update_result(task_id, result):
    try:
        task = db_session.query(ResultModel).filter_by(task_id=task_id).first()
        if task:
            task.result = result
            task.status = TaskStatus.FINISHED
            db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.remove()


def get_result(task_id):
    try:
        return db_session.query(ResultModel).filter_by(task_id=task_id).first()
    finally:
        db_session.remove()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
