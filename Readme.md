
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

```bash
>
> sudo docker compose up -d openapiserver
>
> sudo docker compose up -d openapiclient
>
```

## 3. 把python脚本打包为一个exe
```bash
>
> # 查找python安装路径
> python -m site --user-base
>
> C:\Users\ephraim\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\pyinstaller --onefile src/RunBigmodelSiteLocalUpdate.py .\Config.py
>
```


## 4. windows添加启动服务

- 命令行添加服务、注册表、启动、任务计划，实现开机运行exe或bat 
- 启动优先级：服务>注册表>启动文件夹>计划

```bash
>
> #添加服务 管理员模式打开cmd
> cmd
> sc create AliyunOpenAPI binpath= "D:\devtools\AliyunOpenAPI\RunBigmodelSiteLocalUpdate.exe" displayname= "域名自动注册" depend= Tcpip start= auto
>
> #注意：
> # 1）binPath=后面一定要有个空格，否则会出现错误。
> # 2）如果建错了或者需要修改，这时需要先删除服务，再重新创建，删除服务的命令：
>
> # 删除服务
> sc delete AliyunOpenAPI
> # 在提示建立成功后，可以直接输入
> # 启动服务
> net start AliyunOpenAPI
>
```

## 5. 使用nssm注册服务

```bash
>
> D:\devtools\nssm.2.24\win64\nssm.exe install
> D:\devtools\nssm.2.24\win64\nssm.exe start AliyunOpenAPI
> D:\devtools\nssm.2.24\win64\nssm.exe restart
> D:\devtools\nssm.2.24\win64\nssm.exe stop AliyunOpenAPI
> D:\devtools\nssm.2.24\win64\nssm.exe remove AliyunOpenAPI
>
> # 日志路径 C:\Windows\Temp\AliyunOpenAPI.log
>
```

## 6. 下载python依赖包到目录
```bash
>
> pip download loguru -d project\sidepackage\loguru
> pip download -r requirements.txt -d project\sidepackage\loguru
> # 离线安装
> py -3.8-64 -m pip install --no-index --find-link project\sidepackage\loguru loguru
>
```

## 6. 参考

- 云解析DNS公网DNS解析开发参考API https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-overview
- 云解析 https://api.aliyun.com/api-tools/sdk/Alidns?version=2015-01-09&language=python-tea&tab=primer-doc
- 阿里云RAM账户管理 https://ram.console.aliyun.com/overview?activeTab=overview
