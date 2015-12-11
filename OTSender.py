'''
Created on 08-Dec-2015

@author: pawan
'''
import hashlib
import random
import socket
from generator import euclid, modifiedPower
import math

class OTSender():
    def __init__(self, g, p, q):
        self.g = g
        self.p = p
        self.q = q
        self.s = socket.socket()
        self.conn = self.makeConnection()


    def makeConnection(self):
        self.s.bind(('127.0.0.1', 3000))
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            return c
    
    def randomOracle(self, x):
        return int(hashlib.sha256(str(x)).hexdigest(), base=16)
    
    '''  M0 random lambda bit string and M1 actual string '''
    def Obliviously_Send(self, M0,M1,num_of_OT, lam):
        conn = self.conn
        for i in xrange(num_of_OT):
            print i
            r=random.randrange(self.q)
            c=random.randrange(self.q)
            conn.send(str(c))
            pk0 = conn.recv(200) #you should receive pk0 from the receiver via the sender_receiver channel
            pk0r=modifiedPower(int(pk0),r,self.q)
            gr=modifiedPower(self.g,r,self.q)
            r0=(hashlib.sha512(str(pk0r)+str(0)).digest())
            r00=str(r0)* int(math.ceil(num_of_OT/len(r0))+1)
            cr=modifiedPower(c,r,self.q)
            gcd=inv=-1
            while gcd != 1 and inv <= 0 :
                gcd,inv,k = euclid(pk0r,self.q)
            pk1r=cr*inv%self.q
            r1=(hashlib.sha512(str(pk1r)+str(1)).digest())
            r10=str(r1) * int(math.ceil(num_of_OT/len(r1))+1)
            E0=bin(int(M0[i])^ord(r00[i]))[2:].zfill(lam)
            E1=bin(int(M1[i])^ord(r10[i]))[2:].zfill(lam)
            conn.send(str(gr))
            conn.send(str(E0))
            conn.send(str(E1))
        return True
