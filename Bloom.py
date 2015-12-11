'''
Created on 08-Dec-2015

@author: pawan
'''

import hashlib
import random

class Bloom:
    """  Hash functions used for bloom filter """
    h = [hashlib.sha1(), hashlib.sha384(), hashlib.sha512()]
    ''' Security parameter lambda'''
    lam = 16
    def __init__(self, inputArray):
        self.inputArray = inputArray
        '''Length of bloom filter and garbled bloom filter'''
        self.m = 512
        self.garbledBloomArray = [None for i in xrange(self.m)]
        self.bloomArray = [0 for i in xrange(self.m)]

    def getLambda(self):
        return self.lam

    def getInput(self):
        return self.inputArray

    def getGarbledBloom(self):
        return self.garbledBloomArray
    
    def getBloom(self):
        return self.bloomArray
    
    def generateBloom(self):
        for element in self.inputArray:
            h = [hashlib.sha1(), hashlib.sha384(), hashlib.sha512()]
            for i in xrange(len(h)):
                val = h[i]
                val.update(str(element))
                j = int(val.hexdigest(), base=16) % self.m
                self.bloomArray[j]=1
    
    def generateGarbledBloom(self):

        for element in self.inputArray:
            emptySlot = -1
            finalShare = element
            h = [hashlib.sha1(), hashlib.sha384(), hashlib.sha512()]
            for i in xrange(len(h)):
                val = h[i]
                val.update(str(element))
                j = int(val.hexdigest(), base=16) % self.m
                if(self.garbledBloomArray[j]==None):
                    if(emptySlot==-1):
                        emptySlot = j   # Reserve emptyslot for final share
                    else:
                        newShare = random.getrandbits(self.lam)    # Generate new lambda bit share
                        self.garbledBloomArray[j] = newShare
                        finalShare = finalShare ^ self.garbledBloomArray[j]
                else:
                    finalShare = finalShare ^ self.garbledBloomArray[j]
            self.garbledBloomArray[emptySlot] = finalShare
        for i in xrange(self.m):
            if(self.garbledBloomArray[i]==None):
                self.garbledBloomArray[i] = random.getrandbits(self.lam)
                
    
    def queryBloom(self, x):
        h = [hashlib.sha1(), hashlib.sha384(), hashlib.sha512()]
        for i in xrange(len(h)):
            val = h[i]
            val.update(str(x))
            j = int(val.hexdigest(), base=16) % self.m
            if(self.bloomArray[j]==0):
                return False
        return True
    
    
    def queryGarbled(self, x, GBF):
        recovered = 0
        h = [hashlib.sha1(), hashlib.sha384(), hashlib.sha512()]
        for i in xrange(len(h)):
            val = h[i]
            val.update(str(x))
            j = int(val.hexdigest(), base=16) % self.m
            recovered = recovered ^ GBF[j]
        if(recovered == x):
            return True
        else:
            return False
    
    def generateIntersection(self, GBF):
        GBFint = [None for i in xrange(self.m)]
        for i in xrange(len(self.bloomArray)):
            if(self.bloomArray[i]==0):
                GBFint[i]=random.getrandbits(self.lam)
            else:
                GBFint[i]=GBF[i]
        return GBFint


a = Bloom([1,2,3,4,5,6])
b = Bloom([3,4,5,6])
a.generateGarbledBloom()
b.generateBloom()
inter = b.generateIntersection(a.getGarbledBloom())
for x in [3,4,5,6]:
    if(b.queryGarbled(x, inter)):
        print x
