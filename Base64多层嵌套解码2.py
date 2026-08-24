import requests

url = "http://6ec50a62-53a2-465f-b18b-185758e4516c.challenge.ctf.show"
headers = {
    "User-Agent": "ctf-show-brower"
}
data = {
    "username": "admin",
    "password": "#q7316"
}
resp = requests.post(url+"/check.php", headers=headers, data=data)
print(resp.text)