BASE_DOCKER_NAME='gkspider_base'


echo $1

if [ "$1" == "all" ];
then
sudo docker rmi $BASE_DOCKER_NAME
fi


if  sudo docker images | grep $BASE_DOCKER_NAME
then echo 'spider base image exist !!'
else sudo docker build -t $BASE_DOCKER_NAME ./base_docker
fi


sudo docker-compose stop
sudo docker ps -a | grep entityspider | awk '{print $1}' | xargs  sudo docker rm
sudo docker images | grep entityspider | awk '{print $3}' | xargs sudo docker rmi -f
sudo docker-compose build



