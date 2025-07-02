

# 阿里云 DNS云解析


## 1. Debian环境部署

设置python虚拟环境
```bash
> sudo apt install python3-venv python3-pip
> mkdir /opt/Data/PythonVenv
> cd /opt/Data/PythonVenv
> python3 -m venv AliyunOpenAPI
> source /opt/Data/PythonVenv/AliyunOpenAPI/bin/activate
```

部署推理环境
```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 2. Docker镜像制作

```bash
> sudo docker build -t imaiguo/aliyunopenai:v1.0 .
```


## 3 参考 

- 云解析DNS公网DNS解析开发参考 APIhttps://help.aliyun.com/zh/dns/api-alidns-2015-01-09-overview
