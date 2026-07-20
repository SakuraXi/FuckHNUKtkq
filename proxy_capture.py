# -*- coding: utf-8 -*-
# @Time    : 2026-07-03
# @Author  : xlxlSakura
# @FileName: proxy_capture.py
# @Description: 进程内 mitmproxy 抓包模块
# @Version: 2.0

import asyncio
import ctypes
import logging
import os
import socket
import subprocess
import sys
import threading
import time

if sys.platform.startswith('win'):
    import winreg

_mitmproxy_loaded = False
_mitmproxy_options = None
_mitmproxy_DumpMaster = None

def _ensure_mitmproxy():
    """懒加载 mitmproxy 核心组件"""
    global _mitmproxy_loaded, _mitmproxy_options, _mitmproxy_DumpMaster
    if _mitmproxy_loaded:
        return
    try:
        from mitmproxy import options as _opts
        from mitmproxy.tools.dump import DumpMaster as _DM
        _mitmproxy_options = _opts
        _mitmproxy_DumpMaster = _DM
        _mitmproxy_loaded = True
    except ImportError as e:
        raise ImportError(
            f"mitmproxy 未安装，无法启动抓包代理。请运行: pip install mitmproxy\n"
            f"原始错误: {e}"
        )

TARGET_URL_KEYWORD = "ktkq.hainanu.edu.cn/app/getUserOpenId"

_CONFDIR = os.path.join(
    os.path.expandvars(r"%APPDATA%\FuckHNUktkq"),
    "mitmproxy_conf"
)

class CaptureAddon:
    """
    mitmproxy 插件: 拦截包含目标 URL 的 HTTP 响应，
    将响应体原始字节通过回调函数传回调用方。
    """

    def __init__(self, callback):
        """
        Args:
            callback: 回调函数，签名为 callback(data: bytes)
                      在独立线程中调用，不会阻塞代理事件循环
        """
        self.callback = callback

    def response(self, flow):
        try:
            if TARGET_URL_KEYWORD in flow.request.url:
                print("found")
                logging.info(f"发现目标请求: {flow.request.url}")
                data = flow.response.content  # bytes
                print(data)
                # 在独立线程中执行回调，避免阻塞 mitmproxy 的 asyncio 事件循环
                threading.Thread(
                    target=self._safe_callback,
                    args=(data,),
                    daemon=True
                ).start()
        except Exception as e:
            logging.error(f"拦截处理失败: {e}")

    def _safe_callback(self, data):
        """安全执行回调，捕获所有异常"""
        try:
            if self.callback:
                self.callback(data)
        except Exception as e:
            logging.error(f"回调执行失败: {e}")

