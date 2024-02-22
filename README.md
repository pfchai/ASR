# ASR
语音识别服务


## 环境搭建

### Redis

```
# docker run -d -p 6379:6379 redis
docker run --name myredis -p 6379:6379 -d redis --requirepass "mypassword"
```


```
# Python 虚拟环境
conda create --name ai_asr python=3.10

pip install -r requirements.txt
```

## 启动

```
celery -A celery_app.tasks worker --loglevel=info -Q default
celery flower -A celery_app.tasks --broker=redis://:mypassword@localhost:6379/0 --address=127.0.0.1 --port=5555


python -m server.app
```