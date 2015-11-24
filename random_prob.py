import random


# This makes a flux of length size, with elements taken according to law prob, with parameter p(for binomial law) going to max length of max_int
def makeFlux(size, prob, p, max_int):
    l = []
    for i in range(size):
        l += [random_pick(prob,p,max_int)]
    return l

# This does the picking!
def random_pick(prob, p, max_int):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    result = 0
    for i in range(max_int):
        cumulative_probability += prob(p, max_int, i)
        if x < cumulative_probability:
            break
    return i

# Here come the laws...
def uniform_law(p, max_int, i):
    if i > max_int:
        return 0
    return (1./max_int)

def binomialCoeff(n, k):
    result = 1
    for i in range(1, k+1):
        result = result * (n-i+1) / i
    return result

def binomial_law(p,max_int,i):
    return (binomialCoeff(max_int, i))*(p**i)*((1-p)**(max_int-i))

