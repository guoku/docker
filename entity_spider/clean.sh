BASE_DOCKER_NAME='gkspider_base'


echo $1

if [ "$1" == "all" ];
then
docker rmi $BASE_DOCKER_NAME
fi


if  docker images | grep $BASE_DOCKER_NAME
then echo 'spider base image exist !!'
else docker build -t $BASE_DOCKER_NAME ./base_docker
fi


docker-compose stop
docker ps -a | grep entityspider | awk '{print $1}' | xargs docker rm
docker images | grep entityspider | awk '{print $3}' | xargs docker rmi -f
docker-compose build



