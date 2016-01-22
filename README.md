# docker


* install squid


```
mkdir -p /data/squid/var/{logs,cache}

docker run -d -t -i -v /data:/data -p 10.0.2.110:3128:3128 guoku/squid
docker exec ${docker-name} /opt/squid/sbin/squid -z
docker exec ${docker-name} /opt/squid/sbin/squid -D -SY
```

* install rabbitMQ

```
docker exec ${docker-name} rabbitmqctl add_vhost 'raspberry'
docker exec ${docker-name} rabbitmqctl add_user 'raspberry' 'raspberry1@#'
docker exec ${docker-name} rabbitmqctl set_permissions -p raspberry raspberry '.*' '.*' '.*'
```