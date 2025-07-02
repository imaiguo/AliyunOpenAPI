
import sys
import pathlib
rootPath = pathlib.Path(__file__).parent.parent
sys.path.append(str(rootPath))

# 启动定时线程，发起http请求

import time
import loguru
import requests
import json
import loguru

import Config
import src.Tools as Tools

ServerUrl = f"http://{Config.ServerName}:{Config.ServerPort}/heartbeat"
gDNSIP = "127.0.0.1"

def doSync():
    dataJson = {
        "input": "syncclientip",
        "type": 1,
        "datetime": Tools.GetDateString()
    }

    data = json.dumps(dataJson, indent=4, ensure_ascii=False)
    res = requests.post(url=ServerUrl, headers={"Content-Type": "application/json"}, data=data)
    if res.status_code == 200:
        global gDNSIP
        # jsonStr = json.dumps(res.json(), indent=4, ensure_ascii=False)
        if res.json()['code'] == 0:
            ip = res.json()['ip']
            loguru.logger.debug(f"get back current ip - > [{ip}]")

            if gDNSIP != ip:
                loguru.logger.debug(f"ip[{ip}] is different to old [{gDNSIP}]")
                if Tools.UpdateDNS(ip):
                    loguru.logger.debug(f"Domain Record updated ok.")
                    gDNSIP = ip
                else:
                    loguru.logger.error(f"Domain Record updated failed.")
            else:
                loguru.logger.debug(f"ip[{ip}] is same to old[{gDNSIP}]")

if __name__ == "__main__":
    while(True):
        try:
            doSync()
        except Exception as e:
            loguru.logger.error(f"{e}")
        time.sleep(60)
