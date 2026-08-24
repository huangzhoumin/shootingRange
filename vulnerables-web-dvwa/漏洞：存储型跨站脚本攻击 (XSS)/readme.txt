> 链接：`/vulnerabilities/xss_s/`，是留言板形式，分为 **Name（名字）、Message（留言）** 两个输入框。
> ⚠️注意：Name 输入框前端有`maxlength`长度限制，长 payload 需要 F12 修改 html 里`maxlength="100"`，或者用 Burp 抓包提交，绕过前端限制。
> 存储型 XSS 特点：payload 存入数据库，**刷新页面就自动触发弹窗**，不需要点链接，所有访问该页面的用户都会中招。

## Low 级别（无过滤）

- Message 框直接输入：

```
<script>alert(1)</script>
```

Name 随便填普通字符，点`Sign Guestbook`提交，刷新页面就弹窗成功。

## Medium 级别

后端`Message`做了过滤；`Name`会把小写`<script>`替换为空，**大小写不会过滤**。

1. 方法 1：Name 框大小写绕过（先改 maxlength 长度）

```
<Script>alert(1)</Script>
```

2. 方法 2：img 事件绕过（推荐，兼容性强）

```
<img src=x onerror=alert(1)>
```

>
> src=x 图片不存在，触发`onerror`事件执行 JS，不需要 script 标签。

## High 级别

正则严格过滤所有变体的`<script>`标签，script 标签全部失效，依旧可以用**事件标签绕过**，在 Name 字段提交：

```
<img src=x onerror=alert(document.cookie)>
```

>
> 建议用 Burp 抓包发送，避开前端 maxlength 限制，提交后刷新页面自动弹窗。

## Impossible 级别

对两个输入全部使用`htmlspecialchars()`做 HTML 实体编码，所有`< > " ' &`全部转义，**不存在可用 payload，无法攻击**，这是安全的防御写法。