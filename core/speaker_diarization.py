# -*- coding: utf-8 -*-

import os
import pickle
from dotenv import load_dotenv

import torch
from pyannote.audio import Audio, Pipeline
from transformers.pipelines import audio_utils
from celery.utils.log import get_task_logger

from .utils import MODEL_SAVE_PATH, AUDIO_SAVE_PATH, RESULT_SAVE_PATH


logger = get_task_logger(__name__)
load_dotenv()


def save_diarization_result(task_id, result):
    file_path = os.path.join(RESULT_SAVE_PATH, f'{task_id}.diarization.pickle')
    with open(file_path, 'wb') as f:
        pickle.dump(result, f)


def perform_diarization(task_id, audio_filename, num_speakers=2, cuda_device_index='0'):
    use_auth_token = os.getenv('hf_auth_token')
    model_name = 'pyannote/speaker-diarization-3.1'
    pipeline = Pipeline.from_pretrained(model_name, use_auth_token=use_auth_token)
    if cuda_device_index != '-1':
        pipeline.to(torch.device(f'cuda:{cuda_device_index}'))

    audio_path = os.path.join(AUDIO_SAVE_PATH, audio_filename)
    try:
        io = Audio(mono='downmix', sample_rate=16000)
        waveform, sample_rate = io(audio_path)
        diarization_result = pipeline({"waveform": waveform, "sample_rate": sample_rate})
        
        save_diarization_result(task_id, diarization_result)
        return diarization_result
    except Exception as e:
        logger.error(f'Error during diarization for task {task_id}: {e}')