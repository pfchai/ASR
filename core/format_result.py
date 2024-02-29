# -*- coding: utf-8 -*-

import os
import json
import pickle

from .utils import RESULT_SAVE_PATH
from .merge_diarization import diarize_text


def load_transcription_result(task_id):
    file_path = os.path.join(RESULT_SAVE_PATH, f'{task_id}.transcription.json')
    if os.path.exists(file_path):
        with open(file_path) as f:
            return json.load(f)


def load_diarization_result(task_id):
    file_path = os.path.join(RESULT_SAVE_PATH, f'{task_id}.diarization.pickle')
    if os.path.exists(file_path):    
        with open(file_path, 'rb') as f:
            return pickle.load(f)


def write_to_file(formatted_result, file_path):
    with open(file_path, 'w') as file:
        json.dump(formatted_result, file, ensure_ascii=False)


def format_final_result(task_id):
    asr_result = load_transcription_result(task_id)
    sd_result = load_diarization_result(task_id)

    speaker_sentences = diarize_text(asr_result, sd_result)

    texts, segments = [], []
    for segment, speaker, sentence in speaker_sentences:
        # sent = zhconv.convert(sent, 'zh-cn')
        texts.append(f'{speaker}: {sentence}')
        segments.append({
            'start': segment.start,
            'end': segment.end,
            'speaker': speaker,
            'text': sentence,
        })

    formatted_result = {
        'text': '\n'.join(texts),
        'segments': segments
    }

    formatted_result_file = os.path.join(RESULT_SAVE_PATH, f'{task_id}.formatted.json')
    write_to_file(formatted_result, formatted_result_file)
    return formatted_result