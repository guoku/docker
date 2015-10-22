FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
RUN		apt-get -y update
RUN		apt-get -y install gcc make cpanminus
RUN		echo "alias cpanm='cpanm --sudo --mirror http://mirrors.163.com/cpan --mirror-only'" >> /root/.bashrc
RUN		cpanm MogileFS::Utils
RUN		cpanm MogileFS::Client
RUN		cpanm IO::AIO
RUN		cpanm MogileFS::Server
RUN		mkdir /data
ADD		mogstored.conf /etc/mogilefs/mogstored.conf
VOLUME	/data
EXPOSE		7500 7501
ENTRYPOINT	["/usr/local/bin/mogstored", "--config", "/etc/mogilefs/mogstored.conf"]
CMD		[]
