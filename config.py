from shadowsocks import local

def get_config():
    config = {'server_port' : 20000,    #服务器端口 int类型
              'server' : 'jpaw01.ssrcn.me', #服务器地址 str类型
              'password' :  b'yuxiaowei1994',    #密码 bytes类型
              'local_port' : 1080,   #本地端口 int类型
              'local_address' : '127.0.0.1', #本地地址 str类型
              'method' : 'aes-256-cfb', #加密方式 str类型
              'protocol' : 'origin',    #加密协议 str类型
              'obfs' : 'plain',     #混淆方式 str类型
              'protocol_param' : '',    #协议参数 str类型
              'obfs_param' : '',    #混淆参数 str类型
              #以下类型为固定
              'timeout' : 300,  #超时设置 int类型
              'fast_open' : False,  #快速打开 布尔类型
              'workers' : 1,    #线程数 int类型
              'udp_timeout' : 120,  #udp超时 int类型
              'udp_cache' : 64,     #udp缓存 int类型
              'connect_verbose_info' : 0,   #不知道啥 int类型
              'port_password' : None,   #不知道啥 None
              'verbose' : False     #不知道啥 布尔类型
              }

    return config
