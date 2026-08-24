import requests

url = "http://7fd25cd5-f7b3-43bc-8234-be1e3790b4a1.challenge.ctf.show"
headers = {
    "User-Agent": "ctf-show-brower"
}
data = {
    "username": "admin",
    "password": "CTF{easy_base64}"
}
resp = requests.post(url+"/check.php", headers=headers, data=data)
print(resp.text)