#!/usr/bin/env python2
#!encoding:utf-8
#!filename:ShadowSocks_local.py

# Copyright (c) 2014 Anonymous-Me
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import with_statement
import sys
if sys.version_info < (2, 6):
    import simplejson as json
else:
    import json

try:
    import gevent
    import gevent.monkey
    gevent.monkey.patch_all(dns=gevent.version_info[0] >= 1)
except ImportError:
    gevent = None
    print >>sys.stderr, 'warning: gevent not found, using threading instead'

import socket
import select
import urllib
import urllib2
import thread
import time
import httplib
import SocketServer
import struct
import os
import logging
import getopt
import random
import encrypt
import utils



def send_all(sock, data):
    bytes_sent = 0
    while True:
        r = sock.send(data[bytes_sent:])
        if r < 0:
            return r
        bytes_sent += r
        if bytes_sent == len(data):
            return bytes_sent


class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


class Socks5Server(SocketServer.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if sock in r:
                    data = self.encrypt(sock.recv(4096))
                    if len(data) <= 0:
                        break
                    result = send_all(remote, data)
                    if result < len(data):
                        raise Exception('Failed to send data')

                if remote in r:
                    data = self.decrypt(remote.recv(4096))
                    if len(data) <= 0:
                        break
                    result = send_all(sock, data)
                    if result < len(data):
                        raise Exception('Failed to send data')
        finally:
            sock.close()
            remote.close()

    def encrypt(self, data):
        return self.encryptor.encrypt(data)

    def decrypt(self, data):
        return self.encryptor.decrypt(data)

    def send_encrypt(self, sock, data):
        sock.send(self.encrypt(data))

    def handle(self):
        try:
            self.encryptor = encrypt.Encryptor(KEY, METHOD)
            sock = self.connection
            sock.recv(262)
            sock.send("\x05\x00")
            data = self.rfile.read(4) or '\x00' * 4
            mode = ord(data[1])
            if mode != 1:
                logging.warn('mode != 1')
                return
            addrtype = ord(data[3])
            addr_to_send = data[3]
            if addrtype == 1:
                addr_ip = self.rfile.read(4)
                addr = socket.inet_ntoa(addr_ip)
                addr_to_send += addr_ip
            elif addrtype == 3:
                addr_len = self.rfile.read(1)
                addr = self.rfile.read(ord(addr_len))
                addr_to_send += addr_len + addr
            elif addrtype == 4:
                addr_ip = self.rfile.read(16)
                addr = socket.inet_ntop(socket.AF_INET6, addr_ip)
                addr_to_send += addr_ip
            else:
                logging.warn('addr_type not support')
                # not support
                return
            addr_port = self.rfile.read(2)
            addr_to_send += addr_port
            port = struct.unpack('>H', addr_port)
            try:
                reply = "\x05\x00\x00\x01"
                reply += socket.inet_aton('0.0.0.0') + struct.pack(">H", 2222)
                self.wfile.write(reply)
                # reply immediately
                remote = socket.create_connection((SERVER, REMOTE_PORT))
                self.send_encrypt(remote, addr_to_send)
                logging.info('connecting %s:%d' % (addr, port[0]))
            except socket.error, e:
                logging.warn(e)
                return
            self.handle_tcp(sock, remote)
        except socket.error, e:
            logging.warn(e)
def heart_beat():
    hours=0
    req_url="http://192.168.0.75/test.php"
    logging.info('Loading Config From %s' % config_path)
        with open(config_path, 'rb') as f:
            config = json.load(f)
            PORT = config["server_port"]
    send_data_urlencode=urllib.urlencode(PORT)
    req=urllib2.Request(req_url, send_data_urlencode)
    res=urllib2.urlopen(req)
    result=res.read()
    result=json.load(result):
    if result["code"] == '-1'
        print "Error.余额不足或系统错误"
        sys.exit(0)
    print "当前使用时间",result["hours"],"小时"
    thread.exit_thread()
    
def main():
    print ('Time-Machine Multi-Connection Shadowsocks Client')
    global SERVER, REMOTE_PORT, PORT, KEY, METHOD, LOCAL, IPv6
    
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a+')

    # py2exe 修复 
    if hasattr(sys, "frozen") and sys.frozen in \
            ("windows_exe", "console_exe"):
        p = os.path.dirname(os.path.abspath(sys.executable))
        os.chdir(p)
    version = ''
    try:
        import pkg_resources
        version = pkg_resources.get_distribution('shadowsocks').version
    except:
        pass
    print 'shadowsocks %s' % version

    KEY = None
    METHOD = None
    LOCAL = ''
    IPv6 = False
    
    config_path = utils.find_config()
    optlist, args = getopt.getopt(sys.argv[1:], 's:b:p:k:l:m:c:6')
    for key, value in optlist:
        if key == '-c':
            config_path = value

    if config_path:
        logging.info('Loading Config From %s' % config_path)
        with open(config_path, 'rb') as f:
            config = json.load(f)

            #判断 config.json 中是否包含了 "server_password" 来确定是否启用了多端口
            if config.has_key("server_password") == True:
                #获得 "server_password" 的长度,得到服务器端口记录
                number = len(config["server_password"]) 
                #通过 random 来随机分配用哪一条服务器端口密码记录
                orientation = random.randint(0, number - 1) 
                server_dict = {}
                server_dict[u"服务器\server"]= config["server_password"][orientation][0]
                server_dict[u"链接端口\server_port"] = config["server_password"][orientation][1]
                server_dict[u"密码\password"] = config["server_password"][orientation][2]
                server_dict[u"本地端口\local_port"] = "1080"
                server_dict[u"链接方法\method"] = "AES-256-CFB"
                server_dict[u"超时\\timeout"] = "300"
                config = server_dict
                print config

            #else:
            #    print config



    optlist, args = getopt.getopt(sys.argv[1:], 's:b:p:k:l:m:c:6')
    for key, value in optlist:
        if key == '-p':
            config['server_port'] = int(value)
        elif key == '-k':
            config['password'] = value
        elif key == '-l':
            config['local_port'] = int(value)
        elif key == '-s':
            config['server'] = value
        elif key == '-m':
            config['method'] = value
        elif key == '-b':
            config['local'] = value
        elif key == '-6':
            IPv6 = True

    SERVER = config['server']
    REMOTE_PORT = config['server_port']
    PORT = config['local_port']
    KEY = config['password']
    METHOD = config.get('method', None)
    LOCAL = config.get('local', '')


    if not KEY and not config_path:
        sys.exit('Invalid Config')

    utils.check_config(config)
        
    encrypt.init_table(KEY, METHOD)

    try:
        if IPv6:
            ThreadingTCPServer.address_family = socket.AF_INET6
        server = ThreadingTCPServer((LOCAL, PORT), Socks5Server)
        logging.info("Remote server %s:%d" %(SERVER, REMOTE_PORT))
        logging.info("Starting local at %s:%d" % tuple(server.server_address[:2]))
        server.serve_forever()
    except socket.error, e:
        logging.error(e)
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)
        
if __name__ == '__main__':
     thread.start_new_thread(main)
     while():
        thread.start_new_thread(heart_beat)
        sleep(3600)