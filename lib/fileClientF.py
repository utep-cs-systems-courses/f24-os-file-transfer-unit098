#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os, ibfram
sys.path.append("../lib")       # for params
import params

framer = ibfram.ibframmer()
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-f', '--files' ), 'files', 'shrimp')
    )



progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, fil = paramMap["server"], paramMap["usage"], paramMap["files"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
fill = re.split(",", fil)
for i in fill:
    if os.path.exists(i):
        framer.writeToFrame(i.encode())
        fd = os.open(i, os.O_RDONLY)
        tb = os.read(fd, 1000)
        dba = bytearray()
        while len(tb):
            dba.extend(tb)
            tb = os.read(fd, 1000)
        framer.writeToFrame(dba)
    else:
        msg = "File "+i+" does not exist skipping\n"
        os.write(2, msg.encode())
outMessage = framer.fd
        
while len(outMessage):
    print("sending '%s'" % outMessage.decode())
    bytesSent = s.send(outMessage)
    outMessage = outMessage[bytesSent:]
    

s.shutdown(socket.SHUT_WR)      # no more output

while 1:
    data = s.recv(1024).decode()
    print("Received '%s'" % data)
    if len(data) == 0:
        break
print("Zero length read.  Closing")

s.close()
