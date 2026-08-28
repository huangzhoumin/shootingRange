先使用访客用户guest登入后，观察到返回头里面设置了
Set-Cookie: role=guest; expires=Thu, 27-Aug-2026 08:40:04 GMT; Max-Age=3600
则可以将 role=guest;  设置在cookie里面，使用burp重新发送请求，即可完成cookie伪造，拿到CTF
![img.png](img.png)