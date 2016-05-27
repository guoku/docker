update  2015 - 5 -13 

1 .   fab -f upload_crawler_test.py upload 
    to deploy on 48 , test 
          
2.    fab -f upload_crawler_production.py upload 
    to deploy on 49 , production 
    

3.   in /home/anchen/crawler/guoku_crawler 
     run ./clean_server.sh 
     run sudo docker-compose up -d 
     get worker container hash 
     run sudo docker exec -it {hash} bash enter the container 
     run test in container 
     
up is the newest deploy/testing process , 
for elder process see following , 
make sure you understand docker .


====================================================
first  you must config the project

see configure.md for detail 

-------------------------

# back up production database 
    1. core_article
    2. core_selection_article
    3. core_article_dig
    4. core_article_related_entities
    
   

#deploy phantom webserver

1. cd to {phantom web server dir}

2. to see if there is any running container
    sudo docker-compose ps

3. stop this docker-compose containers  
    sudo docker-compose stop 
    
4. remove stoped container and old image
    sudo docker ps -a | grep phantomwebserver_web | awk '{print $1}' |xargs docker rm
    sudo docker ps -a  | grep standalone-chrome | awk '{ print $1 }' |xargs docker rm
    docker rmi phantomwebserver_web
    
5. rebuild 
    sudo docker-compose build 
    
6. run
    sudo docker-compose up 
    
7. check
    a. get the local ip (for linux)
    b. get the docker-machine ip (for mac)
    c. access  http://ip:5000/_health , if webserver is working 
    d. access  http://ip:4444/ , if the selenium is working 

    if anything wrong , check code , restart from step 1 
    
    f. use postman to post get_cookie to ensure cookie provider is ready
    


  -------------------------------------------------- 


# depoly guoku_crawler 
 
 
8. cd to guoku_crawler dir  and stop all project container 
    docker-compose stop 
    

9. remove any stoped container from host
   remove old images from the host 
   
   sudo docker ps -a | grep guokucrawler | awk '{print $1}' | xargs sudo docker rm
   sudo docker rmi guokucrawler_beat
   sudo docker rmi guokucrawler_flower
   sudo docker rmi guokucrawler_cookie_worker
   sudo docker rmi guokucrawler_worker

 10. build images 
   sudo docker-compose build 
  
 11. run 
   sudo docker-compose up -d 
   
 12. check
   get docker host ip 
        http://io:5555/   check celery-flower working
        
        
   into the worker bash :
        sudo docker-compose run worker bash  #wrong !!!!!
        
        sudo docker attach {container-id} 
        
        http://askubuntu.com/questions/505506/how-to-get-bash-or-ssh-into-a-running-container-in-background-mode
   
   in container bash : 
        cd guoku_crawler/articles
        python crawler
        
   you SHOULD SEE THE MISSION RUNING NOW !!
        
   
13. fetch 1 user weixin article 
   a . into the worker bash:
   b . in guoku_crawler dir 
       python craw_user_weixin.py  {authorized_use_id}
   
   
       
14. test craw
       1. in your test database !!!!
      
       python craw_user_weixin.py 5 (for haruru)
       see if there is any new article in 
       
---------------------
some time you

    export LC_ALL="en_US.UTF-8"
    sudo apt-get install libcurl4-openssl-dev
    
    
-----------------------------
    
    or  you can use 
    
    1. clean_server.sh 
       to rebuild crawler 
    2. setup_env.sh 
       to add python path , for local test convenient 