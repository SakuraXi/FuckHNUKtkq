# -*- coding: utf-8 -*-
# @Time    : 2026-05-29
# @Author  : xlxlSakura
# @FileName: signUtils.py
# @Software: PyCharm
# @Description: 国密SM2签名算法，通过js桥接来调用微信小程序库避免曲率和userID等差异导致签名校验不通过
# @Version: 0.1

import subprocess
import sys

if sys.platform.startswith('win'):
    class SafePopen(subprocess.Popen):
        def __init__(self, *args, **kwargs):
            if 'creationflags' not in kwargs:
                kwargs['creationflags'] = 0x08000000
            super().__init__(*args, **kwargs)
    subprocess.Popen = SafePopen

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

import os
import time
import logging
import execjs

privateKey = "00f661332f70969150a8ea126943958a914cc05abc7e3ad3d96570cc4fd01a9ce4"

os.environ["EXECJS_RUNTIME"] = "Node"
os.environ["NODE_PATH"] = os.path.join(os.getcwd(), "node_modules")

def init_node_env():
    if hasattr(sys, '_MEIPASS'):
        node_dir = os.path.join(sys._MEIPASS, "bin")
    else:
        node_dir = os.path.join(os.path.abspath("."), "bin")

    os.environ["PATH"] = node_dir + os.pathsep + os.environ["PATH"]

    return execjs.get("Node")

def sm2_sign(msg_hex, priv_key_hex):
    init_node_env()
    with open(resource_path("sm2_bridge.js"), "r", encoding="utf-8") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    try:
        signature = ctx.call("sign", msg_hex, priv_key_hex, {"hash": True,})
        return signature
    except Exception as e:
        logging.error(f"执行出错: {e}")
        return None

def sm2_valid(signature, priv_key, testmsg):
    init_node_env()
    with open(resource_path("sm2_bridge.js"), "r", encoding="utf-8") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    pub_key = ctx.call("getPublicKey", priv_key)
    test_msg = testmsg
    is_valid = ctx.call("verify", test_msg, signature, pub_key)
    logging.info(f"验签结果: {is_valid}")

def getSignAndTimestamp():
    timestamp = int(time.time() * 1000)
    sign = sm2_sign(str(timestamp), privateKey)
    return [sign, str(timestamp)]