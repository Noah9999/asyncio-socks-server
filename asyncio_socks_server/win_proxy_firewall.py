import subprocess, time
from asyncio_socks_server.__version__ import __version__
from asyncio_socks_server.app import SocksServer
from asyncio_socks_server.config import BASE_LOGO, SOCKS_SERVER_PREFIX, Config
from asyncio_socks_server.logger import logger

rule_name = "SOCKS5 Proxy"

def add_firewall_rule(rule_name, port, protocol="TCP"):
    """添加防火墙规则"""
    logger.info(f'防火墙执行添加规则')
    command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol={protocol} localport={port}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True,encoding='utf-8',)
    return result.returncode == 0

def delete_firewall_rule(rule_name, direction="in"):
    """删除防火墙规则"""
    logger.info(f'防火墙执行删除规则')
    time.sleep(1)
    command = f'netsh advfirewall firewall delete rule name="{rule_name}" dir={direction}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True,encoding='utf-8',)
    return result.returncode == 0

def main():
    app = SocksServer()
    
    try:
        assert add_firewall_rule(rule_name, app.config.LISTEN_PORT), '开启防火墙端口失败'
        app.run()
    except Exception as e:
        logger.error(f'run error {e}')
        time.sleep(5)


import ctypes
# 定义Windows API
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
PHANDLER_ROUTINE = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_uint)

def _handler(ctrl_type):
    """控制台事件处理函数"""
    delete_firewall_rule(rule_name)
    kernel32.ExitProcess(0)  # 确保退出
    return 0  # 允许其他处理程序

# 注册处理程序
handler = PHANDLER_ROUTINE(_handler)
kernel32.SetConsoleCtrlHandler(handler, True)


if __name__ == "__main__":
    main()
