import struct
from pybitcoin.utilities import *
from pybitcoin.datastructures import *
VERSION = 307

class Header(object):
    START = '\xf9\xbe\xb4\xd9'
    def unserialize(self,text):
        self.text = text
        if len(self.text) == 20:
            self.text += '\0\0\0\0' # Handle missing checksums - hack
        (start,command,size,check) = struct.unpack('<4s 12s i i',self.text)
        command = command.strip(chr(0))
        
        # Verify that the message starts with the right 4 bytes
        assert start == self.START

        # Set the proper variables
        self.command = command
        self.size = size
        if not check: check = None
        self.checksum = check
        return self

    def serialize(self):
        w = Writer()
        w.putString(self.START)
        w.putString(self.command,length=12)
        w.putInt(self.size)
        if self.checksum:
            w.putInt(self.checksum)
        return str(w)

    def shouldHaveChecksum(self):
        return bool(self.command != 'version' and self.size > 0 and VERSION > 209)         
    
    def addChecksum(self,bytes):
        assert len(bytes) == 4
        r = Reader(bytes)
        self.checksum = r.getUInt()        

    def __str__(self):
        return '"{0.command}" {0.size}b (checksum: {0.checksum})'.format(self)

class Message(object): 
    def _buildHeader(self):
        self.header = Header()
        self.header.command = self.COMMAND

        try: self.bytes
        except AttributeError: self.bytes = self.serialize()

        self.header.size = len(self.bytes)
        self.header.checksum = self._calculateChecksum()
        return self.header

    def serialize(self): return ''
    def unserialize(self,bytes): 
        self.bytes = bytes
        return self
    def _calculateChecksum(self): return None
    def __str__(self):
        if not self.header: self._buildHeader()
        return "{0}\n{1}\n".format(self.header,prettyhex(self.bytes))

def newMessageObject(command):
    d = {
        'verack': Verack,
        'version': Version,
        'inv': Inv,
        'getdata': Getdata,
    }
    if command in d:
        return d[command]()
    return Message()

class Verack(Message):
    COMMAND = 'verack'

class Version(Message):
    COMMAND = 'version'
    def _calculateChecksum(self): pass

    def serialize(self):
        w = Writer()
        w.putInt(self.version)
        w.putUInt64(self.nLocalServices)
        w.putUInt64(self.nTime)
        w.putString(self.addrYou.serialize())
        w.putString(self.addrMe.serialize())
        w.putUInt64(self.nLocalHostNonce)
        w.putUByte(len(self.vSubStr))
        w.putString(self.vSubStr)
        w.putInt(self.nBestHeight)
        return str(w)

    def unserialize(self,data):
        r = Reader(data)
        self.version = r.getInt()
        self.nLocalServices = r.getUInt64()
        self.nTime = r.getUInt64()
        self.addrYou = CAddress().unserialize(r.getString(26))
        self.addrMe = CAddress().unserialize(r.getString(26))
        self.nLocalHostNonce = r.getUInt64()
        vSubStrLen = r.getSize()
        self.vSubStr = r.getString(vSubStrLen)
        self.nBestHeight = r.getInt()
        return self

    def __str__(self):
        s = ''
        try: self.header
        except AttributeError: self._buildHeader()
        try: s += "{0}\n".format(self.header)
        except AttributeError: pass
        s += "Version: {0}\n".format(self.version)
        s += "nLocalServices: {0}\n".format(self.nLocalServices)
        s += "nTime: {0}\n".format(self.nTime)
        s += "addrYou: {0}\n".format(self.addrYou)
        s += "addrMe: {0}\n".format(self.addrMe)
        s += "nLocalHostNonce: {0}\n".format(self.nLocalHostNonce)
        s += "vSubStr: \"{0}\"\n".format(self.vSubStr)
        s += "nBestHeight: {0}\n".format(self.nBestHeight)
        return s            

class Inv(Message):
    COMMAND = 'inv'
    def unserialize(self,bytes):
        super(Inv,self).unserialize(bytes)
        r = Reader(bytes)
        self.vInv = []
        for m in range(r.getSize()):
            self.vInv.append(CInv().unserialize(r.getString(36)))
        return self

    def __str__(self):
        s = ''
        try: self.header
        except AttributeError: self._buildHeader()
        try: s += "{0}\n".format(self.header)
        except AttributeError: pass
        s += '\n'.join([str(z) for z in self.vInv])
        return s

class Getdata(Inv):
    COMMAND = 'getdata'
