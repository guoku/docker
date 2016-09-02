BASE_DOCKER_NAME='gk_article_base'

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

sudo docker ps -a | grep phantomwebserver_web | awk '{print $1}' |xargs sudo docker rm
sudo docker ps -a  | grep standalone-chrome | awk '{ print $1 }' |xargs sudo docker rm
sudo docker rmi phantomwebserver_web


sudo docker ps -a | grep guokucrawler | awk '{print $1}' | xargs sudo docker rm
sudo docker rmi guokucrawler_beat
sudo docker rmi guokucrawler_flower
sudo docker rmi guokucrawler_cookie_worker
sudo docker rmi guokucrawler_worker


sudo docker-compose build