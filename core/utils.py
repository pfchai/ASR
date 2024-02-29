# -*- coding: utf-8 -*-

import os
import hashlib
from dotenv import load_dotenv

import requests


def create_uuid(url, encoding='utf-8'):
    return hashlib.md5(url.encode(encoding)).hexdigest()


def get_project_path():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.split(current_file_path)[0]
    return os.path.abspath(os.path.join(current_dir, '../'))


PROJECT_PATH = get_project_path()
DATA_PATH = os.path.join(PROJECT_PATH, 'data')
MODEL_SAVE_PATH = os.getenv('MODEL_SAVE_PATH', os.path.join(DATA_PATH, 'models'))
DATA_CACHE_PATH = os.getenv('AUDIO_SAVE_PATH', os.path.join(DATA_PATH, 'caches'))
AUDIO_SAVE_PATH = os.getenv('AUDIO_SAVE_PATH', DATA_CACHE_PATH)
RESULT_SAVE_PATH = os.getenv('RESULT_SAVE_PATH', os.path.join(DATA_PATH, 'files'))



def download_audio(task_id, url):
    try:
        file_ext = url.split('.')[-1]
        if file_ext not in ('mp3', 'mp4'):
            file_ext = 'acc'

        filename = f'{task_id}.{file_ext}'
        save_path = os.path.join(AUDIO_SAVE_PATH, filename)

        if os.path.exists(save_path):
            return filename

        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Error downloading audio file: {}".format(response.status_code))

        with open(save_path, "wb") as f:
            f.write(response.content)

        return filename
    except Exception as e:
        raise e

