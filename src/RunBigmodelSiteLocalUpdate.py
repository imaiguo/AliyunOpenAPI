
import sys
import pathlib
rootPath = pathlib.Path(__file__).parent.parent
sys.path.append(str(rootPath))

import os
import time
import datetime
import loguru
import netifaces

from Tea.exceptions import UnretryableException, TeaException
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109.client import Client as DnsClient
from alibabacloud_alidns20150109 import models as DnsModels

import Config

RRName = "code"
gDNSIP = "127.0.0.1"
LogPath = os.path.join(rootPath, "AliyunOpenAPI.log")

def GetDateString():
    now = datetime.datetime.now()
    dateStr = now.strftime("%Y-%m-%d %H:%M:%S")
    loguru.logger.debug(dateStr)
    return dateStr

@staticmethod
def GetClient(region_id: str = None) -> DnsClient:
    config = open_api_models.Config()
    config.access_key_id = Config.AccessKeyID
    config.access_key_secret =  Config.AccessKeySecret
    config.region_id = region_id
    config.endpoint = 'alidns.cn-hangzhou.aliyuncs.com'
    return DnsClient(config)

# 获取域名ID列表
def GetDescribeDomain():
    id = ""
    type = ""
    # 1 配置request
    request = DnsModels.DescribeDomainRecordsRequest()
    request.lang = "zh"
    request.domain_name = "bigmodel.site"

    # 2 配置访问客户端
    client = GetClient()

    # 3. 获取请求结果
    try:
        response = client.describe_domain_records(request)
        record = response.body.domain_records.record[0]
        for record in response.body.domain_records.record:
            # loguru.logger.debug(record)
            recordID = record.record_id
            recordsValue = record.value
            recordsRR  = record.rr
            recordstype = record.type
            value = record.value
            # loguru.logger.debug(f"[{recordID}] -> [{recordsRR}] -> [{recordsValue}] -> [{recordstype}] -> [{value}]")
            if recordsRR == RRName:
                id = recordID
                type = recordstype
    except UnretryableException as e:
        loguru.logger.error(e)
    except TeaException as e:
        loguru.logger.error(e)
    except Exception as e:
        loguru.logger.error(e) 
    return id, type

# 更新指定的域名解析
def UpdateDNSIP(ip, rrid, type):
    # 1 修改解析记录
    req = DnsModels.UpdateDomainRecordRequest()
    # 主机记录
    req.rr = RRName
    # 记录ID
    req.record_id = rrid
    # 将主机记录值改为当前主机IP
    req.value = ip
    # 解析记录类型
    req.type = type

    # 2 配置访问客户端
    client = GetClient()

    # 3. 获取请求结果
    try:
        response = client.update_domain_record(req)
        if response.status_code == 200:
            loguru.logger.info(f"RR[{RRName}] is update to ip [{ip}] RequestId-> [{response.body.request_id}]")
        else:
            loguru.logger.error(f"RR[{RRName}] is update to ip [{ip}] Failed")

    except UnretryableException as e:
        loguru.logger.error(e)
        return False
    except TeaException as e:
        loguru.logger.error(e)
        if e.code == "DomainRecordDuplicate":
            return True
    except Exception as e:
        loguru.logger.error(e)
        return False
    return True

def UpdateDNS(ip):
    id, type = GetDescribeDomain()
    loguru.logger.debug(f"Get RR id -> [{id}] type -> [{type}]")
    return UpdateDNSIP(ip=ip, rrid=id, type=type)

def GetLocalIP():
    global gDNSIP
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for addr in addresses[netifaces.AF_INET]:
                ip = addr['addr']
                # print(f"接口 {interface} 的 IPv4 地址是: [{ip}]")
                loguru.logger.debug(f"接口 {interface} 的 IPv4 地址是: [{ip}]")
                if ip.startswith("10.76"):
                    if gDNSIP != ip:
                        loguru.logger.debug(f"ip[{ip}] is different to old[{gDNSIP}]")
                        gDNSIP = ip
                        return ip
                    else:
                        loguru.logger.debug(f"ip[{ip}] is same to old[{gDNSIP}]")

    return ""

def RunMain():
    loguru.logger.debug(f"LogPath ->[{LogPath}]")
    loguru.logger.add(LogPath, rotation="1 day", retention="7 days", level="DEBUG")
    loguru.logger.debug("Server Start ...")
    while True:
        ip = GetLocalIP()
        if(len(ip) > 0):
            id, type = GetDescribeDomain()
            loguru.logger.debug(f"Get RR id -> [{id}] type -> [{type}]")
            UpdateDNSIP(ip, id, type=type)

        time.sleep(60*5)

if __name__ == "__main__":
    RunMain()
