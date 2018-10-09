"""
这个模块是更改代理模式的，有如下三种：
直连模式、PAC模式、全局模式

1 直连模式: 更改注册表，去掉IE代理
2 PAC模式: 更改privoxy下的pac.action 内容替换为 PAC_list 设置IE代理
3 全局模式: 更改privoxy下的pac.action 内容替换为 /   设置IE代理
"""

from requests import get
from base64 import b64decode
import winreg
from os import path


#更新gfwlist 调用即可将gfw拦截的域名更新至最新，写入privoxy文件夹下的gfwlist文件中
def get_gfwlist():
    url_list = ['https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt','https://pagure.io/gfwlist/raw/master/f/gfwlist.txt',
                'https://bitbucket.org/gfwlist/gfwlist/raw/HEAD/gfwlist.txt','https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt',
                'https://repo.or.cz/gfwlist.git/blob_plain/HEAD:/gfwlist.txt','https://git.tuxfamily.org/gfwlist/gfwlist.git/plain/gfwlist.txt']
    err_count=0
    for url in url_list:
        try:
            gfw_list = get(url)

            break
        except:
            pass
            err_count+=1

    if err_count < len(url_list):
        open('./privoxy/gfwlist', 'wb').write(b64decode(gfw_list.content))
    else:
        return 'Network Error'

#修改注册表，传入参数
def set_proxy(enable,proxy_ip):
    path = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_WRITE)
    winreg.SetValueEx(key,'ProxyEnable',0,winreg.REG_DWORD,enable)
    winreg.SetValueEx(key,'ProxyServer',0,winreg.REG_SZ,proxy_ip)


def enable_IEproxy():
    set_proxy(1,'127.0.0.1:1080')

def disable_IEproxy():
    set_proxy(0,'')

#直连模式
def direct_mode():
    disable_IEproxy()

#PAC模式
def pac_mode():
    if path.exists('./privoxy/gfwlist'):
        f_lines = open('./privoxy/gfwlist','r').readlines()
        open('./privoxy/pac.action','w').write('+forward-override{forward-socks5 127.0.0.1:1081 .}}')
        for f in f_lines:
            open('./privoxy/pac.action','a').write(f+'\n')
    else:
        get_gfwlist()
        pac_mode()

    enable_IEproxy()

#全局模式
def all_mode():
    open('./privoxy/pac.action','w').write('{+forward-override{forward-socks5 127.0.0.1:1081 .}}\n /')
    enable_IEproxy()

