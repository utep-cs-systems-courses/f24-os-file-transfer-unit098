#! /usr/bin/env python3

import os
import sys
from sys import argv
import ibfram
import obfram

if len(argv) == 1:
    os.write(2, "this program needs arguments <mode (x ox i ix)> <files if in create mode>\n".encode())
else:
    match argv[1]:
        case 'c':
            if len(argv) == 2:
                os.write(2, "create mode needs at least one file to archive\n".encode())
            else:
                framer = ibfram.ibframmer()
                for i in argv[2::]:
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
                dtw = framer.fd
                while len(dtw):
                    bw = os.write(1, dtw)
                    dtw = dtw[bw::]
                    
        case "oc":
            if len(argv) == 2:
                os.write(2, "create mode needs at least one file to archive\n".encode())
            else:
                framer = obfram.obframmer()
                for i in argv[2::]:
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
                dtw = framer.fd
                while len(dtw):
                    bw = os.write(1, dtw)
                    dtw = dtw[bw::]
        case 'x':
            if len(argv) != 2:
                os.write(2, "extract mode can take no arguments\n".encode())
            else:
                deframer = ibfram.ibdeframmer()
                ab = bytearray()
                tb = os.read(0, 1000)
                while len(tb):
                    ab.extend(tb)
                    tb = os.read(0, 1000)
                deframer.deframefiles(ab)
        case 'ox':
            if len(argv) != 2:
                os.write(2, "extract mode can take no arguments\n".encode())
            else:
                deframer = obfram.obdeframmer()
                ab = bytearray()
                tb = os.read(0, 1000)
                while len(tb):
                    ab.extend(tb)
                    tb = os.read(0, 1000)
                deframer.deframefiles(ab)
        case _:
            os.write(2, "First argument must be either x, ox, c, or oc\n".encode())