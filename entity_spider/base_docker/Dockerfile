FROM python:2.7
MAINTAINER anchen@guoku.com

ENV GC_DEBUG=False
ENV PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple
ENV TZ "Asia/Shanghai"

RUN mkdir /usr/app
WORKDIR /usr/app
ADD ./requirements.txt ./
RUN pip install -r requirements.txt

