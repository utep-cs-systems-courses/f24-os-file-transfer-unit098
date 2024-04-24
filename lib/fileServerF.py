#! /usr/bin/env python3

# Echo server program

import ibfram
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

def childHandler(add):
    dec=ibfram.ibdeframmer()
    conn, addr = add  # wait until incoming connection request (and accept it)
    print(f"Child pid: {os.getpid()} connected to client at {addr}")
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
    sys.exit(0)



pidAddr = {}
progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)
s.settimeout(5) # allow only one outstanding request
# s is a factory for connected sockets


while 1:
    while pidAddr.keys():
        if (waitResult := os.waitid(os.P_ALL, 0, os.WNOHANG | os.WEXITED)): 
            zPid, zStatus = waitResult.si_pid, waitResult.si_status
            print(f"""zombie reaped:
            \tpid={zPid}, status={zStatus}
            \twas connected to {pidAddr[zPid]}""")
            del pidAddr[zPid]
        else:
            break               # no zombies; break from loop
    print(f"Currently {len(pidAddr.keys())} clients")
    
    try:
        connSockAddr = s.accept()
    except TimeoutError:
        connSockAddr = None
        
    if connSockAddr is None:
        continue

    f = os.fork()
    if (f==0):
        s.close()
        childHandler(connSockAddr)
    soc, addr = connSockAddr
    soc.close()
    pidAddr[f] = addr
    print(f"spawned off child with pid = {f} at addr {addr}")
        






