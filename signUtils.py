# -*- coding: utf-8 -*-
# @Time    : 2026-05-29
# @Author  : xlxlSakura
# @FileName: signUtils.py
# @Software: PyCharm
# @Description: 国密SM2签名算法，通过js桥接来调用微信小程序库避免曲率和userID等差异导致签名校验不通过
# @Version: 0.1

import execjs
import os
import time
import sys
import logging

privateKey = "00f661332f70969150a8ea126943958a914cc05abc7e3ad3d96570cc4fd01a9ce4"

os.environ["EXECJS_RUNTIME"] = "Node"
os.environ["NODE_PATH"] = os.path.join(os.getcwd(), "node_modules")


# def get_node_runtime():
#     # 判断是否是 PyInstaller 打包后的环境
#     if hasattr(sys, '_MEIPASS'):
#         # 打包后的路径
#         node_modules_path = os.path.join(sys._MEIPASS, "node_modules")
#         os.environ["NODE_PATH"] = node_modules_path
#         node_path = os.path.join(sys._MEIPASS, "node", "node.exe")
#     else:
#
#         # 开发环境下的路径
#         node_path = os.path.join(os.path.abspath("."), "node", "node.exe")
#     print(f"正在尝试加载 Node: {node_path}")  # 调试用
#     print(f"该路径是否存在: {os.path.exists(node_path)}")
#     if not os.path.exists(node_path):
#         raise FileNotFoundError(f"找不到 Node 解释器: {node_path}")
#
#     # 强制 execjs 使用指定的 node 路径
#     return execjs.ExternalRuntime(
#         name='Node.js (Bundled)',
#         command=[node_path],
#         runner_source=execjs._runner_sources.Node
#     )

def init_node_env():
    if hasattr(sys, '_MEIPASS'):
        node_dir = os.path.join(sys._MEIPASS, "bin")
    else:
        node_dir = os.path.join(os.path.abspath("."), "bin")

    os.environ["PATH"] = node_dir + os.pathsep + os.environ["PATH"]

    return execjs.get("Node")

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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