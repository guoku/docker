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