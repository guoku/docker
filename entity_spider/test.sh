BASE_DOCKER_NAME='gkspider_base'


if  docker images | grep $BASE_DOCKER_NAME
then echo 'spider base image exist !!'
else docker build -t $BASE_DOCKER_NAME ./base_docker
fi

