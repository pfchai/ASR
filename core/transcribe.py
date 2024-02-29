# -*- coding: utf-8 -*-

import os
import json

import whisper

from .utils import MODEL_SAVE_PATH, AUDIO_SAVE_PATH, RESULT_SAVE_PATH


def save_transcription_result(task_id, result):
    file_path = os.path.join(RESULT_SAVE_PATH, f'{task_id}.transcription.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)


def transcribe_audio(task_id, audio_filename, model_name='tiny', device='cpu', language='Chinese'):
    audio_path = os.path.join(AUDIO_SAVE_PATH, audio_filename)
    try:
        model = whisper.load_model(model_name, download_root=MODEL_SAVE_PATH, device=device)
        transcription_result = model.transcribe(audio_path, language=language)
        save_transcription_result(task_id, transcription_result)
        return transcription_result
    except Exception as e:
        logger.error(f'Error during transcription for task {task_id}: {e}')
        return None