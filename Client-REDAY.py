import webbrowser
import os
import md5
import json
print ('Welcome to use Time-Machine Client For Python')
user=raw_input('请输入您的用户名:')
password=raw_input('请输入您的密码:')
key='KC9604B9B43397Ce'
list= {
        'user' : user ,
        'password' : password
        }
send=json.dumps(list)
temp=send+key
hash=md5.new(temp)
print hash
hash2=md5.degest(temp)
print hash2
