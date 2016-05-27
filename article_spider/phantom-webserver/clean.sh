docker-compose stop
docker ps -a | grep phantomwebserver_web | awk '{print $1}' |xargs docker rm
docker ps -a  | grep standalone-chrome | awk '{ print $1 }' |xargs docker rm
docker rmi phantomwebserver_web