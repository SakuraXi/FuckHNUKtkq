# -*- coding: utf-8 -*-
# @Time    : 2026-06-01
# @Author  : xlxlSakura
# @FileName: mitmProxy.py
# @Software: PyCharm
# @Description: 
# @Version: 1.0
import logging

from mitmproxy import http
import requests
import os

flask_port = os.getenv("FLASK_PORT", "5000")
TARGET_URL_KEYWORD = "ktkq.hainanu.edu.cn/app/getUserOpenId"

def response(flow: http.HTTPFlow):
    if TARGET_URL_KEYWORD in flow.request.url:
        logging.info(f"\n[+] 发现目标请求: {flow.request.url}")
        try:
            data = flow.response.json()
            requests.post(f"http://127.0.0.1:{flask_port}/upload", json=data)
        except Exception as e:
            logging.error(f"[-] 解析失败: {e}")