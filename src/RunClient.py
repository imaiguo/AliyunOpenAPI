
import sys
import pathlib
rootPath = pathlib.Path(__file__).parent.parent
sys.path.append(str(rootPath))

# 启动定时线程，发起http请求

import loguru
import requests
import json
import loguru

import Config
import src.Tools as Tools

ServerUrl = f"http://{Config.ServerName}:{Config.ServerPort}/heartbeat"

def doSync():
    dataJson = {
        "input": "syncclientip",
        "type": 1,
        "datetime": Tools.GetDateString()
    }

    data = json.dumps(dataJson, indent=4, ensure_ascii=False)
    res = requests.post(url=ServerUrl, headers={"Content-Type": "application/json"}, data=data)
    if res.status_code == 200:
        jsonStr = json.dumps(res.json(), indent=4, ensure_ascii=False)
        loguru.logger.debug(jsonStr)

if __name__ == "__main__":
    try:
        doSync()
    except Exception as e:
        loguru.logger.error(f"{e}")

