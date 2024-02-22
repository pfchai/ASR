# -*- coding: utf-8 -*-

import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging


BROKER_URL = os.environ.get('REDIS_URL', 'redis://:mypassword@localhost:6379/0')
BACKEND_URL = os.environ.get('REDIS_BACKEND_URL', 'redis://:mypassword@localhost:6379/0')

app = Celery('celery_app',
             broker=BROKER_URL,
             backend=BACKEND_URL,
             include=['celery_app.tasks'])

app.conf.update(
    task_routes={
        'celery_app.tasks.*': {'queue': 'default'},
    },
    task_annotations={
        "celery_app.tasks.*": {"rate_limit": "4/s"},
    },
    worker_concurrency=4,

    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,

    beat_schedule={
        'download_audio': {
            'task': 'celery_app.tasks.download_audio',
            # 'schedule': 10.0,
            'schedule': crontab(minute='*/5'),
        }
    }
)