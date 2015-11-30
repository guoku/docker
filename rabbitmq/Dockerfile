FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
COPY		rabbitmq-signing-key-public.asc /tmp/rabbitmq-signing-key-public.asc
RUN			echo 'deb http://www.rabbitmq.com/debian/ testing main' >> /etc/apt/sources.list
RUN			apt-key add /tmp/rabbitmq-signing-key-public.asc
RUN			apt-get update && apt-get install -y rabbitmq-server
EXPOSE		5672
CMD			["/usr/sbin/rabbitmq-server"]