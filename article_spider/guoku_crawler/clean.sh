BASE_DOCKER_NAME='gk_article_base'

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

docker ps -a | grep phantomwebserver_web | awk '{print $1}' |xargs docker rm
docker ps -a  | grep standalone-chrome | awk '{ print $1 }' |xargs docker rm
docker rmi phantomwebserver_web

docker ps -a | grep guokucrawler | awk '{print $1}' | xargs docker rm
docker rmi guokucrawler_beat
docker rmi guokucrawler_flower
docker rmi guokucrawler_cookie_worker
docker rmi guokucrawler_worker

docker-compose build

