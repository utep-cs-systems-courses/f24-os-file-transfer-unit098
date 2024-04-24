#! /usr/bin/env python3


import os

fg = os.open("./wumbus/test.txt", os.O_RDWR | os.O_CREAT )
os.write(fg, "what?!?!".encode())