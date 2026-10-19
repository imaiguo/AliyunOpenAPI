
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

## 2. Windows环境部署
```bash
>
> cd D:\DevTools\PythonVenv
> python3 -m venv AliyunOpenAPI
>
```
部署环境
```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 2. Docker镜像制作

```bash
> sudo docker build -t httpdnsclient:1.0 .
```

```bash
>
> sudo docker compose up -d OpenApiHttpDNS
> sudo docker save -o httpdnsclient.1.0.tar httpdnsclient:1.0
> sudo docker load -i httpdnsclient.1.0.tar
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

## 7. PVE导出虚拟机为qcow2

- 7.1 SSH登录 PVE节点
- 虚拟机必须关机
```bash
> # a. 先查 VMID，假设虚拟机 ID 为100
> qm list
>
> # b. 查看虚拟机硬件，拿到磁盘卷 ID（例如 `local-lvm:vm-100-disk-0`）
> qm config 100
>
> # c. 通过卷 ID 获取宿主机底层路径
> pvesm path vmdata:vm-102-disk-0
>
> # 示例返回：`/dev/pve/vm-100-disk-0`（LVM），如果是目录存储会直接返回文件路径
>
> # 执行转换导出 qcow2  `-p` 显示进度条，`-c` 开启 qcow2 压缩（可选，会慢一点）
>
> # 源是raw块设备(LVM/ZFS)，-f raw
> # 如果源磁盘本身就是 qcow2（目录存储 local），去掉 `-f raw`
> qemu-img convert -p -f raw -O qcow2 /dev/vmdata/vm-102-disk-0 /opt/Data/Nas/程序/vmdisk/debian13-x64-amd64.qcow2
```

## 8. 参考

- 云解析DNS公网DNS解析开发参考API https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-overview
- 云解析 https://api.aliyun.com/api-tools/sdk/Alidns?version=2015-01-09&language=python-tea&tab=primer-doc
- 阿里云RAM账户管理 https://ram.console.aliyun.com/overview?activeTab=overview
