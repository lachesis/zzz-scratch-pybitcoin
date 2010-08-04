#!/usr/bin/python
import socket,sys,time,random
from pybitcoin.messages import *

class Client(object):
    def __init__(self):
        self.versionNumber = 304

    def buildVersion(self,cnode):
        m = Version()
        m.version = self.versionNumber
        m.nLocalServices = 1
        m.nTime = int(time.time())

        m.addrMe = CAddress()
        m.addrMe.ipBytes = [0,0,0,0]
        m.addrMe.port = 8333

        m.addrYou = CAddress()
        m.addrYou.ipBytes = [int(k) for k in cnode.host.split('.')]
        m.addrYou.port = cnode.port

        m.nLocalHostNonce = random.randint(1,65535*65535)
        m.vSubStr = ''
        m.nBestHeight = 66000
        return m

    def connect(self,cnode):
        return cnode.connect(self)

class CNode(object):
    def __init__(self,host,port=8333):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.version = None
        self.messages = []

    def connect(self,me):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        self.version = self.getMessage()
#        self.sendMessage(me.buildVersion(self))
        self.sendMessage(Verack())
#        self.messages.append(self.getMessage())

    def getMessage(self):
        header = Header()
        headdata = self.socket.recv(20)
        header.unserialize(headdata)
        if header.command != 'version' and header.size > 0 and self.version.version > 209: # Read the checksum
            headdata += self.socket.recv(4)
            header.unserialize(headdata)
            
#        print "Getting",header

        m = newMessageObject(header.command)
        m.header = header
        if header.size > 0:
            m.unserialize(self.socket.recv(header.size))
        return m

    def sendMessage(self,message):
        message._buildHeader()
#        print "Sending",message.header
        self.socket.send(message.header.serialize()+message.bytes)

if __name__ == '__main__':
    # Connect to Bitcoin
    HOST = 'localhost'
    if len(sys.argv) > 1: HOST = sys.argv[1]

    PORT = 8333
    client = Client()
    them = CNode(HOST,PORT)
    client.connect(them)

#    print
    print them.version
#    them.sendMessage()

#    for m in them.messages:
#        print "Got",m.header
