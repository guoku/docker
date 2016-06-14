sudo docker-compose stop
sudo docker ps -a | grep phantomwebserver_web | awk '{print $1}' |xargs sudo docker rm
sudo docker ps -a  | grep standalone-chrome | awk '{ print $1 }' |xargs sudo docker rm
sudo docker rmi phantomwebserver_web
