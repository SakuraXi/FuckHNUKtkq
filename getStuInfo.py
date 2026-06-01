# -*- coding: utf-8 -*-
# @Time    : 2026-06-01
# @Author  : xlxlSakura
# @FileName: getStuInfo.py
# @Software: PyCharm
# @Description: 
# @Version: 1.0

import subprocess
import time
import webbrowser
import winreg
import ctypes
import os
import sys
import threading
from tkinter import filedialog, Tk
import signUtils


class MitmDebugger:
    def __init__(self, script_path="mitmProxy.py", proxy_port="8080", up_port="0"):
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
            print(f"[*] 系统代理状态: {'开启' if enable else '关闭'}")
        except Exception as e:
            print(f"[!] 代理配置失败: {e}")

    def start_mitmproxy(self):
        """在后台启动 mitmdump"""
        if not os.path.exists(self.script_path):
            print(f"[!] 错误: 找不到脚本 {self.script_path}")
            return False

        print(f"[*] 正在启动 mitmdump (脚本: {self.script_path})...")

        env = os.environ.copy()
        env["FLASK_PORT"] = str(self.upload_port)
        # 使用 subprocess.Popen 异步启动
        self.process = subprocess.Popen(
            ["mitmdump","-q", "-s", self.script_path, "-p", self.proxy_addr.split(":")[1]],
            stdout=sys.stdout,
            stderr=sys.stderr,
            env = env
        )
        # 等待代理启动完成
        time.sleep(3)
        return True

    def file_selector_and_exec(self):
        """控制台交互线程：按下回车后选择文件并执行命令"""
        print("[提示] 控制台随时按下 [Enter] 键可以选取cer文件并自动安装证书")
        done = False
        # 初始化一个隐藏的 Tkinter 窗口用于弹出对话框
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)  # 确保弹窗在最前面

        while not done:
            input()  # 等待回车
            print("[*] 正在打开文件选择器...")

            # 弹出选择文件对话框
            file_path = filedialog.askopenfilename(title="选择要处理的文件")

            if file_path:
                print(f"[*] 已选择文件: {file_path}")

                command = f"certutil.exe -addstore root {file_path}"

                print(f"[*] 执行命令: {command}")
                os.system(command)
                done = True
                print("\n[完成] 命令执行完毕。现在可以打开微信小程序。")
            else:
                print("[!] 未选择任何文件。")

    def open_cert_page(self):
        """引导用户安装证书"""
        print("[*] 正在打开证书下载页面 http://mitm.it ...")
        print("[!] 请在该页面下载对应系统的证书并手动完成安装/信任。")
        webbrowser.open("http://mitm.it")

    def run(self):
        try:
            # 启动代理进程
            if self.start_mitmproxy():
                # 修改系统代理
                self.set_system_proxy(True)
                # 引导安装证书 (仅需首次执行)
                self.open_cert_page()
                # 启动交互线程
                interaction_thread = threading.Thread(target=self.file_selector_and_exec, daemon=True)
                interaction_thread.start()
                print("\n[+] 服务已就绪。正在拦截流量并输出 JSON...")
                print("[+] 按下 Ctrl+C 停止服务并自动恢复系统代理设置。")

                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] 正在关闭服务...")
        finally:
            self.is_running = False
            self.cleanup()

    def cleanup(self):
        """清理资源，恢复系统设置"""
        self.set_system_proxy(False)
        if self.process:
            self.process.terminate()
            print("[*] Mitmproxy 进程已关闭")

def runProxy(upload_port):
    debugger = MitmDebugger(script_path=signUtils.resource_path("mitmProxy.py"), up_port=upload_port)
    debugger.run()