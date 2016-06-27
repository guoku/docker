HASH=$(docker ps | grep guokucrawler_worker | awk '{print $1 }')
docker exec -it $HASH bash