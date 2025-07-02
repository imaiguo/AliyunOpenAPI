
# 1. 接受客户端的连接, 获取客户端的公网IP
# 2. 更新域名解析IP地址

import loguru
import fastapi
import uvicorn
import typing
import pydantic

app = fastapi.FastAPI()

class InDataTest(pydantic.BaseModel):
    input: str
    type: str

class OutDataTest(pydantic.BaseModel):
    status:int = 200
    code: int = 0
    msg: str = "OK"
    type: str = "1"
    datalist: typing.Optional[typing.List] = None

@app.get("/health")
def health() -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post("/heartbeat", response_model=OutDataTest)
def test(data:InDataTest):
    loguru.logger.debug(data)
    data = ['Hello', 'World']
    result = OutDataTest(
        datalist = data
    )
    return result

if __name__ == "__main__":
    loguru.logger.debug("Main")
    uvicorn.run(app="BaseMOdelTest:app", host="0.0.0.0", port=8000)
