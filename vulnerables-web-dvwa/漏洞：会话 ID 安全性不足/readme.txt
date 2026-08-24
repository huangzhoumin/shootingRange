漏洞核心：自定义 Cookie `dvwaSession` 的生成算法可预测，攻击者可以猜测 / 推算出合法会话值，实现会话劫持。

>
> 注意：靶场必须先登录 DVWA 账号（admin/password），再进入该关卡。

## Low 级别

### 源码逻辑

每次点击`Generate`按钮，`dvwaSession`从 0 开始**数字自增 + 1**：1、2、3、4…… 完全可预测。

```
if (!isset ($_SESSION['last_session_id'])) {
    $_SESSION['last_session_id'] = 0;
}
$_SESSION['last_session_id']++;
setcookie("dvwaSession", $_SESSION['last_session_id']);
```

### 攻击步骤

1. 页面点击 **Generate**，F12→Application→Cookie，观察`dvwaSession`，每点一次数字 + 1。
2. 复制完整 Cookie：`dvwaSession=3; security=low; PHPSESSID=xxxx`
3. 清除浏览器全部 Cookie（模拟攻击者拿到别人 cookie）。
4. 修改 Cookie，手动设置`dvwaSession`为预测的数字，重新请求页面，即可复现会话劫持效果。

>
> Burp Suite 操作：抓包，修改 Cookie 里`dvwaSession`的值，发送 Repeater；也可以 Intruder 对 dvwaSession 做数字爆破。

## Medium 级别

### 源码逻辑

使用 PHP `time()`，**Unix 时间戳（秒）**作为 dvwaSession 的值，每秒 + 1，依旧可预测。

```
$cookie_value = time();
setcookie("dvwaSession", $cookie_value);
```

### 攻击步骤

1. 点击 Generate 抓包，拿到当前时间戳，例如`dvwaSession=1750000000`。
2. 时间戳是按秒递增，攻击者可以在这个时间窗口前后枚举一小段时间戳。
3. Burp Intruder，对`dvwaSession`做 payload，遍历前后几百秒的时间戳，尝试命中合法会话。

## High 级别

### 源码逻辑

自增数字做 MD5 哈希。底层还是自增数字，只是做 md5 加密，依然可以预测：数字 1、2、3，分别 md5 之后作为 cookie 值。

```
$_SESSION['last_session_id_high']++;
$cookie_value = md5($_SESSION['last_session_id_high']);
setcookie("dvwaSession", $cookie_value, time()+3600, "/vulnerabilities/weak_id/", $_SERVER['SERVER_NAME'], false, false);
```