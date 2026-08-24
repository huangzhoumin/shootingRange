页面目标：提交 `success`，但是**token 由前端 JS 计算生成**，直接填`success`提交，token 不对，返回 token 无效。

>
> 题目地址：`/vulnerabilities/javascript/`，页面提示 `Submit the word "success" to win`

## Low 级别

### 原理

页面 JS 把输入框内容反转，生成 token；提交表单携带 `phrase` 和 `token` 两个参数。
正常默认输入框是`ChangeMe`，token = `eMegnahC`（ChangeMe 反转）。
我们需要提交 `phrase=success`，对应的 token 是 `sseccus`（success 反转）。

### 操作步骤

1. 打开 BurpSuite 抓包，点击 Submit 提交一次，拿到原始 POST 包

```
POST /vulnerabilities/javascript/ HTTP/1.1
token=eMegnahC&phrase=ChangeMe&send=Submit
```

2. 修改参数：
`token=sseccus&phrase=success&send=Submit`
3. 发送改后的包 → `Well done!` 通关。

## Medium 级别

### 原理

JS 放到外部 js 文件，token 生成逻辑：`token = 反转( "XX" + phrase + "XX" )`。
phrase=success，则字符串拼接：`XXsuccessXX`，反转得到：`XXsseccusXX`。

### 操作

1. Burp 抓包，修改 POST 参数

```
token=XXsseccusXX&phrase=success&send=Submit
```

2. 发送数据包，完成通关。

## High 级别（最难）

### 原理

逻辑：

1. `token_part_1("ABCD",44)`：读取 phrase 值
2. 延时 300ms 执行 `token_part_2("XX")`：sha256 ("XX"+ 旧 token)
3. 点击 Submit 触发 `token_part_3()`：sha256 (token + "ZZ")，得到最终 token。
页面加载完会把 phrase 输入框清空，所以直接输入 success，JS 拿不到 success 的值来算 token。