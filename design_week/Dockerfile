FROM python:2.7
MAINTAINER goforalong@gmail.com
EXPOSE 7000

ENV PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple
RUN mkdir /usr/design_week
WORKDIR /usr/design_week
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD . .

CMD gunicorn -b 0.0.0.0:7000 -t 180 --access-logfile "-" app:app
