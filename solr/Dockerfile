FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get update
ADD			jdk-8u51-linux-x64.tar.gz /opt/
ENV			JAVA_HOME /opt/jdk1.8.0_51/
ENV			JRE_HOME=${JAVA_HOME}/jre
ENV			CLASSPATH .:${JAVA_HOME}/lib:${JRE_HOME}/lib
ENV			PATH=${JAVA_HOME}/bin:$PATH

ADD			solr-4.10.4.tgz /data/
COPY		schema.xml /data/solr-4.10.4/example/solr/collection1/conf/schema.xml
RUN			mkdir -p /data/solr-4.10.4/example/solr-webapp/webapp/
WORKDIR		/data/solr-4.10.4/example/solr-webapp/webapp
RUN			jar xf /data/solr-4.10.4/example/webapps/solr.war
#COPY		IKAnalyzer2012FF_u1.jar /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/lib/IKAnalyzer2012FF_u1.jar
COPY		ikanalyzer.jar /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/lib/ikanalyzer.jar
RUN			mkdir -p /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/classes
COPY		IKAnalyzer.cfg.xml /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/classes/IKAnalyzer.cfg.xml
COPY		stopword.dic /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/classes/stopword.dic
COPY		ext.dic /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/classes/ext.dic
COPY		brand.dic /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/classes/brand.dic
COPY		synonyms.dic /data/solr-4.10.4/example/solr-webapp/webapp/WEB-INF/classes/synonyms.dic
EXPOSE		8983
WORKDIR		/data/solr-4.10.4/
ENTRYPOINT	["/data/solr-4.10.4/bin/solr", "start", "-f", "-m", "8g"]
