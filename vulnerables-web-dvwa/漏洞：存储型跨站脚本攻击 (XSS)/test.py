import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club"

COOKIES = {
    "PHPSESSID": "ldi9n0nspgemlhdv38su5o9dt3",
    "security": "low"
}

submit_url = f"{BASE_URL}/vulnerabilities/xss_s/"

def send_stored_xss(name_payload: str, msg_payload: str):
    data = {
        "txtName": name_payload,
        "txtMessage": msg_payload,
        "btnSign": "Sign Guestbook"
    }
    resp_post = requests.post(
        submit_url,
        data=data,
        cookies=COOKIES,
        verify=False,
        allow_redirects=False
    )
    print(f"POST状态码: {resp_post.status_code}")
    # --------调试：打印POST返回的前1000字符--------
    print("\n====POST响应HTML片段====")
    print(resp_post.text[:1000])

    resp_get = requests.get(submit_url, cookies=COOKIES, verify=False)

    print("\n===GET页面检测payload回显===")
    if name_payload in resp_get.text:
        print(f"[+] Name payload回显：{name_payload}")
    else:
        print(f"[-] Name payload被过滤：{name_payload}")

    if msg_payload in resp_get.text:
        print(f"[+] Message payload回显：{msg_payload}")
    else:
        print(f"[-] Message payload被过滤：{msg_payload}")

    if "&lt;script&gt;" not in resp_get.text and "<script>" in resp_get.text:
        print("[!] 检测到：标签原样输出，存在存储XSS漏洞")
    else:
        print("[*] 标签被转义/过滤，无风险")
    return resp_get


if __name__ == "__main__":
    print("\n=====测试1：普通文本入库 =====")
    send_stored_xss(name_payload="mytest001", msg_payload="hello_normal_msg_123456")
