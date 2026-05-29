# -*- coding: utf-8 -*-
# @Time    : 2026.5.28
# @Author  : xlxlSakura
# @FileName: fuckHNU.py
# @Software: PyCharm
# @Description: Automatically FUCK the attendance system of HNU and CRACK the reg-token violently.
# @Version: 0.1

import execjs
import os
import time
import requests

privateKey = "00f661332f70969150a8ea126943958a914cc05abc7e3ad3d96570cc4fd01a9ce4"
serverUrl = "https://ktkq.hainanu.edu.cn/app"
os.environ["EXECJS_RUNTIME"] = "Node"
print(execjs.get().name)

os.environ["NODE_PATH"] = os.path.join(os.getcwd(), "node_modules")

def sm2_sign(msg_hex, priv_key_hex):
    with open("sm2_bridge.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)

    options = {
        "hash": True,
    }

    try:
        signature = ctx.call("sign", msg_hex, priv_key_hex, options)
        return signature
    except Exception as e:
        print(f"执行出错: {e}")
        return None


def sm2_valid(signature, priv_key,testmsg):
    with open("sm2_bridge.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)
    print(f"破解出的私钥: {priv_key}")
    pub_key = ctx.call("getPublicKey", priv_key)
    print(f"推导出的公钥: {pub_key}")

    test_msg = testmsg
    is_valid = ctx.call("verify", test_msg, signature, pub_key)
    print(f"验签结果: {is_valid}")

def send_post(apiurl,postpayload):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 26_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.73(0x18004935) NetType/WIFI Language/zh_CN",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wxa1e3abcd201139a2/35/page-frame.html"
    }
    try:
        response = requests.post(url=serverUrl + "/" + apiurl, data=postpayload, headers=headers, timeout=10)
        response.raise_for_status()
        print("请求成功！")
        print("返回结果:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"请求发送失败: {e}")

if __name__ == "__main__":
    timestamp = int(time.time() * 1000)
    sts = str(timestamp)
    sign = sm2_sign(sts, privateKey)
    sm2_valid(sign, privateKey, sts)
    print(f"SM2 签名结果: {sign}")

    # send_post("getQdKbList", pl_getQdKbList)