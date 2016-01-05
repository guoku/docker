FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get update && apt-get install -y wget openjdk-7-jre openjdk-7-jdk
RUN			echo 'export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64' >> ~/.bashrc
WORKDIR		/tmp/
RUN			wget http://mirror.bit.edu.cn/apache/hadoop/common/stable2/hadoop-2.7.1.tar.gz
RUN			tar xzvf hadoop-2.7.1.tar.gz
RUN			rm -f /tmp/hadoop-2.7.1.tar.gz