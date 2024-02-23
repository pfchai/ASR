# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request

from celery_app.tasks import submit_task
from core.models import add_task, get_result
from core.utils import create_uuid


app = Flask(__name__)


@app.route('/submit_task', methods=['POST'])
def submit_task_api():
    
    # 从请求中获取可能的模型配置
    url = request.json.get('url')
    asr_model = request.json.get('asr_model', 'default')
    speaker_model = request.json.get('speaker_model', 'default')
    
    task_id = create_uuid(url)
    kwargs = {
        'asr_model': asr_model,
        'speaker_model': speaker_model,
    }
    
    add_task(task_id, url)

    # 提交任务到 Celery
    result = submit_task.delay(url, task_id, **kwargs)
    return jsonify({"task_id": task_id}), 202


@app.route('/get_result/<task_id>', methods=['GET'])
def get_result_api(task_id):
    result = get_result(task_id)
    if result:
        return jsonify({"task_id": task_id, 'status': result.status, "result": result.result})
    else:
        return jsonify({"task_id": task_id, 'status': None, "result": "Not Found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5012)
