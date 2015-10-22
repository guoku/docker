FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
RUN		apt-get update
RUN		apt-get -y install cpanminus
RUN		echo "alias cpanm='cpanm --sudo --mirror http://mirrors.163.com/cpan --mirror-only'" >> .bashrc
RUN		cpanm MogileFS::Server
RUN		cpanm MogileFS::Utils
RUN		cpanm MogileFS::Client
RUN		cpanm IO::AIO
ADD		mogstored.conf /etc/mogilefs/mogstored.conf
EXPOSE		6379
ENTRYPOINT	["/usr/bin/redis-server", "/etc/redis.conf"]
CMD		[]
