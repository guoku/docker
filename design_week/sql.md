创建表click_record的SQL语句如下：

CREATE TABLE `click_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `referer` varchar(1024) DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `user_ip` varchar(256) DEFAULT NULL,
  `entity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`));