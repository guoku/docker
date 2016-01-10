FROM        ubuntu
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN         apt-get update && apt-get -y install python2.7 python2.7-dev python-pip libffi-dev libmysqlclient-dev
RUN         pip install -U flask requests gunicorn cffi gevent Flask-SQLAlchemy MySQL-python \
			-i http://pypi.douban.com/simple
VOLUME		/data
EXPOSE		8000
