FROM 		ubuntu:latest
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get update && apt-get install -y php5-curl php5-gd php5-cli php5-geoip php5-fpm
COPY		php-fpm.conf /etc/php5/fpm/php-fpm.conf
COPY		www.conf /etc/php5/fpm/pool.d/www.conf
EXPOSE		9000
CMD			["/usr/sbin/php5-fpm"]