import webbrowser
import os
import hashlib
import json
import urllib
import urllib2
import httplib
print ('Welcome to use Time-Machine Client For Python')
user=raw_input('请输入您的用户名:')
password=raw_input('请输入您的密码:')
key='KC9604B9B43397Ce'
list= {
        'user' : user ,
        'password' : password
        }
json_s=json.dumps(list)
send=json_s+key
hash=hashlib.md5()
hash.update(send)
hash=hash.hexdigest()
req_url="http://192.168.0.75/test.php"
send_data= {
            'data':json_s,
            'hash':hash
            }
send_data_urlencode=urllib.urlencode(send_data)
req=urllib2.Request(req_url, send_data_urlencode)
res=urllib2.urlopen(req)
result=res.read()
result=json.load(result)
if result["code"] == '-1'
    print 'Login Error'
    webbrowser.open("www.Time-Machine.tk")
    return 0
result=json.load(result["data"])
ss_password=result['password']
ss_port=result['port']
os.system("readin.exe %s %s %s" % (ss_password,ss_port))
os.system("ShadowSocks_local.py")