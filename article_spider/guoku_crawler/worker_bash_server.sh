HASH=$(sudo docker ps | grep guokucrawler_worker | awk '{print $1 }')
sudo docker exec -it $HASH bash