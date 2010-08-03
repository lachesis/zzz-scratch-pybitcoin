#!/usr/bin/python

# This code reads the file "dump1.txt" and prints all messages it finds.
# It can be easily adapted to read from a socket.
# (just pass MessageQueue a socket object)

from pybitcoin.utilities import *
from pybitcoin.datastructures import *
from pybitcoin.messages import *
import sys,socket

class BufferedReader(object):
    def __init__(self,fd,chunkSize=1024):
        self.fd = fd
        self.buffer = ''
        self.pointer = 0
        self.chunkSize = chunkSize
    
    def close(self):
        self.fd.close()
        
    def read(self,length):
        while len(self.buffer) - self.pointer < length:
            if isinstance(self.fd,socket._socketobject):
                self.buffer += self.fd.recv(self.chunkSize)
            else:
                self.buffer += self.fd.read(self.chunkSize)
        self.pointer += length
        return self.buffer[self.pointer-length:self.pointer]

    def rewind(self,amt):
        self.pointer -= amt

class MessageQueue(object):
    def __init__(self,fd):
        self.fd = BufferedReader(fd)

    def start(self):
        h = Header()
        lidx = 0
        l4 = []
        while 1:
            l4.append(self.fd.read(1))
            if len(l4) > 4: l4.pop(0)
            potentialStart = ''.join(l4)
            if potentialStart == h.START:
                headdata = potentialStart + self.fd.read(16)
                h.unserialize(headdata)
                if h.shouldHaveChecksum(): h.addChecksum(self.fd.read(4))
                m = newMessageObject(h.command)
                m.header = h
                m.unserialize(self.fd.read(h.size))
                self.handleMessage(m)                  
    
    def handleMessage(self,message):
        print message

#st = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#st.connect(('localhost',8333))

if __name__ == '__main__':
    st = open('dump1.txt','rb')
    MessageQueue(st).start()
    st.close()

