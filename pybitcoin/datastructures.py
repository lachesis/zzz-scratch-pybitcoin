from pybitcoin.utilities import *
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
