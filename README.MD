# 项目名:SSRClient-Winpy
# 语言:python3
# 代码贡献: xiaowei,Roach
### 今天是2018年10月8日 是这个项目的开始时间

# 功能简述

sock5 windows客户端，搭配shadowsocksr服务端使用，可实现基础的 全局代理，PAC自动代理，直连模式，
该版本根据ssrpanel深度定制，美化，可无缝对接面板网站，直接使用网站的账号密码登录。

# 开发环境
后台语言: python3<br/>
winform界面: pyqt5<br/> 
数据库: mysql5.7 <br/>
支持: privoxy,ss_client python版 

# 工作流程 

浏览器 --> http代理 --> （privoxy --> socks5代理 --> ss_client python版） --> ss_server python版 --> 目标网页

#当前界面预览【已实现功能】（2018.10.12）
![预览图](http://github-1251763511.file.myqcloud.com/20181012.png)

#开发日志
2018.10.8  项目开始 / 导入各种依赖库<br/>
2018.10.9  添加注册表改IE代理功能,增加pac判断功能<br/>
2018.10.10 重写PAC自动判断功能，新增自动重启privoxy<br/>
2018.10.11 使用win32api对privoxy进行自动关闭前台窗口处理 / 写了一个基础GUI界面<br/>
2018.10.12 修复privoxy关闭不流畅的问题 / 修改shadowsocks客户端传参数方式 / 写入测试账号密码<br/>
