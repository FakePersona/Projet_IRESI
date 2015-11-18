import hashlib
import random
import math

# This function sums every element of an array
def sum_array(X):
    s = 0
    for x in X:
        s += x
    return s

# This function creates the everage of the lement af array X
def avg(X):
    return sum_array(X)/len(X)
    
    
# This calculates the codeviance between two arrays
def cod(X, Y):
    if len(X) != len(Y):
        return 0
    
    Z = [X[i]*Y[i] for i in range(len(X))]
    
    return avg(Z) - avg(X)*avg(Y)
    
    

def sketch_cod(X, Y, k, delta):#wip
    min_cod = float('inf')
    t = int(math.log(1/delta))
    print(t)
    for _ in range(t):
        Xk, Yk = hash_split(X, Y, k)
        sX = [sum_array(x) for x in Xk]
        sY = [sum_array(y) for y in Yk]
        
        
        min_cod = min(min_cod, cod(sX, sY))
        
    return min_cod

    
class epahttp:
    def __init__(self, string):
        self.parse(string)
        
    def parse(self, s):
        self.host = ""
        self.D = 0
        self.H = 0
        self.M = 0
        self.S = 0
        self.request = ""
        self.code = 0
        self.size = 0
        
        c = 0
        
        while s[c] != ' ':
            self.host += s[c]
            c += 1
        
        while s[c] != '[':
            c += 1
        
        self.D = int(s[c+1:c+3])
        self.H = int(s[c+4:c+6])
        self.M = int(s[c+7:c+9])
        self.S = int(s[c+10:c+12])
        
        while s[c] != '"':
            c += 1
            
        c += 1
        while s[c] != '"':
            self.request += s[c]
            c += 1
            
        c += 2
        s2 = ""
        while s[c] != ' ':
            s2 += s[c]
            c += 1
        try:
            self.code = int(s2)
            self.size = int(s[c:])
        except ValueError:
            ()



def parseFile(path):
    f = open(path)
    data = []
    for line in f:
        data.append(epahttp(line))
    return data
    
    
    
def h(a, x):
    M = 4
    w = 32
    return (a*x) % (1 << w) >> (w - M)

    

def hash_split(X, Y, k): #Modify with hash
    if len(X) != len(Y):
        return [], []
        
    ind = [random.randint(0, k-1) for _ in range(len(X))]
    Xk = [[] for _ in range(k)]
    Yk = [[] for _ in range(k)]
    
    for i in range(len(X)):
        Xk[ind[i]].append(X[i])
        Yk[ind[i]].append(Y[i])
        
    return Xk, Yk
    
    
        
    
X = [random.randint(0, 1 << 32 -1) for i in range(100)]
a = random.randint(0, 1 << 32 -1)
print(X)
print([h(a, x) for x in X])
    
print(sketch_cod([43,12,911,85,76,12,36,77], [83,73,89,326,82,245,78,97], 5, .0001))
        
# data = parseFile("1epahttp.txt")
            
