FROM 		ubuntu:14.04
MAINTAINER	jiaxin	<jiaxin@guoku.com>
COPY		sources.list.trusty /etc/apt/sources.list
RUN			apt-get update && apt-get install -y gcc g++ cmake libreadline6 libreadline6-dev libncurses5-dev zlib1g-dev
ADD			percona-server-5.6.27-75.0.tar.gz /tmp/
WORKDIR		/tmp/percona-server-5.6.27-75.0
RUN			cmake . -DINSTALL_LAYOUT=SVR4 -DMYSQL_DATADIR=/data/mysql \
			-DCMAKE_INSTALL_PREFIX=/opt/mysql5 \
			-DCMAKE_C_FLAGS_RELWITHDEBINFO="-O3 -g" \
			-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-O3 -g" \
			-DWITH_INNOBASE_STORAGE_ENGINE=1 \
			-DEFAULT_CHARSET=utf8mb4 \
			-DEFAULT_COLLATION=utf8mb4_unicode_ci \
			-DMYSQL_UNIX_ADDR=/tmp/mysql.sock \
			-DWITH_EMBEDDED_SERVER=ON
RUN			make && make install
RUN			rm -rf /tmp/percona-server-5.6.27-75.0
RUN			useradd -s /bin/false -d /opt/mysql5 mysql
RUN			chown -R mysql /opt/mysql5
WORKDIR		/opt/mysql5
VOLUME 		["/data"]
ADD 		my.cnf /etc/my.cnf
RUN			/opt/mysql5/scripts/mysql_install_db --user=mysql
EXPOSE		3306
