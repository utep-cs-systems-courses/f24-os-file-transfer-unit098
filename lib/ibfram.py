import os

class ibframmer:
    def __init__(self):
        self.fd = bytearray()
        self.ec = '/'.encode()
        self.pecc = '/'.encode()
        self.eofc = 'e'.encode()
    
    def writeToFrame(self, data):
        for c in data:
            self.fd.append(c)
            if c == ord(self.ec):
                self.fd.append(ord(self.pecc))
        self.fd.append(ord(self.ec))
        self.fd.append(ord(self.eofc))
                   
                

class ibdeframmer:
    def __init__(self):
        self.ec = '/'.encode()
        self.pecc = '/'.encode()
        self.eofc = 'e'.encode()
        
    def deframefiles(self, data):
        named = bytearray()
        filedata = bytearray()
        i=0
        name = True
        Sane = False
        while i < len(data):
            if data[i] == ord(self.ec):
                i +=1
                if data[i] == ord(self.pecc):
                    if name:
                        named.append(ord(self.ec))
                    else:
                        filedata.append(ord(self.ec))
                elif data[i] == ord(self.eofc):
                    if name:
                        Sane = True
                        fd = os.open("./output/"+named.decode(), os.O_WRONLY|os.O_TRUNC|os.O_CREAT)
                        named.clear()
                        name = False
                    else:
                        while len(filedata):
                            bw = os.write(fd, filedata)
                            filedata = filedata[bw::]
                        name = True
            else:
                if name:
                    named.append(data[i])
                else:
                    filedata.append(data[i])
            i+=1
        if not Sane:
            os.write(2, "This arcive is clearly broken no file name was found".encode())