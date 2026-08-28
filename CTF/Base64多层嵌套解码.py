import base64

B64_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
correctPassword = "SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU="

def js_btoa(s: str) -> str:
    return base64.b64encode(s.encode("latin-1")).decode("ascii")

def js_atob(b64: str) -> str:
    return base64.b64decode(b64).decode("latin-1")

def encode_input(input_str: str) -> str:
    s1 = js_btoa(input_str)
    s2 = s1 + 'xH7jK'
    s3 = js_btoa(s2)
    s4 = s3[3:]
    s5 = s4[::-1]
    s6 = js_btoa(s5)
    s7 = 'aB3' + s6 + 'qW9'
    s8 = js_btoa(s7)
    s9 = s8[2:]
    final = js_btoa(s9)
    return final

def is_printable_ascii(s: str) -> bool:
    for ch in s:
        if not (32 <= ord(ch) <= 126):
            return False
    return True

def js_btoa_will_throw(s: str)->bool:
    """模拟判断：字符串丢入浏览器 btoa() 是否会抛出异常"""
    try:
        # JS btoa只允许0x00‑0xFF码点；Python latin‑1已经保证这点
        # JS不允许UTF‑16代理(0xD800‑0xDFFF)
        for c in s:
            cp = ord(c)
            if 0xD800 <= cp <=0xDFFF:
                return True
        js_btoa(s)
        return False
    except:
        return True


def solve_with_hard_constraint():
    s9 = js_atob(correctPassword)
    print(f"[+] s9 len={len(s9)}")
    found_equivalent = set()

    total_d = len(B64_CHARSET)**2
    for idx_d, D1 in enumerate(B64_CHARSET):
        for D2 in B64_CHARSET:
            current_d = idx_d * len(B64_CHARSET) + B64_CHARSET.index(D2)
            if current_d % 256 == 0:
                print(f"Progress D‑layer: {current_d}/{total_d}, found:{len(found_equivalent)}")

            s8_candidate = D1 + D2 + s9
            pad = (4 - len(s8_candidate) % 4) % 4
            s8_padded = s8_candidate + "=" * pad
            try:
                s7_candidate = js_atob(s8_padded)
            except Exception:
                continue

            if not (s7_candidate.startswith("aB3") and s7_candidate.endswith("qW9")):
                continue

            s6 = s7_candidate[3:-3]
            try:
                s5 = js_atob(s6)
            except Exception:
                continue
            s4 = s5[::-1]

            # ======================【关键约束】======================
            # JS真实环境： len(s4) = len(btoa(s2))‑3；btoa输出长度必为4倍数 → len(s4) mod4 == 1
            if len(s4) % 4 != 1:
                continue
            # ======================================================

            for C1 in B64_CHARSET:
                for C2 in B64_CHARSET:
                    for C3 in B64_CHARSET:
                        s3_candidate = C1 + C2 + C3 + s4
                        pad2 = (4 - len(s3_candidate) % 4) % 4
                        s3_padded = s3_candidate + "=" * pad2
                        try:
                            s2_candidate = js_atob(s3_padded)
                        except Exception:
                            continue
                        if not s2_candidate.endswith("xH7jK"):
                            continue

                        s1 = s2_candidate[:-5]
                        try:
                            plain = js_atob(s1)
                        except Exception:
                            continue

                        # 校验1：整体变换数学相等
                        if encode_input(plain) != correctPassword:
                            continue
                        # 校验2：过滤乱码
                        if not is_printable_ascii(plain):
                            continue
                        # 校验3：确保在浏览器JS调用btoa(plain)不会抛异常
                        if js_btoa_will_throw(plain):
                            continue

                        found_equivalent.add(plain)
                        print(f"\n[✅ JS‑runnable candidate] {repr(plain)}")

    return list(found_equivalent)


if __name__ == "__main__":
    res = solve_with_hard_constraint()
    if res:
        print("\n==== Valid candidates (JS运行不会报错，理论可以提交登录) ====")
        for p in res:
            print(repr(p))
    else:
        print("\nNo JS‑runnable printable candidate found.")