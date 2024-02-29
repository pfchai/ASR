# ASR
语音识别服务


## 环境搭建

### Redis

```
# docker run -d -p 6379:6379 redis
docker run --name myredis -p 6379:6379 -d redis --requirepass "mypassword"
```

### Python 环境
```
# Python 虚拟环境
conda create --name ai_asr python=3.10

pip install -r requirements.txt
```

### 配置文

```
cp .env.example .env

# 修改配置文件
vi .env
```

### 相关模型下载

角色识别，使用 [pyannote-audio](https://github.com/pyannote/pyannote-audio) 项目，相关配置见文档说明。



## 启动

```
# 首次启动，初始化数据表
python -m core.models

celery -A celery_app.tasks worker --loglevel=info -Q default
celery flower -A celery_app.tasks --broker=redis://:mypassword@localhost:6379/0 --address=127.0.0.1 --port=5555


python -m server.app
```


## 待完成

- [ ] 支持模型 [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [ ] 支持模型 [whisperX](https://github.com/m-bain/whisperX)



## 其他说明

执行出错

> RuntimeError: cuDNN version incompatibility: PyTorch was compiled  against (8, 9, 2) but found runtime version (8, 8, 0). PyTorch already comes bundled with cuDNN. One option to resolving this error is to ensure PyTorch can find the bundled cuDNN. Looks like your LD_LIBRARY_PATH contains incompatible version of cudnn. Please either remove it from the path or install cudnn (8, 9, 2)

解决，参考 https://discuss.pytorch.org/t/can-anyone-help-me-solve-it/175166

```
export LD_LIBRARY_PATH=
```