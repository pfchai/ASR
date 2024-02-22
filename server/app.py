
import uuid

from flask import Flask, jsonify, request

from celery_app.tasks import submit_task


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


if __name__ == '__main__':
    app.run(debug=True, port=5012)
