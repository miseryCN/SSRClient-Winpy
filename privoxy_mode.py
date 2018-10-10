"""
这个模块是更改代理模式的，有如下三种：
直连模式、PAC模式、全局模式
1 直连模式: 更改注册表，关闭所有代理
2 PAC模式: 设置自动配置脚本，获得路径
3 全局模式: 设置代理服务器，转发所有请求
"""
from time import sleep
from requests import get
from base64 import b64decode
from os import path,popen,remove,getcwd


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


# 修改注册表，传入参数
'''
def set_proxy(enable, proxy_ip):
    path = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, enable)
    winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, proxy_ip)
'''


#更新生成pac文件
def switch_gfwlist():
    g_lines = open('./privoxy/gfwlist','r').readlines()
    g_all = 'var direct = "__DIRECT__";if (direct == "__DIR" + "ECT__") direct = "DIRECT;";var wall_proxy = function(){ return "__PROXY__"; };var wall_v6_proxy = function(){ return "__PROXY__"; };var nowall_proxy = function(){ return direct; };var ip_proxy = function(){ return nowall_proxy(); };var ipv6_proxy = function(){ return nowall_proxy(); };var rules = [\n'
    for g in g_lines:
        if g[0] != '!' and g != '\n' and g[0] != '[':
            g = '\t\"'+g.replace('\n','\",')+'\n'
            g_all += g
    g_all = g_all + '];\n'+open('./privoxy/pacpart','r').read()
    open('./pac','w').write(g_all)



#修改代理模式，自动生成注册表  参考:https://www.jianshu.com/p/49c444d9a435
def set_proxy(proxy_mode):
    settings = 'Windows Registry Editor Version 5.00\n[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections]\n\"DefaultConnectionSettings\"=hex:'
    proxySwitchValue = '46,00,00,00,d2,06,00,00,01,00,00,00,0e,00,00,00,31,32,37,2e,30,2e,30,2e,31,3a,31,30,38,30,'
    fileteLocalValue = 'bf,00,00,00,6c,6f,63,61,6c,68,6f,73,74,3b,31,32,37,2e,2a,3b,31,30,2e,2a,3b,31,37,32,2e,31,36,2e,2a,3b,31,37,32,2e,31,37,2e,2a,3b,31,37,32,2e,31,38,2e,2a,3b,31,37,32,2e,31,39,2e,2a,3b,31,37,32,2e,32,30,2e,2a,3b,31,37,32,2e,32,31,2e,2a,3b,31,37,32,2e,32,32,2e,2a,3b,31,37,32,2e,32,33,2e,2a,3b,31,37,32,2e,32,34,2e,2a,3b,31,37,32,2e,32,35,2e,2a,3b,31,37,32,2e,32,36,2e,2a,3b,31,37,32,2e,32,37,2e,2a,3b,31,37,32,2e,32,38,2e,2a,3b,31,37,32,2e,32,39,2e,2a,3b,31,37,32,2e,33,30,2e,2a,3b,31,37,32,2e,33,31,2e,2a,3b,31,37,32,2e,33,32,2e,2a,3b,31,39,32,2e,31,36,38,2e,2a,3b,3c,6c,6f,63,61,6c,3e,48,'
    if proxy_mode == 'pac':
        pac_path = getcwd()+'\\pac'
        pacValue = '00,00,00,'
        for p in pac_path:
            pacValue += format(ord(p),'x')+','
        proxySwitchValue = proxySwitchValue.replace('01','07')
        reg_value = settings + proxySwitchValue + fileteLocalValue + pacValue
    elif proxy_mode == 'all':
        proxySwitchValue = proxySwitchValue.replace('01','03')
        reg_value = settings+proxySwitchValue+fileteLocalValue
    else:
        reg_value = settings + proxySwitchValue

    open('./tmp.reg','w').write(reg_value)
    popen('reg import ./tmp.reg')
    sleep(0.5)
    remove('./tmp.reg')


# 直连模式
def direct_mode():
    set_proxy('direct')


# PAC模式
def pac_mode():
    if path.exists('./pac'):
        set_proxy('pac')
    else:
        get_gfwlist()
        switch_gfwlist()
        pac_mode()


# 全局模式
def all_mode():
    set_proxy('all')