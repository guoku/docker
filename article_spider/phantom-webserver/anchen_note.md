1.  some conv shell command 


docker rmi -f $(docker images | grep "<none>" | awk "{print \$3}")

a. remove all webserver container 

docker ps -a | grep webserver | awk "{print \$1}" |xargs docker rm

b. remove useless images 

docker images | grep '<none>' | awk "{print \$3}" |xargs docker rmi

