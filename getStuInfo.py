# -*- coding: utf-8 -*-
# @Time    : 2026-07-03
# @Author  : xlxlSakura
# @FileName: getStuInfo.py
# @Description: 启动进程内 mitmproxy 代理抓包，拦截目标响应后通过回调直接处理
# @Version: 2.0

import logging
import threading

import proxy_capture
import fuckHNU


def runProxy(callback):
    """
    启动代理抓包，阻塞直到抓到数据或超时。

    在独立线程中调用 (由 /add_user 端点启动)。

    Args:
        callback: 抓到目标响应后的回调函数 callback(data: bytes)
                  data 是 HTTP 响应体的原始字节 (JSON 格式)
    """
    # 用 Event 实现"抓到数据后自动停止代理"
    capture_done = threading.Event()

    def wrapped_callback(data):
        """包装回调: 执行完后通知 runProxy 可以停止代理了"""
        try:
            callback(data)
        finally:
            capture_done.set()

    # 自动选择空闲端口
    proxy_port = fuckHNU.get_free_port()

    # 创建并启动进程内代理
    proxy = proxy_capture.InProcessProxy(
        callback=wrapped_callback,
        proxy_port=proxy_port
    )

    if not proxy.start():
        logging.error("代理启动失败，抓包中止")
        if fuckHNU.main_window:
            fuckHNU.main_window.evaluate_js(
                "showResult('error', '启动失败', '代理启动失败，请检查 mitmproxy 是否正确安装')"
            )
        return

    logging.info("抓包环境已就绪，等待目标请求...")

    # 阻塞等待: 直到回调执行完毕 (抓到数据) 或超时 (3分钟)
    capture_done.wait(timeout=180)

    # 清理: 关闭代理、恢复系统代理设置
    proxy.stop()
    logging.info("抓包流程结束")
