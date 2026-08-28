开始尝试
![img.png](img.png)
![img_1.png](img_1.png)
![img_2.png](img_2.png)
这个可以但是没内容

换成 php://filter/read=convert.base64-encode/resource=/var/www/html/index.php
可以读取到base64的内容，看到里面引用 db.php
再查看，解析获取到 CTF{3ecret_passw0rd_here}

心得：
关键点需要知道这个项目部署运行目录