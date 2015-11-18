# docker

<<<<<<< HEAD

* install squid


```
mkdir -p /data/squid/var/{logs,cache}

docker run -d -t -i -v /data:/data -p 10.0.2.110:3128:3128 guoku/squid
docker exec ${docker-name} /opt/squid/sbin/squid -z
docker exec ${docker-name} /opt/squid/sbin/squid -D -SY
```

=======
>>>>>>> 5ca4173f7f35016b67d4704f45f730a6af7e6da5
