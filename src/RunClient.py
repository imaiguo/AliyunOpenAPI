
# 启动定时线程，发起http请求

import logurn
import requests
import json

if __name__ == "__main__":

    dataJson = {
        "input": "abc",
        "type":"dfdfd"
    }

    data = json.dumps(dataJson, indent=4, ensure_ascii=False)

    res = requests.post(url='http://127.0.0.1:8000/test',
                headers={"Content-Type": "application/json"},
                data=data)
    logurn.logger.debug(res.text)
