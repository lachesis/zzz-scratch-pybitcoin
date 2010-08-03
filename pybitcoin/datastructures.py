from pybitcoin.utilities import *
COINS = 100000000

class COutPoint(object):
    def unserialize(self,bytes):
        r = Reader(bytes)
        self.hash = r.getUInt256()
        self.n = r.getUInt()
        return self

    def __str__(self):
#        return str(self.hash)
        return "COutPoint({0}..,{1})".format(hex(self.hash)[2:8],self.n)

class CTxOut(object):
    def __init__(self):
        self.nValue = 0

    def __getattr__(self,key):
        if key == 'value':
            return self.nValue / float(COINS)            
        else:
            raise AttributeError("CTxOut has no such key '{0}'".format(key))
    
    def unserialize(self,bytes):
        r = Reader(bytes)
        self.nValue = r.getUInt64()
        size = r.getUByte()
        self.scriptPubKey = CScript().unserialize(r.getString(size))
        return self

    def __str__(self):
        return "CTxOut: {0.value}".format(self)

class CTxIn(object):
    def unserialize(self,bytes):
        r = Reader(bytes)
        self.prevout = COutPoint().unserialize(r.getString(36))
        self.scriptSig = CScript().unserialize(r.getString(r.getUByte()))
        self.nSequence = r.getUInt()
        return self

    def __str__(self):
        return "CTxIn: {0.prevout} seq = {0.nSequence}".format(self)
    
class CScript(object):
    def unserialize(self,bytes):
        self.bytes = bytes
        return self

    def __str__(self):
        return self.bytes

class CAddress(object):
    def __init__(self):
        self.nServices = 1

    def unserialize(self,bytes):
        ''' Extract the relevant data from the bytestring. '''
        r = Reader(bytes)
        self.nServices=r.getUInt64()
        r.advance(12) # Waste 12 characters
        self.ipBytes = [r.getUByte() for z in range(4)]
        self.port = r.getUByte()*256+r.getUByte()
        # I don't know why the following doesn't work, but it doesn't...
        #self.port = r.getUShort(byteOrder='!')
        return self

    def serialize(self):
        w = Writer()
        w.putUInt64(self.nServices)
        w.pad(12)
        for z in self.ipBytes: w.putUByte(z)
        p1 = self.port / 256
        p2 = self.port % 256
        w.putUByte(p1)
        w.putUByte(p2)
        return str(w)

    def __str__(self):
        ipstr = '.'.join( [str(k) for k in self.ipBytes] )
        return "{0}:{1} (nServices: {2})".format(ipstr,self.port,self.nServices)
