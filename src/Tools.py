
import sys
import pathlib
rootPath = pathlib.Path(__file__).parent.parent
sys.path.append(str(rootPath))

import datetime
import loguru

from Tea.exceptions import UnretryableException, TeaException
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109.client import Client as Client
from alibabacloud_alidns20150109 import models as models

import Config

def GetDateString():
    now = datetime.datetime.now()
    dateStr = now.strftime("%Y-%m-%d %H:%M:%S")
    loguru.logger.debug(dateStr)
    return dateStr

def UpdateDNS(ip):
    # 1. 配置访问客户端
    loguru.logger.debug(f"UpdateDNS -> [{ip}]")
    config = open_api_models.Config(access_key_id = Config.AccessKeyID, access_key_secret = Config.AccessKeySecret)
    client = Client(config)
    # 访问的域名
    config.endpoint = 'alidns.cn-hangzhou.aliyuncs.com'

    # 2. 配置请求参数
    request = models.AddCustomLineRequest()
    # 设置请求类 request 的参数。 通过设置 request 类的属性设置参数，即 API 中必须要提供的信息
    # 该参数值为假设值，请您根据实际情况进行填写
    request.lang = "your_value";
    # 该参数值为假设值，请您根据实际情况进行填写
    request.domain_name = "your_value";
    # 该参数值为假设值，请您根据实际情况进行填写
    request.line_name = "your_value";

    # 3. 获取请求结果
    try:
        response = client.add_custom_line(request)
        print(response)
        request_id = response.body.request_id
        print(request_id)
    except UnretryableException as e:
        # 网络异常
        print(e)
    except TeaException as e:
        # 业务异常
        print(e)
    except Exception as e:
        # 其他异常
        print(e)
