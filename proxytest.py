import socket
import socks
import urllib2

socks.set_default_proxy(socks.SOCKS5, "proxy-nl.privateinternetaccess.com",1080,True,"x2341981","KbTTFR4nFU")
socket.socket = socks.socksocket  #dont add ()!!!

conn = urllib2.urlopen('http://python.org')
return_str = conn.read()
print return_str