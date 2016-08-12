1.  移除的商品, 应该不用再抓取了.
2.  抓取到的商品状态,如果是 移除 状态, 则, 需要把


===============================
to deploy 
===============================

1. cd deploy 
2. source a venv with fabric support 
3. fab -f upload_entity_spider_production.py upload 
4. enter pass word for production server (10.0.2.49)

5. ssh to production server 
6. cd /home/anchen/entity_spider
7. run   ./clean_server.sh
8. run   ./sudo docker-compose up -d 

===============================
to see log
===============================

1. docker exec -it {hash} bash 
2. cd entity_spider/config/logs
3. tail -f -n 100 request.log

===============================
to begin entity spider manually 
===============================

1. docker exec -it {hash} bash
2. cd entity_spider/job
3. python check_entity_state.py


TODO : 
1. image crawl
2. category assign 

source /new_sand/venvs/py2711/bin/activate
export PYTHONPATH=/new_sand/python_projects/entity_spider:/new_sand/python_projects/entity_spider/entity_spider/api


celery -A entity_spider.CeleryApp worker --loglevel=error


error shop id 
48
104
150
85

