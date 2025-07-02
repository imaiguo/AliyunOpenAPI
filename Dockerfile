
FROM python:3.12.0-bookworm
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/AliyunOpenAPI

COPY requirements.txt /opt/AliyunOpenAPI/

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN python -m pip install -r requirements.txt
