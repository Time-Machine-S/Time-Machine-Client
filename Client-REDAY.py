import webbrowser
import os
import hashlib
import json
import urllib
import urllib2
print ('Welcome to use Time-Machine Client For Python')
user=raw_input('请输入您的用户名:')
password=raw_input('请输入您的密码:')
key='KC9604B9B43397Ce'
list= {
        'user' : user ,
        'password' : password
        }
json=json.dumps(list)
send=json+key
hash=hashlib.md5()
hash.update(send)
hash.hexdigest()
req_url="http://www.time-machine.tk/api/client-login"
send_data= {
            'data':data,
            'hash':hash
            }
send_data_urlencode=urllib.urlencode(send_data)
connection=httplib.HTTPConnection("www.time-machine.tk")
connection.request(method="POST",url=req_url,body=send_data_urlencode) 
response=connection.getresponse()
response_read=response.read()
