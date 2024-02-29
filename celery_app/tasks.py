# -*- coding: utf-8 -*-

import time
import json

from celery import group, chain
from celery.utils.log import get_task_logger

from core.models import update_download_info, update_result
from core.utils import download_audio
from core.transcribe import transcribe_audio
from core.speaker_diarization import perform_diarization
from core.format_result import format_final_result
from .celery import app

logger = get_task_logger(__name__)


@app.task(name='celery_app.tasks.download_audio')
def download_audio_task(task_id, url):
    logger.info(f'Downloading audio for task {task_id}')
    
    audio_filename = download_audio(task_id, url)
    update_download_info(task_id, audio_filename)
    return audio_filename


@app.task(name='celery_app.tasks.transcribe_audio', ignore_result=True)
def transcribe_audio_task(audio_filename, task_id):
    logger.info(f'Starting audio transcription for task {task_id}')
    start_time = time.time()

    transcription_result = transcribe_audio(task_id, audio_filename)
    logger.info(f'Audio transcription completed for task {task_id}, took {time.time() - start_time} seconds')


@app.task(name='celery_app.tasks.perform_diarization', ignore_result=True)
def perform_diarization_task(audio_filename, task_id):
    logger.info(f'Starting speaker diarization for task {task_id}')
    start_time = time.time()

    perform_diarization(task_id, audio_filename)
    logger.info(f'Speaker diarization completed for task {task_id}, took {time.time() - start_time} seconds')


@app.task(name='celery_app.tasks.format_final_result', ignore_result=True)
def format_final_result_task(task_id):
    logger.info(f'Starting result formatting for task {task_id}')
    start_time = time.time()

    result = format_final_result(task_id)
    result_str = json.dumps(result, ensure_ascii=False)
    update_result(task_id, result_str)
    logger.info(f'Result formatting completed for task {task_id}, took {time.time() - start_time} seconds')


@app.task(name='celery_app.tasks.submit_task', ignore_result=True)
def submit_task(url, task_id, **kwargs):
    logger.info(f'Submitting new task {task_id}')

    processing_group = group(transcribe_audio_task.s(task_id), perform_diarization_task.s(task_id))
    processing_chain = chain(download_audio_task.si(task_id, url), processing_group, format_final_result_task.si(task_id))
    processing_chain()

    return 'success'