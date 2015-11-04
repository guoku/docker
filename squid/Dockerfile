FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get -y update && apt-get -y install gcc make
ADD			squid-2.7.STABLE9.tar.gz /tmp/
WORKDIR		/tmp/squid-2.7.STABLE9
RUN			./configure '--prefix=/opt/squid/' '--enable-epoll' '--enable-gnuregex' \
			'--disable-wccp' '--disable-wccpv2' '--enable-kill-parent-hack' '--with-pthreads' \
			'--with-aio' '--with-dl' '--with-large-files' '--with-maxfd=65536' '--enable-storeio=ufs,coss' \
			'--with-aufs-threads=100' '--enable-coss-aio-ops' '--enable-x-accelerator-vary'
RUN			make && make install
COPY		squid.conf /opt/squid/etc/squid.conf
VOLUME 		["/data"]
EXPOSE 		3128


