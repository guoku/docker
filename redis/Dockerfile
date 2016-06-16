FROM 		ubuntu:14.04
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get update && apt-get -y install redis-server redis-tools
RUN			echo  'vm.overcommit_memory = 1' >> /etc/sysctl.conf
ADD			redis.conf /etc/redis.conf
EXPOSE		6379
ENTRYPOINT	["/usr/bin/redis-server", "/etc/redis.conf"]
CMD			[]
