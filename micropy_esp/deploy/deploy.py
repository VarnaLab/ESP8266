
import sys
import os
import json

parentDir = os.getcwd()
sys.path.insert(0, parentDir+'/lib')
from webrepl_cli import websocket
import websocket_helper

try:
    import usocket as socket
except ImportError:
    import socket

host = "192.168.98.37"
port = "8266"
passwd = "1234"

# establish connection with esp
s = socket.socket()

ai = socket.getaddrinfo(host, port)
addr = ai[0][4]
print('Connecting to address ' + str(addr[0])+":"+str(addr[1]))
s.connect(addr)
#s = s.makefile("rwb")
print('Connected')
websocket_helper.client_handshake(s)

ws = websocket(s)
print('Authenticating...')
webrepl.login(ws, passwd)
print('Successfully authenticated:')
print("Remote WebREPL version:", webrepl.get_ver(ws))

# Set websocket to send data marked as "binary"
ws.ioctl(9, 2)


def uploadSource(filename, subdir):
    import webrepl_cli as webrepl
    src_file = parentDir + '/' + subdir + '/' + filename
    print('Sending ' + src_file + ' to device..')
    webrepl.put_file(ws, src_file, filename)
    print('File sent!')


if len(sys.argv):
    uploadSource(sys.argv[1], 'deploy')
else:
    deploymenJson = json.load(open(parentDir+'/deploy.json'))
    for subdir in deploymenJson:
        for file in deploymenJson[subdir]:
            uploadSource(file, subdir)
        print(deploymenJson[subdir])