class CertManager:
    """
    管理 mitmproxy CA 证书的自动安装与卸载。

    使用 certutil -user -addstore Root 将证书安装到
    "当前用户 > 受信任的根证书颁发机构" 存储，
    不需要管理员权限/UAC 提权。
    """

    # mitmproxy 首次启动后在此目录生成 CA 证书
    CA_CERT_CER = os.path.join(_CONFDIR, "mitmproxy-ca-cert.cer")

    @staticmethod
    def is_cert_installed():
        """检查 mitmproxy CA 证书是否已在当前用户的受信任根证书存储中"""
        try:
            result = subprocess.run(
                ["certutil", "-user", "-store", "Root", "mitmproxy"],
                capture_output=True, text=True, timeout=5
            )
            return "mitmproxy" in result.stdout and "CERTIFICATE" in result.stdout
        except Exception:
            return False

    @staticmethod
    def install_cert():
        """
        将 mitmproxy CA 证书安装到当前用户的受信任根证书存储。
        不需要管理员权限。
        Returns: True 表示成功
        """
        if not os.path.exists(CertManager.CA_CERT_CER):
            logging.warning(f"CA 证书文件不存在: {CertManager.CA_CERT_CER}")
            logging.warning("请确保 mitmproxy 已至少启动过一次以生成证书")
            return False

        try:
            result = subprocess.run(
                ["certutil", "-user", "-addstore", "Root", CertManager.CA_CERT_CER],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                logging.info("CA 证书已自动安装到当前用户受信任根证书存储")
                return True
            else:
                logging.error(f"CA 证书安装失败 (exit={result.returncode}): {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"CA 证书安装异常: {e}")
            return False

    @staticmethod
    def uninstall_cert():
        """从当前用户的受信任根证书存储中移除 mitmproxy CA 证书"""
        try:
            subprocess.run(
                ["certutil", "-user", "-delstore", "Root", "mitmproxy"],
                capture_output=True, timeout=5
            )
            logging.info("CA 证书已从受信任根证书存储移除")
        except Exception:
            pass

class InProcessProxy:
    """
    在进程内运行 mitmproxy

    代理在独立线程中运行，拥有自己的 asyncio 事件循环，
    不影响主线程的 webview/bottle 事件循环。
    """

    def __init__(self, callback, proxy_port=None):
        """
        Args:
            callback: 抓到目标响应后的回调函数 callback(data: bytes)
            proxy_port: 代理监听端口，None 则自动选择空闲端口
        """
        self.callback = callback
        self.proxy_port = proxy_port or self._get_free_port()
        self._master = None
        self._thread = None
        self._loop = None
        self._ready = threading.Event()
        self._started = False

    @staticmethod
    def _get_free_port():
        """获取一个可用的空闲端口"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def set_system_proxy(self, enable=True):
        """开启/关闭 Windows 系统代理，指向本代理端口"""
        xpath = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, xpath, 0, winreg.KEY_WRITE)
            if enable:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ,
                                  f"127.0.0.1:{self.proxy_port}")
            else:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)

            # 通知系统代理设置已变更
            ctypes.windll.wininet.InternetSetOptionW(0, 39, 0, 0)
            ctypes.windll.wininet.InternetSetOptionW(0, 37, 0, 0)

            status = f"开启 (127.0.0.1:{self.proxy_port})" if enable else "关闭"
            logging.info(f"系统代理: {status}")
        except Exception as e:
            logging.error(f"代理配置失败: {e}")

    def _run_proxy_thread(self):
        """代理线程目标函数: 在独立线程中运行 mitmproxy 的 asyncio 事件循环"""

        # 确保 confdir 存在
        os.makedirs(_CONFDIR, exist_ok=True)

        # 懒加载 mitmproxy
        try:
            _ensure_mitmproxy()
        except ImportError as e:
            logging.error(str(e))
            self._ready.set()
            return

        # 使用 SelectorEventLoop，避免 ProactorEventLoop 的兼容性问题
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        async def _main():
            opts = _mitmproxy_options.Options(
                listen_host='127.0.0.1',
                listen_port=self.proxy_port,
                confdir=_CONFDIR,
                ssl_insecure=True,
            )

            try:
                self._master = _mitmproxy_DumpMaster(
                    opts,
                    with_termlog=False,
                    with_dumper=False
                )
            except TypeError:
                # 兼容旧版本 mitmproxy
                self._master = _mitmproxy_DumpMaster(opts)

            self._master.addons.add(CaptureAddon(self.callback))

            # 通知主线程
            self._ready.set()

            try:
                await self._master.run()
            except Exception as e:
                logging.error(f"代理运行异常: {e}")
            finally:
                self._ready.set()

        try:
            self._loop.run_until_complete(_main())
        except Exception as e:
            logging.error(f"代理线程异常: {e}")
            self._ready.set()
        finally:
            if self._loop and not self._loop.is_closed():
                self._loop.close()

    def start(self):
        """
        启动代理: 启动线程 -> 等待就绪 -> 安装CA证书 -> 设置系统代理
        Returns: True 表示成功
        """
        # 启动代理线程 (首次启动会自动生成 CA 证书)
        self._thread = threading.Thread(target=self._run_proxy_thread, daemon=True)
        self._thread.start()

        # 等待代理就绪
        if not self._ready.wait(timeout=15):
            logging.error("代理启动超时")
            return False

        if self._master is None:
            logging.error("代理启动失败 (mitmproxy 未加载)")
            return False

        # 等待 CA 证书文件生成
        for _ in range(10):
            if os.path.exists(CertManager.CA_CERT_CER):
                break
            time.sleep(0.5)

        # 自动安装 CA 证书
        if not CertManager.is_cert_installed():
            logging.info("正在自动安装 mitmproxy CA 证书...")
            CertManager.install_cert()
            time.sleep(0.5)
        else:
            logging.info("CA 证书已安装，跳过")

        # 设置系统代理
        self.set_system_proxy(True)
        time.sleep(0.5)

        self._started = True
        logging.info(f"代理已就绪，监听端口: {self.proxy_port}")
        return True

    def stop(self):
        """停止代理: 关闭系统代理 -> 停止 mitmproxy -> 等待线程结束"""
        self.set_system_proxy(False)

        if self._master and self._loop:
            try:
                if self._loop.is_running():
                    # 异步关闭: 在代理的事件循环中调度 shutdown
                    if asyncio.iscoroutinefunction(self._master.shutdown):
                        asyncio.run_coroutine_threadsafe(
                            self._master.shutdown(),
                            self._loop
                        ).result(timeout=5)
                    else:
                        # 兼容 shutdown 不是协程的情况
                        self._loop.call_soon_threadsafe(self._master.shutdown)
            except Exception as e:
                logging.error(f"关闭代理异常: {e}")
                # 强制停止事件循环
                try:
                    self._loop.call_soon_threadsafe(self._loop.stop)
                except Exception:
                    pass

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)

        self._started = False
        logging.info("代理已停止")

def start_capture(callback, proxy_port=None):
    """
    启动 MITM 代理抓包。

    Args:
        callback: 抓到目标响应后的回调函数，签名为 callback(data: bytes)
                  data 是 HTTP 响应体的原始字节
        proxy_port: 代理监听端口，None 则自动选择

    Returns:
        InProcessProxy 实例 (调用 .stop() 清理资源)，
        启动失败返回 None
    """
    proxy = InProcessProxy(callback, proxy_port)
    if proxy.start():
        return proxy
    return None
