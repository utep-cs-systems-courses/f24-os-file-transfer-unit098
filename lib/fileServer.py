#! /usr/bin/env python3

# Echo server program

import ibfram
import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

dec=ibfram.ibdeframmer()
conn, addr = s.accept()  # wait until incoming connection request (and accept it)
fulldata = bytes()
print('Connected by', addr)
while 1:
    data = conn.recv(1024)
    if len(data) == 0:
        print("Zero length read, nothing to send, writing")
        print(fulldata.decode())
        dec.deframefiles(fulldata)
        break
    fulldata = fulldata+data
    print("captured", data.decode())
    
conn.shutdown(socket.SHUT_WR)
conn.close()

