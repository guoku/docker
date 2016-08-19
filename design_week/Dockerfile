FROM python:2.7
MAINTAINER goforalong@gmail.com
EXPOSE 7000

ENV PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple
RUN mkdir /usr/design_week
WORKDIR /usr/design_week
ADD requirements.txt ./
RUN pip install -r requirements.txt
COPY gunicorn /etc/default/gunicorn
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD . .
CMD supervisord