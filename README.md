ShadowSocks Client For Time-Machine
==================

ShadowSocks 是一个轻量级隧道代理，用来穿过防火墙。

原版由 clowwindy 用 Python 编写，后续有很多其他的移植版本。[见这里](https://github.com/clowwindy/shadowsocks)

但是由于服务需要于是将其改版，支持多服务器链接

所以就在 [ShadowSocks](https://github.com/clowwindy/shadowsocks) 的基础上修改了一个ShadowSocks-Client版本。

使用
----

首先检查是 Python 版本是否是 2.6 or 2.7

    $ python --version
    Python 2.7.5
    
下载 ShadowSocks Client For Time-Machine



在`ShadowSocks Client For Time-Machine`目录下建立一个`config.json`文件、内容如下：

    {
        "server":"my_server_ip",
        "server_port":10086,
        "local_port":1080,
        "password":"barfoo!",
        "timeout":300,
        "method":"table"
    }
    
    
多服务器、端口和密码的`config.json`格式如下：



    {   
        "server_password":
        [
        ["my_server_ip1", 10086, "test"],
        ["my_server_ip2", 10087, "213369852147zxc"],
        ["my_server_ip3", 10088, "qazw2sf31sxedcrfv"],
        ["my_server_ip4", 10089, "barfoosadfs!abcde"]
        ],
        "local_port":1080,
        "timeout":300,
        "method":"aes-256-cfb"
    }

然后运行`ShadowSocks_local.py`

      ShadowSocks_local.py
      

然后把浏览器代理修改为如下即可：

        协议：SOCKS v5
        地址：127.0.0.1
        端口：1080, 也就是刚才填写的 local_port
