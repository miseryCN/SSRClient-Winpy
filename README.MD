# 项目名:flyProxy
# 语言:python3
# 代码贡献: Misery,Roach
# 今天是2018年10月8日 是这个项目的开始时间

# 功能简述:

sock5 windows客户端，搭配shadowsocksr服务端使用，可实现 全局代理，PAC自动代理，直连模式，
该版本根据ssrpanel深度定制，可无缝对接面板网站，直接使用网站的账号密码登录。

# 开发环境
后台语言: python3 
winform界面: wxpython 
数据库: mysql5.7 
调用的软件: privoxy,ss_client python版 

# 工作流程 

浏览器 --> http代理 --> （privoxy --> socks5代理 --> ss_client python版） --> ss_server python版 --> 目标网页