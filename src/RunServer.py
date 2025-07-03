
import sys
import pathlib
rootPath = pathlib.Path(__file__).parent.parent
sys.path.append(str(rootPath))

# 1. 接受客户端的连接, 获取客户端的公网IP
# 2. 更新域名解析IP地址

import os
import loguru
import fastapi
import uvicorn
import pydantic

import Config
import src.Tools as Tools

app = fastapi.FastAPI()

gDNSIP = "127.0.0.1"
LogPath = os.path.join(rootPath, "log", "RunServer.log")

class InDataTest(pydantic.BaseModel):
    input: str
    type: int

class OutDataTest(pydantic.BaseModel):
    status:int = 200
    code: int = 0
    date: str = Tools.GetDateString()
    ip: str = None

@app.get("/health")
def health() -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post("/heartbeat", response_model=OutDataTest)
def syncFunc(data:InDataTest, request: fastapi.Request):
    ip = request.client.host
    global gDNSIP
    if data.input == "syncclientip" and data.type == 1:
        loguru.logger.info(f"Incoming client ip -> [{ip}]")
        result = OutDataTest(ip = ip)
        return result

    return fastapi.responses.JSONResponse(content={"status": "healthy"}, status_code=200)

if __name__ == "__main__":
    loguru.logger.debug("Server Start ...")
    loguru.logger.add(LogPath, rotation="1 day", retention="7 days", level="DEBUG")
    uvicorn.run(app="RunServer:app", host="0.0.0.0", port=Config.ServerPort)
