> 访问地址：`/vulnerabilities/csp/`，页面有一个 `include` 参数输入框，CSP（内容安全策略）用来限制浏览器可以加载哪些 JavaScript，本题就是找策略缺陷实现 JS 执行。
> ⚠️ 仅用于本地靶场学习，禁止用于非授权网站。

---

## Low（低级）

**CSP 策略**：`script‑src 'self' https://pastebin.com ...`，白名单允许 pastebin 等外部站点脚本。

- 原理：输入框内容直接拼接到 `<script src="输入值">`，只要域名在 CSP 白名单就会执行 JS。
- 方法 1：在 pastebin 新建文本，写`alert(1)`，点 raw 拿到原始 JS 链接，填入输入框提交。
- 方法 2：配合文件上传漏洞，上传 js 文件，填入相对路径 `../../hackable/uploads/xxx.js`GitHub。

Payload 示例填入输入框：

```
https://pastebin.com/raw/xxxxxx
```

---

## Medium（中级）

**CSP 策略**：`script‑src 'self' 'nonce‑TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA='`，只允许带这个固定 nonce 的内联 script 标签执行 JS。

>
> nonce 是 CSP 给内联脚本的通行证，这里写死固定值，直接带上即可绕过。

直接把下面整段复制粘贴到输入框提交：

```
<script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(document.cookie)</script>
```

提交后页面渲染该标签，nonce 匹配 CSP，JS 成功执行弹窗。

---

## High（高级）⭐你打开的这个页面大概率是 High 难度

**CSP 策略**：`script‑src 'self'`，**只允许同源脚本，禁止内联 JS**。
页面表单输入框被移除，只能抓包修改 POST 参数`include`；
靶场自带同源 JSONP 接口：`source/jsonp.php?callback=xxx`，`callback`参数可控，会直接输出 `xxx({answer:15})`，相当于执行 xxx () 函数。

### 利用思路

`include`参数会把我们传入的 HTML 直接输出到页面；我们传入一个`<script src>`去加载本域名 jsonp.php，把 callback 写成恶意函数，因为是同源，CSP `script‑src 'self'`放行，实现执行 JS。