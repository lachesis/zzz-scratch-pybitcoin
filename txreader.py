#!/usr/bin/python
from pybitcoin.utilities import prettyhex
from pybitcoin.datastructures import *

with open('textNetworkTxDump','rb') as inp:
    s = inp.read()
    
l = s.split(':')
l.remove('Tx')
z = [a.replace('TxOut','').replace('TxIn','').strip() for a in l]

SUB = ['tx','txin','txout','txout']
for i,b in enumerate(z):
    print SUB[i]
    if i == 1:
        print CTxIn().unserialize(b)
    if i > 1:
        print CTxOut().unserialize(b)
    print prettyhex(b)
    print
