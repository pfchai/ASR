# -*- coding: utf-8 -*-

import os
import time
import random

from celery import group, chain
from celery.utils.log import get_task_logger

from core.models import ResultModel, db_session
from core.models import TaskStatus, update_status, update_result
from .celery import app


logger = get_task_logger(__name__)


@app.task(name='celery_app.tasks.download_audio')
def download_audio(task_id, url):
    logger.info('run download_audio')

    time.sleep(random.randint(3, 10))
    update_status(task_id, TaskStatus.TO_BE_PROCESSED)


@app.task(name='celery_app.tasks.asr_task', ignore_result=True)
def asr_task(task_id, device_index=0):
    logger.info('开始语音识别 %s', task_id)
    _st = time.time()

    time.sleep(random.randint(5, 20))

    logger.info('语音识别完成, %s，耗时：%s', task_id, time.time() - _st)


# 声纹识别
@app.task(name='celery_app.tasks.speaker_diarization_task', ignore_result=True)
def speaker_diarization_task(task_id):
    logger.info('开始声纹识别 %s', task_id)
    _st = time.time()

    time.sleep(random.randint(5, 20))

    logger.info('声纹识别完成 %s，耗时：%s', task_id, time.time() - _st)


@app.task(name='celery_app.tasks.merge_task', ignore_result=True)
def merge_task(task_id):
    logger.info('开始合并结果 %s', task_id)
    _st = time.time()

    time.sleep(random.randint(1, 3))

    # 存储结果到数据库
    update_result(task_id, 'result ' + task_id)
    logger.info('合并结果完成 %s，耗时：%s', task_id, time.time() - _st)


@app.task(name='celery_app.tasks.submit_task', ignore_result=True)
def submit_task(url, task_id, **kwargs):
    logger.info('add new task')

    process = group(asr_task.si(task_id), speaker_diarization_task.si(task_id))

    chain = download_audio.si(task_id, url) | process | merge_task.si(task_id)
    chain()

    return 'success'
