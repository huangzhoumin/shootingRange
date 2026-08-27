垂直越权就是，用普通用户登入，然后使用管理员的权限
> 关卡：`vul/overpermission/op2/op2_login.php`
> 账号提示（点一下提示）：
> 
> 
> - 管理员高权限：`admin / 123456`（level=1，可以查看、新增、删除用户）
> - 普通低权限：`pikachu / 000000`（level=2，**只能看用户列表，不能增删用户**）

## 漏洞现象

`op2_admin_edit.php` 是管理员新增用户页面。
**这个页面只判断 “是否登录”，没有校验当前登录用户是不是管理员（level=1）**；只要登录过，不管是普通用户还是管理员，都可以访问并创建账号，实现低权限执行管理员功能，就是垂直越权。

## 方法一：浏览器直接访问（最简单，不用 BP）

1. 登录普通账号：`pikachu / 000000`，进入普通用户页面`op2_user.php`，页面只能查看会员，**没有 “添加用户” 按钮**。
2. 直接在浏览器地址栏输入管理员新增页面地址：

```
https://f0012fbf98204f57ae3bbf2cb76c8bce--8081.ap-shanghai2.cloudstudio.club/vul/overpermission/op2/op2_admin_edit.php
```

3. 回车，**普通 pikachu 会话下成功打开新增用户表单**，填入用户名密码，点【创建】。
4. 创建完成，再看用户列表，你刚刚新建的账号已经出现在数据库，越权成功。

> 
> ✨注意：删除功能页面`op2_admin.php`做了权限校验，普通用户访问会跳回登录页，只有**添加用户页面存在漏洞**。

## 方法二：Burp Suite 抓包复现（考试常用）

1. 登录 admin，进入添加用户页面，填写信息，提交，BP 抓到 POST 数据包，发送到 Repeater。
2. 退出 admin，登录普通用户`pikachu/000000`，复制 pikachu 的`PHPSESSID` Cookie。
3. 在 Repeater 中，把数据包 Cookie 替换成 pikachu 的 session，发送请求。
4. 响应成功，用户被创建。证明普通用户的会话可以调用管理员新增接口。

## 源码解析（漏洞根源）

**op2_admin_edit.php（有漏洞页面）**

```
//只判断是否登录，完全不校验权限等级level
if(!check_op2_login($link)){
    header("location:op2_login.php");
    exit();
}
//缺失：if($_SESSION['op2']['level']!=1)  管理员权限校验
```

**op2_admin.php（删除页面，写了正确校验做对比）**

```
//同时校验登录 + 必须是管理员level=1
if(!check_op2_login($link) || $_SESSION['op2']['level']!=1){
    header("location:op2_login.php");
    exit();
}
```

> 
> 对比可见：删除功能做了角色校验；新增用户页面漏掉角色校验，只检查登录状态，造成垂直越权。

## 修复方案

1. 所有管理员接口 / 页面，除了判断登录，**必须校验 session 中用户角色 / 权限等级**；非管理员直接跳转登录或者 403 拒绝访问。

```
//修复示例
if(!check_op2_login($link) || $_SESSION['op2']['level'] != 1){
    header("location:op2_login.php");
    exit;
}
```

2. 后端不能只靠前端隐藏按钮做权限控制；前端隐藏按钮，但是 URL / 接口仍然可以直接访问，必须后端鉴权。

## 水平越权 (op1) vs 垂直越权 (op2)

表格

| 类型 | 场景 | 例子 |
| --- | --- | --- |
| 水平越权（op1） | **相同权限等级** | lucy 看 lili 的数据，平级之间偷看别人数据 |
| 垂直越权（op2） | **不同权限等级** | 普通用户 pikachu 执行管理员新增账号功能，下级做上级的操作 |


# =============
实操
先登入admin账户，进入添加用户页面，保存url地址
然后退出登入，再登入pikachu账户。此时如果再访问添加用户的界面，就可以发现pikachu用户可以新增用户了（之前的页面没展示这个选项，需要直接从url进去）


