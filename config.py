'''
这个文件是用来从网站获取个人连接数据的
流程如下:
1. 通过ssrpanel的登录API获取账号信息
2. 通过账号信息内的订阅链接获取服务器，连接信息
'''
from requests import get
from json import loads
from datetime import datetime
from base64 import b64decode


# 对流量进行计算,取不同单位
def transfer_calculate(transfer):
    if transfer < 1024 and transfer >= 0:
        return str(transfer) + 'B'
    elif transfer >= 1024 and transfer < 1024 ** 2:
        transfer = round(transfer / 1024, 2)
        return str(transfer) + 'KB'
    elif transfer >= 1024 ** 2 and transfer < 1024 ** 3:
        transfer = round(transfer / 1024 / 1024, 2)
        return str(transfer) + 'MB'
    elif transfer >= 1024 ** 3 and transfer < 1024 ** 4:
        transfer = round(transfer / 1024 / 1024 / 1024, 2)
        return str(transfer) + 'GB'
    elif transfer >= 1024 ** 4:
        transfer = round(transfer / 1024 / 1024 / 1024 / 1024, 2)
        return str(transfer) + 'TB'
    else:
        return '0B'


# 字符串的b64解码
def str_bdecode(string):
    if len(string) % 4:
        string += '=' * (4 - len(string) % 4)
    string = str(b64decode(string), encoding='utf-8')
    return string


# 订阅链接解析
def subscribe_link(link):
    link_response = get(link).text
    response_decode = str_bdecode(link_response)
    ssr_links = response_decode.replace('ssr://', '').splitlines()
    conn_info = {}
    for ssr_link in ssr_links:
        #try:
        single_info = str_bdecode(ssr_link).replace('eXV4aWFvd2VpMTk5NA/?', '').split(':')
        #except:
         #   return 'no server to use'
        single_param = single_info[5].split('&')
        obfs_param = str_bdecode(single_param[0].replace('obfsparam=', ''))
        proto_param = str_bdecode(single_param[1].replace('protoparam=', ''))
        remarks = str_bdecode(single_param[2].replace('remarks=', ''))
        group = str_bdecode(single_param[3].replace('group=', ''))
        remarks_dic = {
            'address': single_info[0],
            'port': single_info[1],
            'protocol': single_info[2],
            'method': single_info[3],
            'obfs': single_info[4],
            'proto_param': proto_param,
            'obfs_param': obfs_param,
            'group': group
        }
        conn_info[remarks] = remarks_dic

    return conn_info  # 返回一个嵌套字典


def api_login():
    username = str(input('输入你的用户名:'))
    password = str(input('输入你的密码:'))
    login_url = 'https://vpn.xiaoweigod.com/api/login'
    login_data = {
        'username': username,
        'password': password
    }

    try:
        login_response = get(login_url, login_data).text
    except ConnectionError:
        return 'connect error'
    login_info = loads(login_response)
    if login_info['status'] == 'success':  # status判断登录成功
        user_info = login_info['data']['user']
        username = user_info['username']
        transfer_enable = user_info['transfer_enable']  # 总可用流量
        upload_transfer = user_info['u']  # 上传流量
        download_transfer = user_info['d']  # 下载流量
        last_use = user_info['t']  # 最后使用时间
        enable = user_info['enable']  # 是否可用
        balance = user_info['balance']  # 余额
        score = user_info['score']  # 积分
        enable_time = user_info['enable_time']  # 开通时间
        expire_time = user_info['expire_time']  # 过期时间
        status = user_info['status']  # 是否激活
        password = user_info['passwd']  # 连接密码
        link = login_info['data']['link']  # 订阅链接
        conn_info = subscribe_link(link)

        # 对时间进行格式化
        last_use = datetime.fromtimestamp(last_use).strftime('%Y-%m-%d %H:%M:%S')

        # 计算流量
        transfer_enable = transfer_calculate(transfer_enable)
        used_transfer = transfer_calculate(upload_transfer + download_transfer)
        info_list = [username, transfer_enable, used_transfer, last_use, enable, balance, score, enable_time,
                     expire_time, status, password, conn_info]
        return info_list
    else:
        return 'error user'

'''
def get_config():
    config = {'server_port': 20000,  # 服务器端口 int类型
              'server': 'jpaw01.ssrcn.me',  # 服务器地址 str类型
              'password': b'yuxiaowei1994',  # 密码 bytes类型
              'local_port': 1080,  # 本地端口 int类型
              'local_address': '127.0.0.1',  # 本地地址 str类型
              'method': 'aes-256-cfb',  # 加密方式 str类型
              'protocol': 'origin',  # 加密协议 str类型
              'obfs': 'plain',  # 混淆方式 str类型
              'protocol_param': '',  # 协议参数 str类型
              'obfs_param': '',  # 混淆参数 str类型
              # 以下类型为固定
              'timeout': 300,  # 超时设置 int类型
              'fast_open': False,  # 快速打开 布尔类型
              'workers': 1,  # 线程数 int类型
              'udp_timeout': 120,  # udp超时 int类型
              'udp_cache': 64,  # udp缓存 int类型
              'connect_verbose_info': 0,  # 不知道啥 int类型
              'port_password': None,  # 不知道啥 None
              'verbose': False  # 不知道啥 布尔类型
              }

    return config
'''
