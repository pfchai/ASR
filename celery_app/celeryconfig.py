# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

from celery.schedules import crontab


load_dotenv()

broker_url = os.getenv('BROKER_URL')
result_backend = os.getenv('BACKEND_URL')

include=['celery_app.tasks']

task_routes = {
    'celery_app.tasks.*': {'queue': 'default'},
}
task_annotations={
    "celery_app.tasks.*": {"rate_limit": "4/s"},
}
worker_concurrency = 4

beat_schedule = {
    'download_audio': {
        'task': 'celery_app.tasks.download_audio',
        'schedule': crontab(minute='*/5'),
    }
}

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone='Asia/Shanghai',
enable_utc = True
