# -*- coding: utf-8 -*-

import uuid

from flask import Flask, jsonify, request

from celery_app.tasks import submit_task
from core.models import ResultModel, db_session


app = Flask(__name__)


@app.route('/submit_task', methods=['POST'])
def submit_task_api():
    # 生成唯一的任务ID
    task_id = str(uuid.uuid4())
    
    # 从请求中获取可能的模型配置
    url = request.json.get('url')
    asr_model = request.json.get('asr_model', 'default')
    speaker_model = request.json.get('speaker_model', 'default')
    
    kwargs = {
        'asr_model': asr_model,
        'speaker_model': speaker_model,
    }
    # 提交任务到 Celery
    result = submit_task.delay(url, task_id, **kwargs)
    return jsonify({"task_id": task_id}), 202


@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    result = db_session.query(ResultModel).filter_by(task_id=task_id).first()
    if result:
        return jsonify({"task_id": task_id, "result": result.result})
    else:
        return jsonify({"task_id": task_id, "result": "Pending or Not Found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5012)
