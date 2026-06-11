# -*- coding: utf-8 -*-
# @Time    : 2026-06-01
# @Author  : xlxlSakura
# @FileName: getStuInfo.py
# @Software: PyCharm
# @Description: 
# @Version: 1.0

import subprocess
import time
import winreg
import ctypes
import os
import logging
import sys
import signUtils
import fuckHNU

class MitmDebugger:
    def __init__(self, script_path=signUtils.resource_path("mitmProxy.py"), proxy_port="8080", up_port="0"):
        self.proxy_addr = f"127.0.0.1:{proxy_port}"
        self.script_path = script_path
        self.process = None
        self.is_running = True
        self.upload_port = up_port

    def set_system_proxy(self, enable=True):
        """配置 Windows 系统代理"""
        xpath = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, xpath, 0, winreg.KEY_WRITE)
            if enable:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, self.proxy_addr)
            else:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)

            # 刷新系统设置
            ctypes.windll.wininet.InternetSetOptionW(0, 39, 0, 0)
            ctypes.windll.wininet.InternetSetOptionW(0, 37, 0, 0)
            logging.info(f"系统代理状态: {'开启' if enable else '关闭'}")
        except Exception as e:
            logging.error(f"代理配置失败: {e}")

    def start_mitmproxy(self):
        """在后台启动 mitmdump"""
        if not os.path.exists(self.script_path):
            logging.error(f"错误: 找不到脚本 {self.script_path}")
            return False

        logging.info(f"[*] 正在启动 mitmdump (脚本: {self.script_path})...")

        env = os.environ.copy()
        env["FLASK_PORT"] = str(self.upload_port)
        # 使用 subprocess.Popen 异步启动
        exe_path = signUtils.resource_path("mitmdump.exe")
        if not os.path.exists(exe_path):
            logging.error(f"致命错误：找不到 {exe_path}")
            return
        self.process = subprocess.Popen(
            [exe_path,"-q", "-s", self.script_path, "-p", self.proxy_addr.split(":")[1]],
            stdout=sys.stdout,
            stderr=sys.stderr,
            env = env
        )
        # 等待代理启动完成
        time.sleep(3)
        return True

    def run(self):
        try:
            # 启动代理进程
            if self.start_mitmproxy():
                # 修改系统代理
                self.set_system_proxy(True)
                time.sleep(1)
                file_path = os.path.expandvars("%USERPROFILE%/.mitmproxy/mitmproxy-ca-cert.cer")
                if file_path:
                    command = f"certutil.exe -addstore root {file_path}"
                    os.system(command)
                    logging.info("环境检测完毕。现在可以打开微信小程序。")
                else:
                    logging.error("未找到证书。")
                logging.info("服务已就绪。正在拦截流量并输出 JSON...")

                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            logging.info("正在关闭服务...")
        finally:
            logging.debug("6")
            self.is_running = False
            self.cleanup()

    def cleanup(self):
        """清理资源，恢复系统设置"""
        self.set_system_proxy(False)
        if self.process:
            self.process.terminate()
            logging.info("Mitmproxy 进程已关闭")

def runProxy(upload_port):
    debugger = MitmDebugger(script_path=signUtils.resource_path("mitmProxy.py"), up_port=upload_port, proxy_port=fuckHNU.get_free_port())
    debugger.run()