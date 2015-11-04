FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get -y update && apt-get -y install gcc make cpanminus
RUN			echo "alias cpanm='cpanm --sudo --mirror http://mirrors.163.com/cpan --mirror-only'" >> /root/.bashrc
RUN			cpanm MogileFS::Utils
RUN			cpanm MogileFS::Client
RUN			cpanm IO::AIO
RUN			cpanm MogileFS::Server
ADD			mogstored.conf /etc/mogilefs/mogstored.conf
VOLUME		["/data"]
EXPOSE		7500 7501
ENTRYPOINT	["/usr/local/bin/mogstored", "--config", "/etc/mogilefs/mogstored.conf"]
CMD		[]
