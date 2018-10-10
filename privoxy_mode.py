"""
这个模块是更改代理模式的，有如下三种：
直连模式、PAC模式、全局模式
1 直连模式: 更改注册表，关闭所有代理
2 PAC模式: 设置自动配置脚本，获得路径
3 全局模式: 设置代理服务器，转发所有请求
"""
from time import sleep
from requests import get
from os import path,popen,remove
import win32gui
import win32con
import win32api

#直接获取gfwlist,无需转换 6小时更新一次
def updateGfwList():
    IEProxy('disable')
    url = 'https://zfl9.github.io/gfwlist2privoxy/gfwlist.action'
    open('./privoxy/pac.action','wb').write(get(url).content)


'''
# 更新gfwlist 调用即可将gfw拦截的域名更新至最新，写入privoxy文件夹下的gfwlist文件中
def get_gfwlist():
    url_list = ['https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt',
                'https://pagure.io/gfwlist/raw/master/f/gfwlist.txt',
                'https://bitbucket.org/gfwlist/gfwlist/raw/HEAD/gfwlist.txt',
                'https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt',
                'https://repo.or.cz/gfwlist.git/blob_plain/HEAD:/gfwlist.txt',
                'https://git.tuxfamily.org/gfwlist/gfwlist.git/plain/gfwlist.txt']
    err_count = 0
    for url in url_list:
        try:
            gfw_list = get(url)

            break
        except:
            pass
            err_count += 1
    if err_count < len(url_list):
        open('./privoxy/gfwlist', 'wb').write(b64decode(gfw_list.content))
        return 'Success'
    else:
        return 'Network Error'


# 修改注册表，传入参数(此方法不可用)

def set_proxy(enable, proxy_ip):
    path = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, enable)
    winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, proxy_ip)
'''

#逗比专用模块（退出）/后期会改
def exit_privoxy():
    win_title = 'Privoxy'
    wnd = win32gui.FindWindow(None, win_title)
    win32gui.SendMessage(wnd, win32con.WM_CLOSE)


#仅供娱乐，关闭到任务栏/后期会改
def close_privoxy():
    win_title = 'Privoxy'
    wnd = win32gui.FindWindow(None, win_title)
    left, top, right, bottom = win32gui.GetWindowRect(wnd)
    right = right - 25
    top = top + 25
    win32api.SetCursorPos([right, top])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0)


#是否启用IE代理，地址为 127.0.0.1:1080 写入注册表。参考:https://www.jianshu.com/p/49c444d9a435
def IEProxy(enable):
    settings = 'Windows Registry Editor Version 5.00\n[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections]\n\"DefaultConnectionSettings\"=hex:'
    proxySwitchValue = '46,00,00,00,d2,06,00,00,01,00,00,00,0e,00,00,00,31,32,37,2e,30,2e,30,2e,31,3a,31,30,38,31,'
    fileteLocalValue = 'bf,00,00,00,6c,6f,63,61,6c,68,6f,73,74,3b,31,32,37,2e,2a,3b,31,30,2e,2a,3b,31,37,32,2e,31,36,2e,2a,3b,31,37,32,2e,31,37,2e,2a,3b,31,37,32,2e,31,38,2e,2a,3b,31,37,32,2e,31,39,2e,2a,3b,31,37,32,2e,32,30,2e,2a,3b,31,37,32,2e,32,31,2e,2a,3b,31,37,32,2e,32,32,2e,2a,3b,31,37,32,2e,32,33,2e,2a,3b,31,37,32,2e,32,34,2e,2a,3b,31,37,32,2e,32,35,2e,2a,3b,31,37,32,2e,32,36,2e,2a,3b,31,37,32,2e,32,37,2e,2a,3b,31,37,32,2e,32,38,2e,2a,3b,31,37,32,2e,32,39,2e,2a,3b,31,37,32,2e,33,30,2e,2a,3b,31,37,32,2e,33,31,2e,2a,3b,31,37,32,2e,33,32,2e,2a,3b,31,39,32,2e,31,36,38,2e,2a,3b,3c,6c,6f,63,61,6c,3e,48,'
    if enable == 'enable':
        proxySwitchValue = proxySwitchValue.replace('01','03')
        reg_value = settings+proxySwitchValue+fileteLocalValue
    elif enable == 'disable':
        reg_value = settings+proxySwitchValue+fileteLocalValue
    open('./tmp.reg','w').write(reg_value)
    popen('reg import ./tmp.reg')
    sleep(0.5)
    remove('./tmp.reg')




# 直连模式
def direct_mode():
    IEProxy('disable')


# PAC模式
def pac_mode():
    if path.exists('./privoxy/pac.action'):
        f = open('./privoxy/config.txt', 'r').read()
        f = f.replace('forward-socks5 / 127.0.0.1:1080 .','actionsfile pac.action')
        open('./privoxy/config.txt', 'w').write(f)
        IEProxy('enable')
        exit_privoxy()
        sleep(0.3)
        popen('cd privoxy && privoxy.exe')
        sleep(0.5)
        close_privoxy()

    else:
        updateGfwList()
        pac_mode()


# 全局模式
def all_mode():
    f = open('./privoxy/config.txt','r').read()
    f = f.replace('actionsfile pac.action','forward-socks5 / 127.0.0.1:1080 .')
    open('./privoxy/config.txt','w').write(f)
    IEProxy('enable')
    exit_privoxy()
    sleep(0.3)
    popen('cd privoxy && privoxy.exe')
    sleep(0.5)
    close_privoxy()

pac_mode()
