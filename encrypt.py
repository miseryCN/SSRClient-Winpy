"""
这个文件是用来对本地存储的账号密码信息进行加密解密的

首次运行:
1 客户端发送账号给服务端
2 服务端对客户端的账号随机生成一个秘钥并存储
3 服务端发送秘钥给客户端 客户端对账号密码信息加密进行本地存储

非首次运行:
1 客户端发送账号给客户端
2 服务端查询账号对应的秘钥，发送给客户端
3 客户端使用秘钥，对账号密码信息进行解密
"""

from Crypto.Cipher import AES
from requests import get
from os import path


def add_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    add_value = str.encode(value)
    return add_value

def AES_encrypt(username,password,key):
    text = 'username='+username+'&password='+password
    aes = AES.new(add_16(key),AES.MODE_ECB)
    encrypt_aes = aes.encrypt(add_16(text))
    open('./user_info','wb').write(encrypt_aes)

def AES_decrypt(key):
    encrypted_text = open('./user_info','rb').read()
    aes = AES.new(add_16(key),AES.MODE_ECB)
    decrypt_text = str(aes.decrypt(encrypted_text),encoding='utf-8').replace('\0','')
    return decrypt_text

def get_key(username):
    key_server = 'http://127.0.0.1:1024'
    data = {
        'username' : username
    }

    try:
        key = get(key_server,data).text
        return key
    except:
        return 'error_network'

def get_password(username):
    key = get_key(username)
    if path.exists('./user_info'):
        user_info = AES_decrypt(key)
        user_info = user_info.split('&')
        password = user_info[1].replace('password=','')
        return password
