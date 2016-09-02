HASH=$(docker ps | grep entityspider_worker | awk '{print $1 }')
docker exec -it  $HASH bash
