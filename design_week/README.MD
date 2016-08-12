1. 配置数据库在db.py中, 连接的是nut项目的数据库core，需要修改user, passwd, db host ip
2. 修改app.py中的SITE_HOST, 即跳转后目标URL的host
3. 执行docker-compose build, docker-compose up -d运行
4. 目前的存储使用的sqlite, 测试的话需要先调用db.py里面的init_db。首先docker ps 查看container id, 然后执行docker exec -it [container id] bash 进入容器,然后在python解释器中执行from db import inin_db， init_db(), 这样在浏览器中输入跳转的链接就可以保存到数据库了。