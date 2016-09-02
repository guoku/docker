HASH=$(sudo docker ps | grep entityspider_worker | awk '{print $1 }')
sudo docker exec -it $HASH bash