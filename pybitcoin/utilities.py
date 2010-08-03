import StringIO,struct,math
def prettyhex(bin,newlinesEvery=8):
    l = ["0x{0:02X}".format(ord(z)) for z in bin]
    if newlinesEvery:
        p = []
        for i in range(0,len(l),newlinesEvery):
            p.append(' '.join(l[i:i+newlinesEvery]) + '')
        return '\n'.join(p)
    return ' '.join(l)

class Reader(object):
    def __init__(self,text):
        self.stringIO = StringIO.StringIO(text)
        
    def _get(self,structCode='I',byteOrder='<'):
        s = struct.Struct('{0}{1}'.format(byteOrder,structCode))
        return s.unpack(self.stringIO.read(s.size))[0]

    def advance(self,length): # Ignore this many bytes
        self.stringIO.read(length)

    def getSize(self): 
        first = self.getUByte()
        if first == 255: return self.getUInt64()
        elif first == 254: return self.getUInt()
        elif first == 253: return self.getUShort()
        else: return first

    def getInt(self,byteOrder='<'): return self._get('i')
    def getInt64(self,byteOrder='<'): return self._get('q')
    def getUInt(self,byteOrder='<'): return self._get('I')
    def getUInt64(self,byteOrder='<'): return self._get('Q')
    def getUInt256(self,byteOrder='<'): 
        b = []
        for a in range(32): b.append(self.getUByte())
        res = 0
        for i,a in enumerate(b):
            res += a*int(math.pow(8,i))
        return res
    def getShort(self,byteOrder='<'): return self._get('h')
    def getByte(self,byteOrder='<'): return self._get('b')
    def getUShort(self,byteOrder='<'): return self._get('H')
    def getUByte(self,byteOrder='<'): return self._get('B')
    def getString(self,size,byteOrder='<'): return self._get('{0}s'.format(size))

class Writer(object):
    def __init__(self):
        self.output = ''
        
    def _put(self,value,structCode='I',byteOrder='<'):
        s = struct.Struct('{0}{1}'.format(byteOrder,structCode))
        v = s.pack(value)
        self.output += v
        return v

    def pad(self,length): # Ignore this many bytes
        self.output += '\0'*length

    def putSize(self,size):
        if size < 253:
            return self.putUByte(size)
        elif size <= math.pow(8,2): 
            self.putUByte(253)
            return self.putUShort(size)
        elif size <= math.pow(8,4): 
            self.putUByte(254)
            return self.putUInt(size)
        else: 
            self.putUByte(255)
            return self.putUInt64(size)

    def putInt(self,value,byteOrder='<'): return self._put(value,'i')
    def putInt64(self,value,byteOrder='<'): return self._put(value,'q')
    def putUInt(self,value,byteOrder='<'): return self._put(value,'I')
    def putUInt64(self,value,byteOrder='<'): return self._put(value,'Q')
    def putShort(self,value,byteOrder='<'): return self._put(value,'h')
    def putByte(self,value,byteOrder='<'): return self._put(value, 'b')
    def putUShort(self,value,byteOrder='<'): return self._put(value,'H')
    def putUByte(self,value,byteOrder='<'): return self._put(value,'B')
    def putString(self,value,byteOrder='<',length=None): return self._put(value,'{0}s'.format(length and length or len(value)))

    def __str__(self):
        return self.output

