import hashlib
import random
import math
import hash_rand
import parser

####### Statistic tools

# This function creates the average of the elements of array X
def avg(X):
    return sum_array(X)/len(X)

# Returns the biggest element of a vector
def maxi(l):
    max = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
    return max

# Returns the variance
def variance(l):
    m=avg(l)
    return avg([(x-m)**2 for x in l])


def ecart(t):
    return variance(t)**0.5

# This function sums every element of an array
def sum_array(X):
    s = 0
    for x in X:
        s += x
    return s

###### Codeviance computing
    
# This calculates the codeviance between two arrays
def cod(X, Y,max):
    if len(X) != len(Y):
        return 0
    X1 = [0 for i in range(max)]        # Let's create frequency vectors
    Y1 = [0 for i in range(max)]
    for i in range(len(X)):
        X1[X[i]]+=1
        Y1[Y[i]]+=1
    Z = [X1[i]*Y1[i] for i in range(len(X1))] # Then we compute the metrics to get the codeviance
    return avg(Z) - avg(X1)*avg(Y1)

# Same thing except we assume X and Y are frequency vectors
def cod_int(X, Y):
    if len(X) != len(Y):
        return 0
    Z = [X[i]*Y[i] for i in range(len(X))]
    return avg(Z) - avg(X)*avg(Y)
    
    
# This calculates the codeviance between two streams
def sketch_cod(X, Y, k, delta):
    min_cod = float('inf')
    X1 = [0 for i in range(len(X))]     # We will need to work on frequency vectors
    Y1 = [0 for i in range(len(X))]
    for i in range(len(X1)):
        X1[X[i]]+=1
        Y1[Y[i]]+=1
    t = int(math.log(1/delta)) + 1
    for _ in range(t):
        h = hash_rand.Hash(32, int(math.log(k,2)))
        Xk, Yk = hash_split(X1, Y1, h, k)
        sX = [sum_array(x) for x in Xk]
        sY = [sum_array(y) for y in Yk]
        min_cod = min(min_cod, cod_int(sX, sY))
    return min_cod

#Another version not using the h_split auxiliary function, which allows us to use two separate hash functions for X and Y
def sketch_cod2(X, Y, k, delta):
    min_cod = float('inf')
    t = int(math.log(1/delta)) + 1
    for _ in range(t):
        h1 = hash_rand.Hash(32, int(math.log(k,2)))
        h2 = hash_rand.Hash(32, int(math.log(k,2)))
        X1 = [0 for i in range(k)]     # We will need to work on frequency vectors
        Y1 = [0 for i in range(k)]
        for i in range(len(X)):
            X1[h1(X[i])]+=1
            Y1[h2(Y[i])]+=1
        min_cod = min(min_cod, cod_int(X1, Y1))
    return min_cod

######Distributed algorithm

# Another version used to compute the distributed algorithm
def sketch_int(X, Y, k, delta, h):#wip
    min_cod = float('inf')
    t = int(math.log(1/delta)) + 1
    for _ in range(t):
        X1 = [0 for i in range(k)]     # We will need to work on frequency vectors
        Y1 = [0 for i in range(k)]
        for i in range(len(X)):
            X1[h[i](X[i])]+=1
            Y1[h[i](Y[i])]+=1
        min_cod = min(min_cod, cod_int(X1, Y1))
    return min_cod

# This finds out how many rounds the distributed algorithm will take
def find_r(d, length):
    t = True
    r=0
    s=d
    while t:
       if s < length:
           r+=1
           s+=(2**r)*s
       else:
           r-=1
           t = False
    return r

# This calculates a sketch between a set of streams
def count_min(X,delta,k,d):
    cod_mat = [[0 for i in range(len(X))] for j in range(len(X))]
    X1 = [[(X[i])[j] for j in range(d)] for i in range(len(X))]
    l = d
    h = [hash_rand.Hash(32, int(math.log(k,2))) for _ in range(int(math.log(1/delta))+1)]
    for i in range(len(X)):                  # That would be the first round
        for j in range(len(X)):
            (cod_mat[i])[j] = sketch_int(X1[i],X1[j], k, delta, h)
    for r in range(find_r(d, len(min(X[0],X[1])))): # We be iteratin' now!
        X_int = [[(X[i])[l+j] for j in range((2**(r+1))*d)] for i in range(len(X))]
        l += (2**(r+1))*d
        cod_temp = [[(cod_mat[i])[j] for i in range(len(X))] for j in range(len(X))]
        for i in range(len(X)):   
            for j in range(len(X)):
                (cod_mat[i])[j] = (sketch_int(X_int[i],X_int[j], k, delta,h) + (cod_temp[i])[j])
    return cod_mat

    
#this function will split elements of 2 lists according to a hash function
def hash_split(X, Y, h, k):
    if len(X) != len(Y):
        return [], []
    Xk = [[] for _ in range(k)]
    Yk = [[] for _ in range(k)]
    for i in range(len(X)):
        Xk[h(i)].append(X[i])
        Yk[h(i)].append(Y[i])
    return Xk, Yk

####### Function relative to parsed information

# This function allows us to get the relevant bit of parsed information    
def get_group(sample, i, s):
    if sample[i] == None:
        return 0
    else:
        return (sample[i].group(s))

# return -1 if a is not in l, the first position of a in l otherwise
def belong(l,a):
    for i in range(len(l)):
        if l[i] == a:
            return i
    return (-1)

# Returns the number of distinct elements in l
def distinct(l):
    D=[]
    for i in range(len(l)):
        if (belong(D,l[i]))<0:
            D.append(l[i])
    return len(D)

# Replaces character strings by numbers
def make_standard(data, s, max):
    D=[]
    Used=[]
    for i in range(max):
        if belong(Used,get_group(data,i,s))<0:
            Used.append(get_group(data,i,s))
            D.append(len(Used))
        else:
            D.append(belong(Used,get_group(data,i,s)))
    return D

    
data1 = parser.parseFile("1epahttp.txt","epahttp")
data2 = parser.parseFile("2sdschttp2.txt","sdschttp")
data3 = parser.parseFile("3Calgaryaccess_log.txt","calgaryhttp")         
sample1 = make_standard(data1, "host", 25000)
sample2 = make_standard(data2, "host", 25000)
sample3 = make_standard(data3, "host", 25000)


print(ecart([sketch_cod2(sample1, sample2, 64, 0.0001) for i in range(100)]))
#print(count_min([sample1,sample2,sample3],0.000001,1024,25000))

