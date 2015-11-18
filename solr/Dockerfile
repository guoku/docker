FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
<<<<<<< HEAD
RUN			apt-get update
ADD			jdk-8u51-linux-x64.tar.gz /opt/
ADD			solr-4.10.4.tgz /data/
COPY		schema.xml /data/solr-4.10.4/example/solr/collection1/conf/schema.xml
ENV			JAVA_HOME /opt/jdk1.8.0_51/
ENV			JRE_HOME=${JAVA_HOME}/jre
ENV			CLASSPATH .:${JAVA_HOME}/lib:${JRE_HOME}/lib
ENV			PATH=${JAVA_HOME}/bin:$PATH
EXPOSE		8983

ENTRYPOINT	["/data/solr-4.10.4/bin/solr", "start", "-f", "-m", "8g"]
=======
RUN			apt-get update
>>>>>>> 5ca4173f7f35016b67d4704f45f730a6af7e6da5
